from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User
from .models import SupportTicket


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ("category", "equipment_name", "subject", "description", "attachment")
        labels = {
            "category": "Issue category",
            "equipment_name": "Affected equipment / system",
            "subject": "Short issue title",
            "description": "Describe the problem",
            "attachment": "Photo evidence (optional)",
        }
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "equipment_name": forms.TextInput(attrs={"placeholder": "e.g. Office desktop computer"}),
            "subject": forms.TextInput(attrs={"placeholder": "e.g. Computer will not turn on"}),
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "Explain what happened, when it started, and any steps already tried."}),
            "attachment": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def clean_equipment_name(self):
        value = self.cleaned_data["equipment_name"].strip()
        if len(value) < 2:
            raise ValidationError("Enter the name of the affected equipment or system.")
        return value

    def clean_subject(self):
        value = self.cleaned_data["subject"].strip()
        if len(value) < 5:
            raise ValidationError("The issue title must contain at least 5 characters.")
        return value

    def clean_description(self):
        value = self.cleaned_data["description"].strip()
        if len(value) < 15:
            raise ValidationError("Please provide at least 15 characters so IT Support can understand the issue.")
        return value

    def clean_attachment(self):
        attachment = self.cleaned_data.get("attachment")
        if attachment and attachment.size > 5 * 1024 * 1024:
            raise ValidationError("The image must be 5 MB or smaller.")
        return attachment


class TicketAdminUpdateForm(forms.ModelForm):
    update_message = forms.CharField(
        required=False,
        min_length=3,
        max_length=1000,
        label="Update for the reporter (optional)",
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Add an assignment or progress note visible to the reporter."}),
    )

    class Meta:
        model = SupportTicket
        fields = (
            "category", "equipment_name", "subject", "description", "attachment",
            "priority", "status", "assigned_to", "resolution_notes",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "resolution_notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Enter the final resolution when marking the ticket resolved."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = User.objects.filter(
            role=User.Role.IT_TECHNICIAN,
            is_active=True,
        ).order_by("first_name", "last_name", "username")
        self.fields["assigned_to"].required = False
        self.fields["assigned_to"].label = "Assign to technician"

    def clean_attachment(self):
        attachment = self.cleaned_data.get("attachment")
        if attachment and attachment.size > 5 * 1024 * 1024:
            raise ValidationError("The image must be 5 MB or smaller.")
        return attachment

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("status") == SupportTicket.Status.RESOLVED and not (cleaned.get("resolution_notes") or "").strip():
            self.add_error("resolution_notes", "Resolution notes are required before marking a ticket as resolved.")
        if cleaned.get("assigned_to") and cleaned.get("status") == SupportTicket.Status.PENDING:
            cleaned["status"] = SupportTicket.Status.ACKNOWLEDGED
        return cleaned


class TicketTechnicianUpdateForm(forms.ModelForm):
    update_message = forms.CharField(
        label="Work update",
        min_length=5,
        max_length=1000,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Describe the inspection, troubleshooting, or repair performed."}),
    )

    class Meta:
        model = SupportTicket
        fields = ("status", "resolution_notes")
        widgets = {
            "resolution_notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Required when marking the ticket as resolved."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = [
            (SupportTicket.Status.ACKNOWLEDGED, "Acknowledged"),
            (SupportTicket.Status.IN_PROGRESS, "In Progress"),
            (SupportTicket.Status.RESOLVED, "Resolved"),
        ]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("status") == SupportTicket.Status.RESOLVED and not (cleaned.get("resolution_notes") or "").strip():
            self.add_error("resolution_notes", "Add resolution notes before resolving this ticket.")
        return cleaned
