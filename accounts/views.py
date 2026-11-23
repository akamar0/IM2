from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from .decorators import role_required
from .forms import RegistrationForm, UserProfileForm
from .models import User


def home(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard_redirect")
    return redirect("accounts:login")


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        messages.success(self.request, "Your UniFix account was created. You can now log in.")
        return super().form_valid(form)


class UniFixLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "The username or password you entered is incorrect.")
        return super().form_invalid(form)


@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("accounts:login")


@login_required
def dashboard_redirect(request):
    user = request.user
    role_to_url = {
        User.Role.UNIVERSITY_PERSONNEL: "accounts:personnel_dashboard",
        User.Role.IT_ADMIN: "accounts:it_admin_dashboard",
        User.Role.IT_TECHNICIAN: "accounts:technician_dashboard",
        User.Role.SYSTEM_ADMIN: "accounts:system_admin_dashboard",
    }
    if user.is_superuser:
        return redirect("accounts:system_admin_dashboard")
    return redirect(role_to_url.get(user.role, "accounts:personnel_dashboard"))


def render_dashboard(request, *, title, subtitle, cards, role_label):
    return render(request, "accounts/dashboard.html", {
        "dashboard_title": title,
        "dashboard_subtitle": subtitle,
        "dashboard_cards": cards,
        "role_label": role_label,
    })


@role_required(User.Role.UNIVERSITY_PERSONNEL)
def personnel_dashboard(request):
    return render_dashboard(
        request,
        title="Personnel Dashboard",
        subtitle="Your starting point for university IT support and equipment requests.",
        role_label="University Personnel",
        cards=[
            {"icon": "▣", "title": "Technical Support", "description": "Submit and follow up on reports about defective computers, monitors, printers, projectors, and other equipment.", "status": "Next development phase"},
            {"icon": "↗", "title": "Borrow Equipment", "description": "Request temporary use of available items such as HDMI cables, TV remotes, monitors, and projectors.", "status": "Next development phase"},
            {"icon": "◉", "title": "My Requests", "description": "Track request numbers, updates, approvals, and completion details in one place.", "status": "Next development phase"},
        ],
    )


@role_required(User.Role.IT_ADMIN)
def it_admin_dashboard(request):
    return render_dashboard(
        request,
        title="IT Support Administrator Dashboard",
        subtitle="Coordinate university support requests, technician assignments, and equipment borrowing.",
        role_label="IT Support Administrator",
        cards=[
            {"icon": "▤", "title": "Support Ticket Queue", "description": "Review, categorize, prioritize, and assign incoming technical support tickets.", "status": "Next development phase"},
            {"icon": "⇄", "title": "Borrowing Requests", "description": "Review equipment availability and approve or reject borrowing requests.", "status": "Next development phase"},
            {"icon": "▦", "title": "Equipment Records", "description": "Maintain equipment availability, condition, and maintenance history.", "status": "Next development phase"},
        ],
    )


@role_required(User.Role.IT_TECHNICIAN)
def technician_dashboard(request):
    return render_dashboard(
        request,
        title="IT Technician Dashboard",
        subtitle="View the work assigned to you and document technical resolutions.",
        role_label="IT Technician",
        cards=[
            {"icon": "⌁", "title": "Assigned Tickets", "description": "Review support issues assigned to you and update their progress.", "status": "Next development phase"},
            {"icon": "✓", "title": "Repair Records", "description": "Document inspections, troubleshooting steps, repairs, and final outcomes.", "status": "Next development phase"},
        ],
    )


@role_required(User.Role.SYSTEM_ADMIN)
def system_admin_dashboard(request):
    return render_dashboard(
        request,
        title="System Administrator Dashboard",
        subtitle="Manage UniFix accounts, assigned roles, and system-level settings.",
        role_label="System Administrator",
        cards=[
            {"icon": "♙", "title": "Account and Role Management", "description": "Create and maintain accounts and assign authorized UniFix roles.", "status": "Available in Django Admin"},
            {"icon": "⚙", "title": "System Administration", "description": "Use the protected Django administration site for authorized system configuration.", "status": "Available in Django Admin"},
        ],
        )


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"profile_user": request.user})


@login_required
def profile_edit_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit.html", {"form": form})
