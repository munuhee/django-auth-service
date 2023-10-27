from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_registration(self):
        response = self.client.post(reverse("registration"), self.user_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "testpassword"}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_request(self):
        response = self.client.post(reverse("password-reset-request"), {"email": "test@example.com"}, format="json")
        self.assertEqual(response.status_code, 200)
