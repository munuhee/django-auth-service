"""Module for User Serializer in the authentication app."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

# pylint: disable=R0903
class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        """Meta options for the UserSerializer."""
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            }
        }
# pylint: disable=W0223,R0903
class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for PasswordReset model"""  
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    # pylint: disable=W0237
    def validate(self, data):
        """Check if the passwords match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
