from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.roles import MANAGER, STUDENT
from bookings.models import EquipmentBooking, RoomBooking
from resources.models import EquipmentItem, StudyRoom


class BookingViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("setup_roles", verbosity=0)
        user_model = get_user_model()
        cls.student = user_model.objects.create_user(username="student")
        cls.other_student = user_model.objects.create_user(username="other-student")
        cls.manager = user_model.objects.create_user(username="manager")
        cls.unassigned_user = user_model.objects.create_user(username="unassigned")
        cls.student.groups.add(Group.objects.get(name=STUDENT))
        cls.other_student.groups.add(Group.objects.get(name=STUDENT))
        cls.manager.groups.add(Group.objects.get(name=MANAGER))

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

    def setUp(self):
        self.start = timezone.localtime(timezone.now() + timedelta(days=1)).replace(
            second=0,
            microsecond=0,
        )
        self.end = self.start + timedelta(hours=1)

    def booking_data(self, resource_field, resource, **overrides):
        data = {
            resource_field: resource.pk,
            "start_time": self.start.strftime("%Y-%m-%dT%H:%M"),
            "end_time": self.end.strftime("%Y-%m-%dT%H:%M"),
            "comment": "Group project",
        }
        data.update(overrides)
        return data

    def test_anonymous_user_is_redirected_to_login(self):
        url = reverse("bookings:list")

        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={url}",
            fetch_redirect_response=False,
        )

    def test_user_without_role_cannot_open_booking_list(self):
        self.client.force_login(self.unassigned_user)

        response = self.client.get(reverse("bookings:list"))

        self.assertEqual(response.status_code, 403)

    def test_student_can_create_room_booking_but_not_choose_owner_or_status(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("bookings:room-create"),
            self.booking_data(
                "room",
                self.room,
                user=self.other_student.pk,
                status=RoomBooking.Status.APPROVED,
            ),
        )

        self.assertRedirects(response, reverse("bookings:list"))
        booking = RoomBooking.objects.get()
        self.assertEqual(booking.user, self.student)
        self.assertEqual(booking.status, RoomBooking.Status.PENDING)

    def test_booking_create_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.student)

        response = csrf_client.post(
            reverse("bookings:room-create"),
            self.booking_data("room", self.room),
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(RoomBooking.objects.exists())

    @patch("bookings.views.StudyRoom.objects.select_for_update")
    def test_resource_removed_during_create_returns_form_error(self, select_for_update):
        select_for_update.return_value.get.side_effect = StudyRoom.DoesNotExist
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("bookings:room-create"),
            self.booking_data("room", self.room),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "no longer available")
        self.assertFalse(RoomBooking.objects.exists())

    def test_student_can_create_equipment_booking(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("bookings:equipment-create"),
            self.booking_data("equipment", self.equipment),
        )

        self.assertRedirects(response, reverse("bookings:list"))
        self.assertTrue(
            EquipmentBooking.objects.filter(
                user=self.student,
                equipment=self.equipment,
            ).exists()
        )

    def test_overlapping_room_booking_is_rejected_by_create_view(self):
        RoomBooking.objects.create(
            user=self.other_student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("bookings:room-create"),
            self.booking_data("room", self.room),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already has a booking")
        self.assertEqual(RoomBooking.objects.count(), 1)

    def test_booking_form_is_available_and_prefills_selected_resource(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse("bookings:room-create"),
            {"room": self.room.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].initial["room"],
            str(self.room.pk),
        )

    def test_booking_list_contains_only_current_users_records(self):
        own_booking = RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        other_booking = RoomBooking.objects.create(
            user=self.other_student,
            room=self.other_room,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.student)

        response = self.client.get(reverse("bookings:list"))

        self.assertContains(response, own_booking.room.name)
        self.assertNotContains(response, other_booking.room.name)

    def test_student_cannot_edit_another_users_booking(self):
        booking = RoomBooking.objects.create(
            user=self.other_student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.student)

        response = self.client.get(
            reverse("bookings:room-update", args=[booking.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_only_pending_booking_can_be_edited(self):
        booking = RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
            status=RoomBooking.Status.APPROVED,
        )
        self.client.force_login(self.student)

        response = self.client.get(
            reverse("bookings:room-update", args=[booking.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_student_can_edit_own_pending_booking(self):
        booking = RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.student)
        new_end = self.end + timedelta(hours=1)

        response = self.client.post(
            reverse("bookings:room-update", args=[booking.pk]),
            self.booking_data(
                "room",
                self.room,
                end_time=new_end.strftime("%Y-%m-%dT%H:%M"),
                comment="Updated comment",
            ),
        )

        self.assertRedirects(response, reverse("bookings:list"))
        booking.refresh_from_db()
        self.assertEqual(booking.end_time, new_end)
        self.assertEqual(booking.comment, "Updated comment")

    def test_edit_cannot_move_booking_into_an_occupied_time(self):
        RoomBooking.objects.create(
            user=self.other_student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        booking = RoomBooking.objects.create(
            user=self.student,
            room=self.other_room,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("bookings:room-update", args=[booking.pk]),
            self.booking_data("room", self.room),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already has a booking")
        booking.refresh_from_db()
        self.assertEqual(booking.room, self.other_room)

    def test_student_can_edit_and_cancel_equipment_booking(self):
        booking = EquipmentBooking.objects.create(
            user=self.student,
            equipment=self.equipment,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.student)

        update_response = self.client.post(
            reverse("bookings:equipment-update", args=[booking.pk]),
            self.booking_data(
                "equipment",
                self.equipment,
                comment="Updated equipment request",
            ),
        )
        cancel_response = self.client.post(
            reverse("bookings:equipment-cancel", args=[booking.pk])
        )

        self.assertRedirects(update_response, reverse("bookings:list"))
        self.assertRedirects(cancel_response, reverse("bookings:list"))
        booking.refresh_from_db()
        self.assertEqual(booking.comment, "Updated equipment request")
        self.assertEqual(booking.status, EquipmentBooking.Status.CANCELLED)

    def test_cancellation_requires_post_and_ownership(self):
        own_booking = RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        other_booking = EquipmentBooking.objects.create(
            user=self.other_student,
            equipment=self.equipment,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.student)

        get_response = self.client.get(
            reverse("bookings:room-cancel", args=[own_booking.pk])
        )
        other_response = self.client.post(
            reverse("bookings:equipment-cancel", args=[other_booking.pk])
        )
        cancel_response = self.client.post(
            reverse("bookings:room-cancel", args=[own_booking.pk])
        )

        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(other_response.status_code, 404)
        self.assertRedirects(cancel_response, reverse("bookings:list"))
        own_booking.refresh_from_db()
        self.assertEqual(own_booking.status, RoomBooking.Status.CANCELLED)

    def test_student_cannot_open_manager_queue(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("bookings:manage"))

        self.assertEqual(response.status_code, 403)

    def test_student_cannot_post_manager_status_action(self):
        booking = RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("bookings:room-status", args=[booking.pk, "approve"])
        )

        self.assertEqual(response.status_code, 403)
        booking.refresh_from_db()
        self.assertEqual(booking.status, RoomBooking.Status.PENDING)

    def test_manager_can_approve_and_reject_pending_bookings(self):
        room_booking = RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        equipment_booking = EquipmentBooking.objects.create(
            user=self.student,
            equipment=self.equipment,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.manager)

        approve_response = self.client.post(
            reverse(
                "bookings:room-status",
                args=[room_booking.pk, "approve"],
            )
        )
        reject_response = self.client.post(
            reverse(
                "bookings:equipment-status",
                args=[equipment_booking.pk, "reject"],
            )
        )

        self.assertRedirects(approve_response, reverse("bookings:manage"))
        self.assertRedirects(reject_response, reverse("bookings:manage"))
        room_booking.refresh_from_db()
        equipment_booking.refresh_from_db()
        self.assertEqual(room_booking.status, RoomBooking.Status.APPROVED)
        self.assertEqual(
            equipment_booking.status,
            EquipmentBooking.Status.REJECTED,
        )

    def test_manager_transition_requires_post_and_pending_status(self):
        booking = RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
            status=RoomBooking.Status.REJECTED,
        )
        self.client.force_login(self.manager)
        url = reverse("bookings:room-status", args=[booking.pk, "approve"])

        get_response = self.client.get(url)
        post_response = self.client.post(url)

        self.assertEqual(get_response.status_code, 405)
        self.assertRedirects(post_response, reverse("bookings:manage"))
        booking.refresh_from_db()
        self.assertEqual(booking.status, RoomBooking.Status.REJECTED)

    def test_unknown_manager_action_is_rejected(self):
        booking = RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        self.client.force_login(self.manager)

        response = self.client.post(
            reverse(
                "bookings:room-status",
                args=[booking.pk, "archive"],
            )
        )

        self.assertEqual(response.status_code, 400)
        booking.refresh_from_db()
        self.assertEqual(booking.status, RoomBooking.Status.PENDING)

    def test_approval_rechecks_booking_conflicts(self):
        RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        conflicting = RoomBooking.objects.create(
            user=self.other_student,
            room=self.room,
            start_time=self.start + timedelta(minutes=15),
            end_time=self.end + timedelta(minutes=15),
        )
        self.client.force_login(self.manager)

        response = self.client.post(
            reverse(
                "bookings:room-status",
                args=[conflicting.pk, "approve"],
            )
        )

        self.assertRedirects(response, reverse("bookings:manage"))
        conflicting.refresh_from_db()
        self.assertEqual(conflicting.status, RoomBooking.Status.PENDING)

    def test_manager_cannot_approve_booking_for_inactive_resource(self):
        booking = RoomBooking.objects.create(
            user=self.student,
            room=self.room,
            start_time=self.start,
            end_time=self.end,
        )
        self.room.is_active = False
        self.room.save(update_fields=["is_active"])
        self.client.force_login(self.manager)

        response = self.client.post(
            reverse("bookings:room-status", args=[booking.pk, "approve"])
        )

        self.assertRedirects(response, reverse("bookings:manage"))
        booking.refresh_from_db()
        self.assertEqual(booking.status, RoomBooking.Status.PENDING)
