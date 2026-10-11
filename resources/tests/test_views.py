from django.test import TestCase
from django.urls import reverse

from resources.models import EquipmentItem, StudyRoom


class RoomListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.small_room = StudyRoom.objects.create(
            name="Quiet Study Room",
            building="Library",
            room_number="L12",
            capacity=6,
        )
        cls.large_room = StudyRoom.objects.create(
            name="Project Room",
            building="Main Building",
            room_number="204",
            capacity=12,
        )
        cls.inactive_room = StudyRoom.objects.create(
            name="Closed Room",
            building="Main Building",
            room_number="205",
            capacity=20,
            is_active=False,
        )

    def test_page_displays_only_active_rooms(self):
        response = self.client.get(reverse("resources:room-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/room_list.html")
        self.assertContains(response, self.small_room.name)
        self.assertContains(response, self.large_room.name)
        self.assertNotContains(response, self.inactive_room.name)

    def test_filters_rooms_by_building_and_capacity(self):
        response = self.client.get(
            reverse("resources:room-list"),
            {"building": "Main Building", "min_capacity": 10},
        )

        self.assertContains(response, self.large_room.name)
        self.assertNotContains(response, self.small_room.name)

    def test_rejects_invalid_minimum_capacity(self):
        response = self.client.get(
            reverse("resources:room-list"),
            {"min_capacity": 0},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["filter_form"].errors)


class EquipmentListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.laptop = EquipmentItem.objects.create(
            name="Dell Latitude Laptop",
            category=EquipmentItem.Category.LAPTOP,
            inventory_code="LAP-001",
            condition=EquipmentItem.Condition.GOOD,
            location="Library desk",
        )
        cls.projector = EquipmentItem.objects.create(
            name="Portable Projector",
            category=EquipmentItem.Category.PROJECTOR,
            inventory_code="PRO-001",
            condition=EquipmentItem.Condition.EXCELLENT,
            location="Main Building reception",
        )
        cls.inactive_item = EquipmentItem.objects.create(
            name="Retired Camera",
            category=EquipmentItem.Category.CAMERA,
            inventory_code="CAM-OLD",
            condition=EquipmentItem.Condition.FAIR,
            location="Storage",
            is_active=False,
        )

    def test_page_displays_only_active_equipment(self):
        response = self.client.get(reverse("resources:equipment-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/equipment_list.html")
        self.assertContains(response, self.laptop.name)
        self.assertContains(response, self.projector.name)
        self.assertNotContains(response, self.inactive_item.name)

    def test_filters_equipment_by_category_and_search_query(self):
        response = self.client.get(
            reverse("resources:equipment-list"),
            {"category": EquipmentItem.Category.LAPTOP, "q": "Library"},
        )

        self.assertContains(response, self.laptop.name)
        self.assertNotContains(response, self.projector.name)
