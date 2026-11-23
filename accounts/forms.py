from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    """Public registration form. Public users cannot choose privileged roles."""

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "department",
            "contact_number",
        )
        labels = {
            "first_name": "First name",
            "last_name": "Last name",
            "department": "Department / Office",
            "contact_number": "Contact number",
        }
        widgets = {
            "username": forms.TextInput(attrs={"autocomplete": "username", "placeholder": "Choose a username"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "name@example.com"}),
            "department": forms.TextInput(attrs={"placeholder": "Your department or office"}),
            "contact_number": forms.TextInput(attrs={"placeholder": "Optional contact number"}),
        }

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("That username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        # Never accept a role from the public registration form.
        user.role = User.Role.UNIVERSITY_PERSONNEL
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "department", "contact_number")
        labels = {
            "first_name": "First name",
            "last_name": "Last name",
            "department": "Department / Office",
            "contact_number": "Contact number",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com"}),
            "department": forms.TextInput(attrs={"placeholder": "Department or office"}),
            "contact_number": forms.TextInput(attrs={"placeholder": "Contact number"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        existing = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError("Another account is already using this email address.")
        return email
