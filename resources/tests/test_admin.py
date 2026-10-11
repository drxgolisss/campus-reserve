from django.contrib import admin
from django.test import SimpleTestCase

from resources.models import EquipmentItem, StudyRoom


class ResourceAdminTests(SimpleTestCase):
    def test_resource_models_are_registered(self):
        self.assertIn(StudyRoom, admin.site._registry)
        self.assertIn(EquipmentItem, admin.site._registry)
