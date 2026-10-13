from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from bookings.models import EquipmentBooking, RoomBooking
from resources.models import EquipmentItem, StudyRoom


class BookingModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="student",
            password="test-password",
        )
        cls.other_user = get_user_model().objects.create_user(
            username="other-student",
            password="test-password",
        )
        cls.room = StudyRoom.objects.create(
            name="Project Room",
            building="Library",
            room_number="201",
            capacity=8,
        )
        cls.other_room = StudyRoom.objects.create(
            name="Quiet Room",
            building="Library",
            room_number="202",
            capacity=4,
        )
        cls.equipment = EquipmentItem.objects.create(
            name="Projector",
            category=EquipmentItem.Category.PROJECTOR,
            inventory_code="PRO-101",
            condition=EquipmentItem.Condition.GOOD,
            location="Library reception",
        )
        cls.start = timezone.now() + timedelta(days=1)
        cls.end = cls.start + timedelta(hours=2)

    def test_end_time_must_be_later_than_start_time(self):
        booking = RoomBooking(
            user=self.user,
            room=self.room,
            start_time=self.start,
            end_time=self.start,
        )

        with self.assertRaisesMessage(
            ValidationError,
            "End time must be later than start time.",
        ):
            booking.full_clean()

    def test_inactive_resource_cannot_be_booked(self):
        self.room.is_active = False
        self.room.save()
        booking = RoomBooking(
            user=self.user,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )

        with self.assertRaisesMessage(ValidationError, "not available"):
            booking.full_clean()

    def test_inactive_resource_booking_can_be_rejected(self):
        self.room.is_active = False
        self.room.save()
        booking = RoomBooking(
            user=self.user,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
            status=RoomBooking.Status.REJECTED,
        )

        booking.full_clean()

    def test_pending_booking_blocks_overlapping_time(self):
        RoomBooking.objects.create(
            user=self.user,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        overlapping = RoomBooking(
            user=self.other_user,
            room=self.room,
            start_time=self.start + timedelta(hours=1),
            end_time=self.end + timedelta(hours=1),
        )

        with self.assertRaisesMessage(ValidationError, "already has a booking"):
            overlapping.full_clean()

    def test_approved_booking_blocks_overlapping_time(self):
        EquipmentBooking.objects.create(
            user=self.user,
            equipment=self.equipment,
            start_time=self.start,
            end_time=self.end,
            status=EquipmentBooking.Status.APPROVED,
        )
        overlapping = EquipmentBooking(
            user=self.other_user,
            equipment=self.equipment,
            start_time=self.start + timedelta(minutes=30),
            end_time=self.end,
        )

        with self.assertRaisesMessage(ValidationError, "already has a booking"):
            overlapping.full_clean()

    def test_cancelled_and_rejected_bookings_do_not_block_time(self):
        for status in [RoomBooking.Status.CANCELLED, RoomBooking.Status.REJECTED]:
            RoomBooking.objects.create(
                user=self.user,
                room=self.room,
                start_time=self.start,
                end_time=self.end,
                status=status,
            )

        booking = RoomBooking(
            user=self.other_user,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )

        booking.full_clean()

    def test_adjacent_and_different_resource_bookings_are_allowed(self):
        RoomBooking.objects.create(
            user=self.user,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        adjacent = RoomBooking(
            user=self.other_user,
            room=self.room,
            start_time=self.end,
            end_time=self.end + timedelta(hours=1),
        )
        another_room = RoomBooking(
            user=self.other_user,
            room=self.other_room,
            start_time=self.start,
            end_time=self.end,
        )

        adjacent.full_clean()
        another_room.full_clean()

    def test_booking_does_not_conflict_with_itself_when_edited(self):
        booking = RoomBooking.objects.create(
            user=self.user,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        booking.comment = "Need a whiteboard"

        booking.full_clean()
