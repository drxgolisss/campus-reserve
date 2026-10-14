from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase

from accounts.roles import ADMINISTRATOR, MANAGER, STUDENT
from bookings.models import EquipmentBooking, RoomBooking
from resources.models import EquipmentItem, StudyRoom


class SeedDemoCommandTests(TestCase):
    def test_command_creates_demo_data_and_is_repeatable(self):
        first_output = StringIO()
        call_command("seed_demo", stdout=first_output)

        self.assertEqual(StudyRoom.objects.count(), 4)
        self.assertEqual(EquipmentItem.objects.count(), 6)
        self.assertEqual(get_user_model().objects.count(), 3)
        self.assertEqual(RoomBooking.objects.count(), 1)
        self.assertEqual(EquipmentBooking.objects.count(), 1)
        self.assertIn("created 4 rooms", first_output.getvalue())

        for username, role_name in {
            "student_demo": STUDENT,
            "manager_demo": MANAGER,
            "admin_demo": ADMINISTRATOR,
        }.items():
            user = get_user_model().objects.get(username=username)
            self.assertTrue(user.groups.filter(name=role_name).exists())

        self.assertTrue(Group.objects.filter(name=STUDENT).exists())

        room = StudyRoom.objects.get(building="Main Building", room_number="204")
        equipment = EquipmentItem.objects.get(inventory_code="PRO-001")
        student = get_user_model().objects.get(username="student_demo")
        demo_room_booking = room.bookings.get(comment="Demo project meeting")
        RoomBooking.objects.create(
            user=student,
            room=room,
            start_time=demo_room_booking.end_time,
            end_time=demo_room_booking.end_time + timedelta(hours=1),
            comment="Student-created booking",
        )
        room.is_active = False
        equipment.is_active = False
        student.is_active = False
        room.save()
        equipment.save()
        student.save()

        second_output = StringIO()
        call_command("seed_demo", stdout=second_output)

        self.assertEqual(StudyRoom.objects.count(), 4)
        self.assertEqual(EquipmentItem.objects.count(), 6)
        self.assertEqual(get_user_model().objects.count(), 3)
        self.assertEqual(RoomBooking.objects.count(), 2)
        self.assertEqual(EquipmentBooking.objects.count(), 1)
        room.refresh_from_db()
        equipment.refresh_from_db()
        student.refresh_from_db()
        self.assertTrue(room.is_active)
        self.assertTrue(equipment.is_active)
        self.assertTrue(student.is_active)
        self.assertIn("created 0 rooms", second_output.getvalue())
        self.assertIn("0 equipment items", second_output.getvalue())
        self.assertIn("0 users", second_output.getvalue())
        self.assertIn("0 bookings", second_output.getvalue())
