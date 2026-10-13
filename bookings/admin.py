from django.contrib import admin

from .models import EquipmentBooking, RoomBooking


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "resource",
        "user",
        "start_time",
        "end_time",
        "status",
    )
    list_filter = ("status", "start_time")
    search_fields = ("user__username",)
    ordering = ("-start_time",)

    @admin.display(description="Resource")
    def resource(self, obj):
        return getattr(obj, obj.resource_field)


@admin.register(RoomBooking)
class RoomBookingAdmin(BookingAdmin):
    search_fields = (*BookingAdmin.search_fields, "room__name", "room__room_number")


@admin.register(EquipmentBooking)
class EquipmentBookingAdmin(BookingAdmin):
    search_fields = (
        *BookingAdmin.search_fields,
        "equipment__name",
        "equipment__inventory_code",
    )

