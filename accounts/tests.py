from django.test import TestCase
from django.urls import reverse
from .models import User


class AccountFeatureTests(TestCase):
    def test_registration_creates_personnel_and_hashes_password(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "newstaff",
            "first_name": "New",
            "last_name": "Staff",
            "email": "NEWSTAFF@example.com",
            "department": "Registrar",
            "contact_number": "09123456789",
            "password1": "A-Strong-Test-Password-2026!",
            "password2": "A-Strong-Test-Password-2026!",
        })
        self.assertRedirects(response, reverse("accounts:login"))
        user = User.objects.get(username="newstaff")
        self.assertEqual(user.role, User.Role.UNIVERSITY_PERSONNEL)
        self.assertEqual(user.email, "newstaff@example.com")
        self.assertTrue(user.check_password("A-Strong-Test-Password-2026!"))
        self.assertNotEqual(user.password, "A-Strong-Test-Password-2026!")

    def test_logged_out_user_is_sent_to_login_for_profile(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:profile')}")

    def test_personnel_cannot_open_it_admin_dashboard(self):
        user = User.objects.create_user(username="personnel", password="A-Strong-Test-Password-2026!")
        self.client.login(username="personnel", password="A-Strong-Test-Password-2026!")
        response = self.client.get(reverse("accounts:it_admin_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_user_can_only_edit_their_own_profile_route(self):
        user = User.objects.create_user(username="profileuser", password="A-Strong-Test-Password-2026!")
        self.client.login(username="profileuser", password="A-Strong-Test-Password-2026!")
        response = self.client.get(reverse("accounts:profile_edit"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "profileuser")
