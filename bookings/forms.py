from django import forms

from resources.models import EquipmentItem, StudyRoom

from .models import EquipmentBooking, RoomBooking


class BookingForm(forms.ModelForm):
    """Shared form settings for room and equipment bookings."""

    class Meta:
        fields = ("start_time", "end_time", "comment")
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M"]


class RoomBookingForm(BookingForm):
    class Meta(BookingForm.Meta):
        model = RoomBooking
        fields = ("room", *BookingForm.Meta.fields)
        widgets = BookingForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["room"].queryset = StudyRoom.objects.filter(is_active=True)


class EquipmentBookingForm(BookingForm):
    class Meta(BookingForm.Meta):
        model = EquipmentBooking
        fields = ("equipment", *BookingForm.Meta.fields)
        widgets = BookingForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["equipment"].queryset = EquipmentItem.objects.filter(
            is_active=True
        )

