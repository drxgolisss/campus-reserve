from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from resources.models import EquipmentItem, StudyRoom


class Booking(models.Model):
    """Fields and validation shared by both booking types."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    resource_field = None

    class Meta:
        abstract = True
        ordering = ["-start_time"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(start_time__lt=models.F("end_time")),
                name="%(app_label)s_%(class)s_valid_time_range",
            )
        ]

    def clean(self):
        super().clean()
        errors = {}

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            errors["end_time"] = "End time must be later than start time."

        resource_id = getattr(self, f"{self.resource_field}_id", None)
        if resource_id:
            resource = getattr(self, self.resource_field)
            if (
                self.status in {self.Status.PENDING, self.Status.APPROVED}
                and not resource.is_active
            ):
                errors[self.resource_field] = "This resource is not available."

        if (
            resource_id
            and self.start_time
            and self.end_time
            and self.start_time < self.end_time
            and self.status in {self.Status.PENDING, self.Status.APPROVED}
        ):
            overlapping = type(self).objects.filter(
                **{f"{self.resource_field}_id": resource_id},
                status__in=[self.Status.PENDING, self.Status.APPROVED],
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            ).exclude(pk=self.pk)

            if overlapping.exists():
                errors["__all__"] = (
                    "This resource already has a booking during the selected time."
                )

        if errors:
            raise ValidationError(errors)


class RoomBooking(Booking):
    resource_field = "room"

    room = models.ForeignKey(
        StudyRoom,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    def __str__(self):
        return f"{self.room} — {self.start_time:%Y-%m-%d %H:%M}"


class EquipmentBooking(Booking):
    resource_field = "equipment"

    equipment = models.ForeignKey(
        EquipmentItem,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    def __str__(self):
        return f"{self.equipment} — {self.start_time:%Y-%m-%d %H:%M}"
