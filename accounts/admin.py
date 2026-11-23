from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UniFixUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("UniFix role and contact details", {"fields": ("role", "department", "contact_number")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("UniFix role and contact details", {"fields": ("role", "department", "contact_number", "email")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "department", "is_active")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "department")
