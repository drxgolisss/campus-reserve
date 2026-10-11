from django.core.exceptions import ValidationError
from django.test import TestCase

from resources.models import EquipmentItem, StudyRoom


class StudyRoomModelTests(TestCase):
    def test_string_representation_contains_location_and_name(self):
        room = StudyRoom(
            name="Project Room",
            building="Main Building",
            room_number="204",
            capacity=12,
        )

        self.assertEqual(str(room), "Main Building 204 — Project Room")

    def test_capacity_must_be_at_least_one(self):
        room = StudyRoom(
            name="Invalid Room",
            building="Main Building",
            room_number="000",
            capacity=0,
        )

        with self.assertRaises(ValidationError):
            room.full_clean()


class EquipmentItemModelTests(TestCase):
    def test_string_representation_contains_inventory_code(self):
        item = EquipmentItem(
            name="Portable Projector",
            category=EquipmentItem.Category.PROJECTOR,
            inventory_code="PRO-001",
            condition=EquipmentItem.Condition.GOOD,
            location="Main Building reception",
        )

        self.assertEqual(str(item), "Portable Projector (PRO-001)")
