from django.core.management.base import BaseCommand

from resources.models import EquipmentItem, StudyRoom


ROOMS = [
    {
        "building": "Main Building",
        "room_number": "101",
        "name": "Quiet Study Room",
        "capacity": 8,
        "description": "A small room for individual and quiet group study.",
    },
    {
        "building": "Main Building",
        "room_number": "204",
        "name": "Project Room",
        "capacity": 12,
        "description": "A room with a display and a whiteboard.",
    },
    {
        "building": "Library",
        "room_number": "L12",
        "name": "Library Team Room",
        "capacity": 6,
        "description": "A reservable team room near the reading area.",
    },
    {
        "building": "Engineering Centre",
        "room_number": "E07",
        "name": "Workshop Meeting Room",
        "capacity": 16,
        "description": "A larger room for technical project meetings.",
    },
]

EQUIPMENT = [
    {
        "inventory_code": "LAP-001",
        "name": "Dell Latitude Laptop",
        "category": EquipmentItem.Category.LAPTOP,
        "condition": EquipmentItem.Condition.GOOD,
        "location": "Library desk",
    },
    {
        "inventory_code": "LAP-002",
        "name": "Lenovo ThinkPad Laptop",
        "category": EquipmentItem.Category.LAPTOP,
        "condition": EquipmentItem.Condition.EXCELLENT,
        "location": "Library desk",
    },
    {
        "inventory_code": "PRO-001",
        "name": "Portable Projector",
        "category": EquipmentItem.Category.PROJECTOR,
        "condition": EquipmentItem.Condition.GOOD,
        "location": "Main Building reception",
    },
    {
        "inventory_code": "CAM-001",
        "name": "Mirrorless Camera",
        "category": EquipmentItem.Category.CAMERA,
        "condition": EquipmentItem.Condition.GOOD,
        "location": "Media laboratory",
    },
    {
        "inventory_code": "AUD-001",
        "name": "USB Podcast Microphone",
        "category": EquipmentItem.Category.AUDIO,
        "condition": EquipmentItem.Condition.EXCELLENT,
        "location": "Media laboratory",
    },
    {
        "inventory_code": "LAB-001",
        "name": "Digital Oscilloscope",
        "category": EquipmentItem.Category.LAB_DEVICE,
        "condition": EquipmentItem.Condition.FAIR,
        "location": "Electronics laboratory",
    },
]


class Command(BaseCommand):
    help = "Create or update demonstration rooms and equipment."

    def handle(self, *args, **options):
        created_rooms = self._seed_rooms()
        created_equipment = self._seed_equipment()

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data is ready: "
                f"created {created_rooms} rooms and "
                f"{created_equipment} equipment items."
            )
        )

    def _seed_rooms(self):
        created_count = 0
        for room_data in ROOMS:
            lookup = {
                "building": room_data["building"],
                "room_number": room_data["room_number"],
            }
            defaults = {
                key: value
                for key, value in room_data.items()
                if key not in lookup
            }
            _, created = StudyRoom.objects.update_or_create(
                **lookup,
                defaults=defaults,
            )
            created_count += int(created)
        return created_count

    def _seed_equipment(self):
        created_count = 0
        for item_data in EQUIPMENT:
            inventory_code = item_data["inventory_code"]
            defaults = {
                key: value
                for key, value in item_data.items()
                if key != "inventory_code"
            }
            _, created = EquipmentItem.objects.update_or_create(
                inventory_code=inventory_code,
                defaults=defaults,
            )
            created_count += int(created)
        return created_count
