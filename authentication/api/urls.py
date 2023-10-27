"""URL configuration for user authentication endpoints."""
from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    RefreshTokenView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)

# pylint: disable=C0103
app_name = 'authentication'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset'),
    path(
        'reset-password/<str:token>/<str:user_id>/',
        PasswordResetConfirmView.as_view(),
        name='password-reset-confirm'),
        path('login/', LoginView.as_view(),
        name='login'
    ),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
