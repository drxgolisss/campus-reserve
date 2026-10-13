from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from resources.models import EquipmentItem, StudyRoom

from .forms import EquipmentBookingForm, RoomBookingForm
from .models import EquipmentBooking, RoomBooking


def _add_validation_errors(form, error):
    """Copy model validation errors back to the form shown to the user."""
    for field, field_errors in error.message_dict.items():
        form_field = None if field == "__all__" else field
        for message in field_errors:
            form.add_error(form_field, message)


def _save_booking_form(form, resource_model):
    """Validate and save while the selected resource is locked."""
    booking = form.instance
    resource_field = booking.resource_field
    resource_id = getattr(booking, f"{resource_field}_id")
    try:
        resource = resource_model.objects.select_for_update().get(pk=resource_id)
    except resource_model.DoesNotExist:
        form.add_error(resource_field, "This resource is no longer available.")
        return False
    setattr(booking, resource_field, resource)

    try:
        booking.full_clean()
    except ValidationError as error:
        _add_validation_errors(form, error)
        return False

    booking.save()
    return True


@login_required
@permission_required(
    ("bookings.view_roombooking", "bookings.view_equipmentbooking"),
    raise_exception=True,
)
def booking_list(request):
    room_bookings = RoomBooking.objects.filter(user=request.user).select_related(
        "room"
    )
    equipment_bookings = EquipmentBooking.objects.filter(
        user=request.user
    ).select_related("equipment")
    return render(
        request,
        "bookings/booking_list.html",
        {
            "room_bookings": room_bookings,
            "equipment_bookings": equipment_bookings,
        },
    )


@login_required
@permission_required("bookings.add_roombooking", raise_exception=True)
def room_booking_create(request):
    booking = RoomBooking(user=request.user)
    initial = {"room": request.GET.get("room")} if request.GET.get("room") else None
    form = RoomBookingForm(request.POST or None, instance=booking, initial=initial)

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            if _save_booking_form(form, StudyRoom):
                messages.success(request, "Room booking request created.")
                return redirect("bookings:list")

    return render(
        request,
        "bookings/booking_form.html",
        {"form": form, "page_title": "Reserve a study room"},
    )


@login_required
@permission_required("bookings.add_equipmentbooking", raise_exception=True)
def equipment_booking_create(request):
    booking = EquipmentBooking(user=request.user)
    initial = (
        {"equipment": request.GET.get("equipment")}
        if request.GET.get("equipment")
        else None
    )
    form = EquipmentBookingForm(request.POST or None, instance=booking, initial=initial)

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            if _save_booking_form(form, EquipmentItem):
                messages.success(request, "Equipment booking request created.")
                return redirect("bookings:list")

    return render(
        request,
        "bookings/booking_form.html",
        {"form": form, "page_title": "Reserve equipment"},
    )


@login_required
@permission_required("bookings.view_roombooking", raise_exception=True)
def room_booking_update(request, pk):
    if request.method == "POST":
        with transaction.atomic():
            booking = get_object_or_404(
                RoomBooking.objects.select_for_update(),
                pk=pk,
                user=request.user,
                status=RoomBooking.Status.PENDING,
            )
            form = RoomBookingForm(request.POST, instance=booking)
            if form.is_valid() and _save_booking_form(form, StudyRoom):
                messages.success(request, "Room booking request updated.")
                return redirect("bookings:list")
    else:
        booking = get_object_or_404(
            RoomBooking,
            pk=pk,
            user=request.user,
            status=RoomBooking.Status.PENDING,
        )
        form = RoomBookingForm(instance=booking)

    return render(
        request,
        "bookings/booking_form.html",
        {"form": form, "page_title": "Edit room booking"},
    )


