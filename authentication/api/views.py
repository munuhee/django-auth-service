"""Module for handling user registration, password reset, and token refresh."""
import os

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import generics, status

from authentication.models import PasswordResetToken, CustomUser

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, PasswordResetConfirmSerializer

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    """View for user registration."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """create user an send email on successful registration"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        password = make_password(validated_data['password'])

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password
        )

        # Send a registration success email
        send_mail(
            'Registration Successful',
            'Thank you for registering with us!',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        response_data = UserSerializer(user).data
        return Response(response_data, status=status.HTTP_201_CREATED)

class LoginView(generics.CreateAPIView):
    """View for user login."""
    serializer_class = UserSerializer
    def create(self, request):
        """Authenticates the user and returns an access token."""
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return Response({
                'detail': 'Username is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate the user using username
        user = None
        user = authenticate(username=username, password=password)

        # Debugging statement
        print(f"Authenticated User: {user}")

        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'detail': 'Login successful',
            'access': access_token,
            })

class PasswordResetRequestView(generics.CreateAPIView):
    """View for generating a password reset token and sending a reset email."""
    serializer_class = UserSerializer

    def create(self, request):
        """
        Creates a password reset token and sends a reset email
         to the user's email address.
        """
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned:
            return Response(
                {'detail': 'Multiple users with the same email. Contact support.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reset_token = default_token_generator.make_token(user)
        expiration_time = timezone.now() + timezone.timedelta(hours=1)

        reset_token_instance = PasswordResetToken(
            user=user, token=reset_token,
            expires_at=expiration_time
        )
        reset_token_instance.save()

        current_site = get_current_site(request)

        reset_url = reverse(
            'authentication:password-reset-confirm',
            args=[reset_token, str(user.id)]
        )

        # Build the complete reset URL
        protocol = 'http' if not request.is_secure() else 'https'
        reset_url = f"{protocol}://{current_site.domain}{reset_url}"

        context = {
            'user': user,
            'token': reset_token,
            'reset_url': reset_url,
        }

        subject = 'Password Reset Request'

        html_content = render_to_string('authentication/password_reset_email.html', context)

        text_content = f"Click the following link to reset your password: {reset_url}"

        email_subject = subject
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]
        msg = EmailMultiAlternatives(email_subject, text_content, from_email, to_email)

        msg.attach_alternative(html_content, "text/html")

        msg.send()

        return Response(
            {'detail': 'Password reset email sent successfully.'},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(generics.UpdateAPIView):
    """View for verifying the reset token and resetting the user's password."""
    serializer_class = PasswordResetConfirmSerializer

    def update(self, request, **kwargs):
        """Verifies the reset token and updates the user's password if valid."""
        token = kwargs.get('token')
        user_id = kwargs.get('user_id')
        password = request.data.get('password')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            print(f"User not found for user_id: {user_id}")
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            PasswordResetToken.objects.filter(user=user).delete()

            return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(generics.CreateAPIView):
    """View for refreshing access tokens."""
    def post(self, request):
        """Generate a new access token using a refresh token."""
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token})
        except Exception as e:
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
