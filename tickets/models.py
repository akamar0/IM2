import uuid

from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils import timezone


class SupportTicket(models.Model):
    """A university personnel report about an IT/equipment problem."""

    class Category(models.TextChoices):
        HARDWARE = "HARDWARE", "Hardware"
        SOFTWARE = "SOFTWARE", "Software"
        NETWORK = "NETWORK", "Network / Internet"
        PRINTER = "PRINTER", "Printer"
        OTHER = "OTHER", "Other"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        NORMAL = "NORMAL", "Normal"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACKNOWLEDGED = "ACKNOWLEDGED", "Acknowledged"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"
        REJECTED = "REJECTED", "Rejected"

    ticket_number = models.CharField(max_length=24, unique=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="support_tickets",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_support_tickets",
        null=True,
        blank=True,
        limit_choices_to={"role": "TECHNICIAN", "is_active": True},
    )
    department = models.CharField(max_length=120, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    equipment_name = models.CharField(max_length=120)
    subject = models.CharField(max_length=160)
    description = models.TextField(validators=[MinLengthValidator(15)])
    attachment = models.ImageField(upload_to="ticket_attachments/%Y/%m/", blank=True, null=True)
    priority = models.CharField(max_length=12, choices=Priority.choices, default=Priority.NORMAL)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("status", "created_at"), name="ticket_status_created_idx"),
            models.Index(fields=("created_by", "created_at"), name="ticket_owner_created_idx"),
            models.Index(fields=("assigned_to", "status"), name="ticket_assignee_status_idx"),
        ]

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            date_part = timezone.localdate().strftime("%Y%m%d")
            self.ticket_number = f"UF-{date_part}-{uuid.uuid4().hex[:8].upper()}"
        if self.status == self.Status.RESOLVED and self.resolved_at is None:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        attachment = self.attachment
        super().delete(*args, **kwargs)
        if attachment:
            attachment.delete(save=False)

    def __str__(self):
        return f"{self.ticket_number} – {self.subject}"

    @property
    def can_be_edited_by_reporter(self):
        return self.status == self.Status.PENDING


class TicketUpdate(models.Model):
    """A chronological update visible to users who can access the ticket."""

    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="updates")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="ticket_updates",
    )
    message = models.TextField(validators=[MinLengthValidator(3), MaxLengthValidator(1000)])
    status_snapshot = models.CharField(max_length=16, choices=SupportTicket.Status.choices, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Update for {self.ticket.ticket_number} by {self.author}"
