from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from resources.models import EquipmentItem, StudyRoom


class ResourceManagementViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="resource-manager")
        cls.room = StudyRoom.objects.create(
            name="Team Room",
            building="Library",
            room_number="L10",
            capacity=8,
        )
        cls.equipment = EquipmentItem.objects.create(
            name="Portable Projector",
            category=EquipmentItem.Category.PROJECTOR,
            inventory_code="PRO-010",
            condition=EquipmentItem.Condition.GOOD,
            location="Library desk",
        )

    def give_permission(self, codename):
        permission = Permission.objects.get(
            content_type__app_label="resources",
            codename=codename,
        )
        self.user.user_permissions.add(permission)

    def test_anonymous_user_is_redirected_to_login(self):
        url = reverse("resources:room-create")

        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={url}",
            fetch_redirect_response=False,
        )

    def test_authenticated_user_without_permission_gets_forbidden_response(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("resources:equipment-create"))

        self.assertEqual(response.status_code, 403)

    def test_user_with_permission_can_create_room(self):
        self.give_permission("add_studyroom")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("resources:room-create"),
            {
                "name": "Silent Room",
                "building": "Science Centre",
                "room_number": "S21",
                "capacity": 12,
                "description": "Room for quiet study.",
                "is_active": "on",
            },
        )

        self.assertRedirects(response, reverse("resources:room-list"))
        self.assertTrue(
            StudyRoom.objects.filter(
                building="Science Centre",
                room_number="S21",
            ).exists()
        )

    def test_invalid_room_form_is_displayed_without_saving(self):
        self.give_permission("add_studyroom")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("resources:room-create"),
            {
                "name": "Invalid Room",
                "building": "Library",
                "room_number": "L11",
                "capacity": 0,
                "is_active": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "capacity",
            "Ensure this value is greater than or equal to 1.",
        )
        self.assertFalse(StudyRoom.objects.filter(room_number="L11").exists())

    def test_user_with_permission_can_update_and_deactivate_room(self):
        self.give_permission("change_studyroom")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("resources:room-update", args=[self.room.pk]),
            {
                "name": "Updated Team Room",
                "building": self.room.building,
                "room_number": self.room.room_number,
                "capacity": 10,
                "description": "",
            },
        )

        self.assertRedirects(response, reverse("resources:room-list"))
        self.room.refresh_from_db()
        self.assertEqual(self.room.name, "Updated Team Room")
        self.assertEqual(self.room.capacity, 10)
        self.assertFalse(self.room.is_active)

    def test_user_with_permission_can_create_equipment(self):
        self.give_permission("add_equipmentitem")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("resources:equipment-create"),
            {
                "name": "Video Camera",
                "category": EquipmentItem.Category.CAMERA,
                "inventory_code": "CAM-021",
                "condition": EquipmentItem.Condition.EXCELLENT,
                "location": "Media office",
                "description": "",
                "is_active": "on",
            },
        )

        self.assertRedirects(response, reverse("resources:equipment-list"))
        self.assertTrue(
            EquipmentItem.objects.filter(inventory_code="CAM-021").exists()
        )

    def test_duplicate_inventory_code_is_rejected(self):
        self.give_permission("add_equipmentitem")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("resources:equipment-create"),
            {
                "name": "Second Projector",
                "category": EquipmentItem.Category.PROJECTOR,
                "inventory_code": self.equipment.inventory_code,
                "condition": EquipmentItem.Condition.GOOD,
                "location": "Main reception",
                "is_active": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "inventory_code",
            "Equipment item with this Inventory code already exists.",
        )
        self.assertEqual(EquipmentItem.objects.count(), 1)

    def test_user_with_permission_can_update_and_deactivate_equipment(self):
        self.give_permission("change_equipmentitem")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("resources:equipment-update", args=[self.equipment.pk]),
            {
                "name": self.equipment.name,
                "category": self.equipment.category,
                "inventory_code": self.equipment.inventory_code,
                "condition": EquipmentItem.Condition.MAINTENANCE,
                "location": "Service room",
                "description": "Waiting for inspection.",
            },
        )

        self.assertRedirects(response, reverse("resources:equipment-list"))
        self.equipment.refresh_from_db()
        self.assertEqual(
            self.equipment.condition,
            EquipmentItem.Condition.MAINTENANCE,
        )
        self.assertEqual(self.equipment.location, "Service room")
        self.assertFalse(self.equipment.is_active)
