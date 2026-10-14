from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.roles import ADMINISTRATOR, MANAGER, STUDENT
from bookings.models import EquipmentBooking, RoomBooking
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

DEMO_PASSWORD = "CampusDemo2026!"
DEMO_USERS = {
    "student_demo": STUDENT,
    "manager_demo": MANAGER,
    "admin_demo": ADMINISTRATOR,
}


class Command(BaseCommand):
    help = "Create or update demonstration users, resources, and bookings."

    def handle(self, *args, **options):
        call_command("setup_roles", verbosity=0)
        created_rooms = self._seed_rooms()
        created_equipment = self._seed_equipment()
        created_users, users = self._seed_users()
        created_bookings = self._seed_bookings(users)

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data is ready: "
                f"created {created_rooms} rooms and "
                f"{created_equipment} equipment items, "
                f"{created_users} users, and "
                f"{created_bookings} bookings."
            )
        )
        self.stdout.write(
            "Demo accounts: student_demo, manager_demo, admin_demo "
            f"(password: {DEMO_PASSWORD})"
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
            defaults["is_active"] = True
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
            defaults["is_active"] = True
            _, created = EquipmentItem.objects.update_or_create(
                inventory_code=inventory_code,
                defaults=defaults,
            )
            created_count += int(created)
        return created_count

    def _seed_users(self):
        user_model = get_user_model()
        users = {}
        created_count = 0

        for username, role_name in DEMO_USERS.items():
            user, created = user_model.objects.get_or_create(username=username)
            user.email = f"{username}@example.com"
            user.is_active = True
            user.is_staff = role_name == ADMINISTRATOR
            user.set_password(DEMO_PASSWORD)
            user.save()
            user.groups.set([Group.objects.get(name=role_name)])
            users[role_name] = user
            created_count += int(created)

        return created_count, users

    def _seed_bookings(self, users):
        start_time = timezone.now().replace(minute=0, second=0, microsecond=0)
        start_time += timedelta(days=1, hours=1)
        end_time = start_time + timedelta(hours=2)
        room = StudyRoom.objects.get(building="Main Building", room_number="204")
        equipment = EquipmentItem.objects.get(inventory_code="PRO-001")

        room_booking = RoomBooking.objects.filter(
            user=users[STUDENT],
            room=room,
            comment="Demo project meeting",
        ).first()
        room_created = room_booking is None
        if room_booking is None:
            room_booking = RoomBooking(user=users[STUDENT], room=room)
        room_booking.start_time = start_time
        room_booking.end_time = end_time
        room_booking.status = RoomBooking.Status.PENDING
        room_booking.comment = "Demo project meeting"
        room_booking.save()

        equipment_booking = EquipmentBooking.objects.filter(
            user=users[STUDENT],
            equipment=equipment,
            comment="Demo presentation",
        ).first()
        equipment_created = equipment_booking is None
        if equipment_booking is None:
            equipment_booking = EquipmentBooking(
                user=users[STUDENT],
                equipment=equipment,
            )
        equipment_booking.start_time = start_time
        equipment_booking.end_time = end_time
        equipment_booking.status = EquipmentBooking.Status.APPROVED
        equipment_booking.comment = "Demo presentation"
        equipment_booking.save()

        return int(room_created) + int(equipment_created)
