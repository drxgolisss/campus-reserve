from django.db.models import Q
from django.shortcuts import render

from .forms import EquipmentFilterForm, RoomFilterForm
from .models import EquipmentItem, StudyRoom


def _is_htmx_request(request):
    return (
        request.headers.get("HX-Request") == "true"
        and request.headers.get("HX-History-Restore-Request") != "true"
    )


def room_list(request):
    rooms = StudyRoom.objects.filter(is_active=True)
    filter_form = RoomFilterForm(request.GET or None)

    if filter_form.is_valid():
        search_query = filter_form.cleaned_data["q"]
        building = filter_form.cleaned_data["building"]
        min_capacity = filter_form.cleaned_data["min_capacity"]

        if search_query:
            rooms = rooms.filter(
                Q(name__icontains=search_query)
                | Q(building__icontains=search_query)
                | Q(room_number__icontains=search_query)
            )
        if building:
            rooms = rooms.filter(building=building)
        if min_capacity is not None:
            rooms = rooms.filter(capacity__gte=min_capacity)

    template_name = (
        "resources/partials/room_catalog.html"
        if _is_htmx_request(request)
        else "resources/room_list.html"
    )
    return render(
        request,
        template_name,
        {"rooms": rooms, "filter_form": filter_form},
    )


def equipment_list(request):
    equipment = EquipmentItem.objects.filter(is_active=True)
    filter_form = EquipmentFilterForm(request.GET or None)

    if filter_form.is_valid():
        search_query = filter_form.cleaned_data["q"]
        category = filter_form.cleaned_data["category"]
        condition = filter_form.cleaned_data["condition"]

        if search_query:
            equipment = equipment.filter(
                Q(name__icontains=search_query)
                | Q(inventory_code__icontains=search_query)
                | Q(location__icontains=search_query)
            )
        if category:
            equipment = equipment.filter(category=category)
        if condition:
            equipment = equipment.filter(condition=condition)

    template_name = (
        "resources/partials/equipment_catalog.html"
        if _is_htmx_request(request)
        else "resources/equipment_list.html"
    )
    return render(
        request,
        template_name,
        {"equipment": equipment, "filter_form": filter_form},
    )