@login_required
@permission_required("bookings.view_equipmentbooking", raise_exception=True)
def equipment_booking_update(request, pk):
    if request.method == "POST":
        with transaction.atomic():
            booking = get_object_or_404(
                EquipmentBooking.objects.select_for_update(),
                pk=pk,
                user=request.user,
                status=EquipmentBooking.Status.PENDING,
            )
            form = EquipmentBookingForm(request.POST, instance=booking)
            if form.is_valid() and _save_booking_form(form, EquipmentItem):
                messages.success(request, "Equipment booking request updated.")
                return redirect("bookings:list")
    else:
        booking = get_object_or_404(
            EquipmentBooking,
            pk=pk,
            user=request.user,
            status=EquipmentBooking.Status.PENDING,
        )
        form = EquipmentBookingForm(instance=booking)

    return render(
        request,
        "bookings/booking_form.html",
        {"form": form, "page_title": "Edit equipment booking"},
    )


@require_POST
@login_required
@permission_required("bookings.view_roombooking", raise_exception=True)
def room_booking_cancel(request, pk):
    with transaction.atomic():
        booking = get_object_or_404(
            RoomBooking.objects.select_for_update(),
            pk=pk,
            user=request.user,
            status=RoomBooking.Status.PENDING,
        )
        booking.status = RoomBooking.Status.CANCELLED
        booking.save(update_fields=["status", "updated_at"])
    messages.success(request, "Room booking request cancelled.")
    return redirect("bookings:list")


@require_POST
@login_required
@permission_required("bookings.view_equipmentbooking", raise_exception=True)
def equipment_booking_cancel(request, pk):
    with transaction.atomic():
        booking = get_object_or_404(
            EquipmentBooking.objects.select_for_update(),
            pk=pk,
            user=request.user,
            status=EquipmentBooking.Status.PENDING,
        )
        booking.status = EquipmentBooking.Status.CANCELLED
        booking.save(update_fields=["status", "updated_at"])
    messages.success(request, "Equipment booking request cancelled.")
    return redirect("bookings:list")


@login_required
@permission_required(
    ("bookings.change_roombooking", "bookings.change_equipmentbooking"),
    raise_exception=True,
)
def booking_management(request):
    room_bookings = RoomBooking.objects.select_related("room", "user")
    equipment_bookings = EquipmentBooking.objects.select_related(
        "equipment", "user"
    )
    return render(
        request,
        "bookings/booking_management.html",
        {
            "room_bookings": room_bookings,
            "equipment_bookings": equipment_bookings,
        },
    )


def _change_booking_status(request, booking, action):
    statuses = {
        "approve": booking.Status.APPROVED,
        "reject": booking.Status.REJECTED,
    }
    if action not in statuses:
        return HttpResponseBadRequest("Unknown booking action.")
    if booking.status != booking.Status.PENDING:
        messages.error(request, "Only pending bookings can be changed.")
        return redirect("bookings:manage")

    booking.status = statuses[action]
    try:
        booking.full_clean()
    except ValidationError as error:
        messages.error(request, "; ".join(error.messages))
        return redirect("bookings:manage")

    booking.save(update_fields=["status", "updated_at"])
    messages.success(request, f"Booking {booking.get_status_display().lower()}.")
    return redirect("bookings:manage")


@require_POST
@login_required
@permission_required("bookings.change_roombooking", raise_exception=True)
def room_booking_status_update(request, pk, action):
    with transaction.atomic():
        booking = get_object_or_404(RoomBooking.objects.select_for_update(), pk=pk)
        booking.room = StudyRoom.objects.select_for_update().get(pk=booking.room_id)
        return _change_booking_status(request, booking, action)


@require_POST
@login_required
@permission_required("bookings.change_equipmentbooking", raise_exception=True)
def equipment_booking_status_update(request, pk, action):
    with transaction.atomic():
        booking = get_object_or_404(
            EquipmentBooking.objects.select_for_update(), pk=pk
        )
        booking.equipment = EquipmentItem.objects.select_for_update().get(
            pk=booking.equipment_id
        )
        return _change_booking_status(request, booking, action)
