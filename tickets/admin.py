from django.contrib import admin
from .models import SupportTicket, TicketUpdate


class TicketUpdateInline(admin.TabularInline):
    model = TicketUpdate
    extra = 0
    readonly_fields = ("author", "message", "status_snapshot", "created_at")
    can_delete = False


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_number", "subject", "created_by", "assigned_to",
        "priority", "status", "created_at",
    )
    list_filter = ("status", "priority", "category", "created_at")
    search_fields = ("ticket_number", "subject", "equipment_name", "created_by__username", "created_by__email")
    readonly_fields = ("ticket_number", "created_by", "department", "created_at", "updated_at", "resolved_at")
    inlines = (TicketUpdateInline,)


@admin.register(TicketUpdate)
class TicketUpdateAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author", "status_snapshot", "created_at")
    list_filter = ("status_snapshot", "created_at")
    search_fields = ("ticket__ticket_number", "message", "author__username")
    readonly_fields = ("ticket", "author", "message", "status_snapshot", "created_at")
