from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """UniFix user with an assigned university support role."""

    class Role(models.TextChoices):
        UNIVERSITY_PERSONNEL = "PERSONNEL", "University Personnel"
        IT_ADMIN = "IT_ADMIN", "IT Support Administrator"
        IT_TECHNICIAN = "TECHNICIAN", "IT Technician"
        SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Administrator"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.UNIVERSITY_PERSONNEL,
    )
    department = models.CharField(max_length=120, blank=True)
    contact_number = models.CharField(max_length=30, blank=True)

    def save(self, *args, **kwargs):
        # Normalize email addresses so case differences do not create duplicates.
        if self.email:
            self.email = self.email.strip().lower()
        if self.is_superuser:
            self.role = self.Role.SYSTEM_ADMIN
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return self.get_full_name().strip() or self.username

    def __str__(self):
        return f"{self.display_name} ({self.get_role_display()})"
