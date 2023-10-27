from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from authentication.models import CustomUser, PasswordResetToken
from rest_framework_simplejwt.tokens import RefreshToken

class RegistrationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('registration')
        self.valid_registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }

    def test_register_user(self):
        response = self.client.post(self.registration_url, self.valid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.valid_login_data = {
            'username_or_email': 'testuser',
            'password': 'password123'
        }

    def test_user_login(self):
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PasswordResetRequestViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password_reset_request_url = reverse('password-reset-request')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.valid_reset_request_data = {
            'email': 'testuser@example.com'
        }

    def test_reset_request(self):
        response = self.client.post(self.password_reset_request_url, self.valid_reset_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PasswordResetConfirmViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password_reset_confirm_url = reverse('password-reset-confirm', args=['valid_token', '1'])
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.valid_reset_confirm_data = {
            'password': 'newpassword'
        }

    def test_reset_confirm(self):
        response = self.client.put(self.password_reset_confirm_url, self.valid_reset_confirm_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RefreshTokenViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.refresh_token_url = reverse('refresh-token')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.valid_refresh_data = {
            'refresh': str(self.refresh)
        }

    def test_refresh_token(self):
        response = self.client.post(self.refresh_token_url, self.valid_refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
