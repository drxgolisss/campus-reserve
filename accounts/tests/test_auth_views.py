import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class AuthenticationViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="student",
            email="student@example.com",
            password="test-password-123",
        )

    def test_login_page_is_available(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_user_can_log_in_and_continue_to_requested_page(self):
        response = self.client.post(
            f"{reverse('login')}?next={reverse('resources:room-list')}",
            {
                "username": self.user.username,
                "password": "test-password-123",
            },
        )

        self.assertRedirects(
            response,
            reverse("resources:room-list"),
            fetch_redirect_response=False,
        )

    def test_invalid_credentials_show_an_error(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password")

    def test_authenticated_user_can_log_out_with_post(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("core:home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_password_reset_sends_email_for_known_address(self):
        response = self.client.post(
            reverse("password_reset"),
            {"email": self.user.email},
        )

        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/accounts/reset/", mail.outbox[0].body)
        self.assertIn(self.user.username, mail.outbox[0].body)

    def test_user_can_set_a_new_password_from_reset_link(self):
        self.client.post(
            reverse("password_reset"),
            {"email": self.user.email},
        )
        reset_url = re.search(
            r"http://testserver(/accounts/reset/\S+)",
            mail.outbox[0].body,
        ).group(1)

        token_response = self.client.get(reset_url)
        response = self.client.post(
            token_response.url,
            {
                "new_password1": "new-test-password-456",
                "new_password2": "new-test-password-456",
            },
        )

        self.assertRedirects(response, reverse("password_reset_complete"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new-test-password-456"))

    def test_password_reset_does_not_reveal_unknown_address(self):
        response = self.client.post(
            reverse("password_reset"),
            {"email": "unknown@example.com"},
        )

        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)
