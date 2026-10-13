from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from bookings.forms import EquipmentBookingForm, RoomBookingForm
from bookings.models import RoomBooking
from resources.models import EquipmentItem, StudyRoom


class BookingFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="student")
        cls.room = StudyRoom.objects.create(
            name="Project Room",
            building="Library",
            room_number="201",
            capacity=8,
        )
        cls.inactive_room = StudyRoom.objects.create(
            name="Renovated Room",
            building="Main Building",
            room_number="105",
            capacity=10,
            is_active=False,
        )
        cls.equipment = EquipmentItem.objects.create(
            name="Projector",
            category=EquipmentItem.Category.PROJECTOR,
            inventory_code="PRO-101",
            condition=EquipmentItem.Condition.GOOD,
            location="Library reception",
        )

    def booking_data(self, **overrides):
        start = timezone.localtime(timezone.now() + timedelta(days=1))
        data = {
            "room": self.room.pk,
            "start_time": start.strftime("%Y-%m-%dT%H:%M"),
            "end_time": (start + timedelta(hours=1)).strftime(
                "%Y-%m-%dT%H:%M"
            ),
            "comment": "Group study",
        }
        data.update(overrides)
        return data

    def test_forms_do_not_expose_user_or_status(self):
        room_form = RoomBookingForm()
        equipment_form = EquipmentBookingForm()

        self.assertNotIn("user", room_form.fields)
        self.assertNotIn("status", room_form.fields)
        self.assertNotIn("user", equipment_form.fields)
        self.assertNotIn("status", equipment_form.fields)

    def test_only_active_resources_are_available(self):
        form = RoomBookingForm()

        self.assertIn(self.room, form.fields["room"].queryset)
        self.assertNotIn(self.inactive_room, form.fields["room"].queryset)

    def test_datetime_fields_use_browser_datetime_local_widget(self):
        form = RoomBookingForm()

        self.assertEqual(form.fields["start_time"].widget.input_type, "datetime-local")
        self.assertEqual(form.fields["end_time"].widget.input_type, "datetime-local")

    def test_form_rejects_an_overlapping_booking(self):
        start = timezone.localtime(timezone.now() + timedelta(days=1))
        RoomBooking.objects.create(
            user=self.user,
            room=self.room,
            start_time=start,
            end_time=start + timedelta(hours=1),
        )
        data = self.booking_data(
            start_time=(start + timedelta(minutes=15)).strftime(
                "%Y-%m-%dT%H:%M"
            ),
            end_time=(start + timedelta(hours=2)).strftime(
                "%Y-%m-%dT%H:%M"
            ),
        )

        form = RoomBookingForm(data=data, instance=RoomBooking(user=self.user))

        self.assertFalse(form.is_valid())
        self.assertIn("already has a booking", form.non_field_errors()[0])
