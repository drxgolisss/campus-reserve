from django.urls import path

from . import views

app_name = "resources"

urlpatterns = [
    path("rooms/", views.room_list, name="room-list"),
    path("rooms/add/", views.room_create, name="room-create"),
    path("rooms/<int:pk>/edit/", views.room_update, name="room-update"),
    path("equipment/", views.equipment_list, name="equipment-list"),
    path("equipment/add/", views.equipment_create, name="equipment-create"),
    path(
        "equipment/<int:pk>/edit/",
        views.equipment_update,
        name="equipment-update",
    ),
]
