"""Module containing test cases for the CustomUser model in the authentication app."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import CustomUser

class CustomUserTests(TestCase):
    """Test case class for the CustomUser model in the authentication app"""
    def setUp(self):
        """Set up the test client and create a user for testing."""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Test creating a new user."""
        user_data = {
            'username': 'testperson',
            'email': 'testperson@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('authentication:register'), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        """Test user login."""
        response = self.client.post(
            reverse('authentication:login'),
            {'username': 'testuser', 'password': 'testpassword'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_request(self):
        """Test password reset request."""
        response = self.client.post(
            reverse('authentication:password-reset'),
            {'email': 'testuser@example.com'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm(self):
        """Test password reset confirmation with an invalid token."""
        token = 'some_valid_token'
        user_id = str(self.user.id)
        response = self.client.put(
            reverse('authentication:password-reset-confirm',
            args=(token, user_id)),
            {'password': 'newpassword'},
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
