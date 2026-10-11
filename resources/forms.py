from django import forms

from .models import EquipmentItem, StudyRoom


class RoomFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs={"placeholder": "Name, building, or room number"}
        ),
    )
    building = forms.ChoiceField(required=False, label="Building")
    min_capacity = forms.IntegerField(
        required=False,
        min_value=1,
        label="Minimum capacity",
        widget=forms.NumberInput(attrs={"min": 1, "placeholder": "Any"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        buildings = (
            StudyRoom.objects.filter(is_active=True)
            .order_by("building")
            .values_list("building", flat=True)
            .distinct()
        )
        self.fields["building"].choices = [
            ("", "All buildings"),
            *((building, building) for building in buildings),
        ]


class EquipmentFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs={"placeholder": "Name, inventory code, or location"}
        ),
    )
    category = forms.ChoiceField(
        required=False,
        label="Category",
        choices=[("", "All categories"), *EquipmentItem.Category.choices],
    )
    condition = forms.ChoiceField(
        required=False,
        label="Condition",
        choices=[("", "Any condition"), *EquipmentItem.Condition.choices],
    )
