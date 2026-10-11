from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from resources.models import EquipmentItem, StudyRoom


class SeedDemoCommandTests(TestCase):
    def test_command_creates_demo_data_and_is_repeatable(self):
        first_output = StringIO()
        call_command("seed_demo", stdout=first_output)

        self.assertEqual(StudyRoom.objects.count(), 4)
        self.assertEqual(EquipmentItem.objects.count(), 6)
        self.assertIn("created 4 rooms", first_output.getvalue())

        second_output = StringIO()
        call_command("seed_demo", stdout=second_output)

        self.assertEqual(StudyRoom.objects.count(), 4)
        self.assertEqual(EquipmentItem.objects.count(), 6)
        self.assertIn("created 0 rooms", second_output.getvalue())
        self.assertIn("0 equipment items", second_output.getvalue())
