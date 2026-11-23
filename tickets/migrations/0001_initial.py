import django.core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SupportTicket",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ticket_number", models.CharField(editable=False, max_length=24, unique=True)),
                ("department", models.CharField(blank=True, max_length=120)),
                ("category", models.CharField(choices=[("HARDWARE", "Hardware"), ("SOFTWARE", "Software"), ("NETWORK", "Network / Internet"), ("PRINTER", "Printer"), ("OTHER", "Other")], max_length=20)),
                ("equipment_name", models.CharField(max_length=120)),
                ("subject", models.CharField(max_length=160)),
                ("description", models.TextField(validators=[django.core.validators.MinLengthValidator(15)])),
                ("attachment", models.ImageField(blank=True, null=True, upload_to="ticket_attachments/%Y/%m/")),
                ("priority", models.CharField(choices=[("LOW", "Low"), ("NORMAL", "Normal"), ("HIGH", "High"), ("URGENT", "Urgent")], default="NORMAL", max_length=12)),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("ACKNOWLEDGED", "Acknowledged"), ("IN_PROGRESS", "In Progress"), ("RESOLVED", "Resolved"), ("CLOSED", "Closed"), ("REJECTED", "Rejected")], default="PENDING", max_length=16)),
                ("resolution_notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("resolved_at", models.DateTimeField(blank=True, null=True)),
                ("assigned_to", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="assigned_support_tickets", to=settings.AUTH_USER_MODEL, limit_choices_to={"role": "TECHNICIAN", "is_active": True})),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="support_tickets", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="TicketUpdate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message", models.TextField(validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(1000)])),
                ("status_snapshot", models.CharField(blank=True, choices=[("PENDING", "Pending"), ("ACKNOWLEDGED", "Acknowledged"), ("IN_PROGRESS", "In Progress"), ("RESOLVED", "Resolved"), ("CLOSED", "Closed"), ("REJECTED", "Rejected")], max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="ticket_updates", to=settings.AUTH_USER_MODEL)),
                ("ticket", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="updates", to="tickets.supportticket")),
            ],
            options={"ordering": ("created_at",)},
        ),
        migrations.AddIndex(
            model_name="supportticket",
            index=models.Index(fields=["status", "created_at"], name="ticket_status_created_idx"),
        ),
        migrations.AddIndex(
            model_name="supportticket",
            index=models.Index(fields=["created_by", "created_at"], name="ticket_owner_created_idx"),
        ),
        migrations.AddIndex(
            model_name="supportticket",
            index=models.Index(fields=["assigned_to", "status"], name="ticket_assignee_status_idx"),
        ),
    ]
