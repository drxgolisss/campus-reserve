from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.booking_list, name="list"),
    path("rooms/new/", views.room_booking_create, name="room-create"),
    path(
        "rooms/<int:pk>/edit/",
        views.room_booking_update,
        name="room-update",
    ),
    path(
        "rooms/<int:pk>/cancel/",
        views.room_booking_cancel,
        name="room-cancel",
    ),
    path(
        "equipment/new/",
        views.equipment_booking_create,
        name="equipment-create",
    ),
    path(
        "equipment/<int:pk>/edit/",
        views.equipment_booking_update,
        name="equipment-update",
    ),
    path(
        "equipment/<int:pk>/cancel/",
        views.equipment_booking_cancel,
        name="equipment-cancel",
    ),
    path("manage/", views.booking_management, name="manage"),
    path(
        "manage/rooms/<int:pk>/<str:action>/",
        views.room_booking_status_update,
        name="room-status",
    ),
    path(
        "manage/equipment/<int:pk>/<str:action>/",
        views.equipment_booking_status_update,
        name="equipment-status",
    ),
]
