from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True,
                                     write_only=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

# to get list of all users (admin's right)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(TokenObtainPairSerializer):
    ...
    # Use email for authentication instead of username
    # def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
    #     email = attrs.get('email')
    #     password = attrs.get('password')

    #     if not email or not password:
    #         raise AuthenticationFailed('Email and password are required')
        
    #             # Authenticate the user using email and password
    #     user = authenticate(request=self.context.get('request'), email=email, password=password)

    #     if not user:
    #         raise AuthenticationFailed('No active account found with the given credentials')

    #     if not user.is_active:
    #         raise AuthenticationFailed('This account is inactive')

    #     # Override attrs to match expected fields in TokenObtainPairSerializer
    #     # attrs['username'] = user.email  # Simulate username field for token generation

    #     return super().validate(attrs)


class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True,
                                            write_only=True,
                                            max_length=255)
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class DeleteUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, 
                                   required=True)