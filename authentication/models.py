"""
Django Authentication Models and Managers

This module defines custom Django authentication models and managers
for handling user authentication and password reset tokens.

Classes:
- CaseInsensitiveUserManager: Custom User Manager that handles
  case-insensitive usernames and emails.
- CustomUser: Custom User model with email as the unique identifier.
- EmailBackend: Authentication backend for email or username login.
- PasswordResetToken: Model to store password reset tokens for users.
"""
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# pylint: disable=R0903
class CaseInsensitiveUserManager(UserManager):
    """Custom User Manager that handles case-insensitive usernames and emails."""
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Create a regular user with optional email and password."""
        if not email:
            email = self.normalize_email(username)
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # pylint: disable=W0222
    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create a superuser with admin privileges."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)

# pylint: disable=R0903
class CustomUser(AbstractUser):
    """Custom User model with email as the unique identifier."""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    class Meta:
        """Meta option for the app label"""
        app_label = 'authentication'

    objects = CaseInsensitiveUserManager()

# pylint: disable=R0903
class PasswordResetToken(models.Model):
    """Model to store password reset tokens for users."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    def __str__(self):
        """Return a string representation of the password reset token."""
        return f"Password reset token for {self.user}"
