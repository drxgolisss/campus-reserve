from django.urls import path

from . import views

app_name = "resources"

urlpatterns = [
    path("rooms/", views.room_list, name="room-list"),
    path("equipment/", views.equipment_list, name="equipment-list"),
]
