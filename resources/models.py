from django.core.validators import MinValueValidator
from django.db import models


class StudyRoom(models.Model):
    """A university room that students will be able to reserve."""

    name = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["building", "room_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["building", "room_number"],
                name="unique_room_per_building",
            ),
            models.CheckConstraint(
                condition=models.Q(capacity__gte=1),
                name="room_capacity_at_least_one",
            ),
        ]

    def __str__(self):
        return f"{self.building} {self.room_number} — {self.name}"


class EquipmentItem(models.Model):
    """A single inventory item that students will be able to reserve."""

    class Category(models.TextChoices):
        LAPTOP = "laptop", "Laptop"
        PROJECTOR = "projector", "Projector"
        CAMERA = "camera", "Camera"
        AUDIO = "audio", "Audio equipment"
        LAB_DEVICE = "lab_device", "Laboratory device"
        OTHER = "other", "Other"

    class Condition(models.TextChoices):
        EXCELLENT = "excellent", "Excellent"
        GOOD = "good", "Good"
        FAIR = "fair", "Fair"
        MAINTENANCE = "maintenance", "Under maintenance"

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=Category.choices)
    inventory_code = models.CharField(max_length=30, unique=True)
    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.GOOD,
    )
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "inventory_code"]

    def __str__(self):
        return f"{self.name} ({self.inventory_code})"
