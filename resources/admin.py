from django.contrib import admin

from .models import EquipmentItem, StudyRoom


@admin.register(StudyRoom)
class StudyRoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "building",
        "room_number",
        "capacity",
        "is_active",
    )
    list_filter = ("building", "is_active")
    search_fields = ("name", "building", "room_number")
    ordering = ("building", "room_number")


@admin.register(EquipmentItem)
class EquipmentItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "inventory_code",
        "category",
        "condition",
        "location",
        "is_active",
    )
    list_filter = ("category", "condition", "location", "is_active")
    search_fields = ("name", "inventory_code", "location")
    ordering = ("name", "inventory_code")
