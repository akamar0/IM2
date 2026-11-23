from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.UniFixLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_redirect, name="dashboard_redirect"),
    path("dashboard/personnel/", views.personnel_dashboard, name="personnel_dashboard"),
    path("dashboard/it-admin/", views.it_admin_dashboard, name="it_admin_dashboard"),
    path("dashboard/technician/", views.technician_dashboard, name="technician_dashboard"),
    path("dashboard/system-admin/", views.system_admin_dashboard, name="system_admin_dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
]
