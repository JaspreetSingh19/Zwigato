import re

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import User
from apps.common.constants import REGEX
from apps.common.messages.msg_validation import MIN_LENGTH, MAX_LENGTH, VALIDATION


class LoginSerializer(serializers.ModelSerializer):
    """
    used to verify the login credentials and return the login response
    """
    username = serializers.CharField(
        min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'], required=True, allow_blank=False,
        trim_whitespace=False, error_messages=VALIDATION['username']
    )
    password = serializers.CharField(
        min_length=MIN_LENGTH['password'], max_length=MAX_LENGTH['password'], write_only=True, required=True,
        trim_whitespace=False, error_messages=VALIDATION['password']
    )

    @staticmethod
    def validate_username(value):
        """
        Check that the username is alphanumeric with at least one special character
        """
        if not re.match(REGEX["username"], value):
            raise serializers.ValidationError(VALIDATION['username']['invalid'])
        return value

    @staticmethod
    def validate_password(value):
        """
        Check that the password is valid
        """
        if not re.match(REGEX["password"], value):
            raise serializers.ValidationError(VALIDATION['password']['invalid'])
        return value

    def validate(self, attrs):
        """
        Validate if the username and password are correct
        """
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(VALIDATION['invalid credentials'])

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """
        Generate the access and refresh tokens for the authenticated user
        """
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)

        user_token = User.objects.get(id=user.id)
        user_token.token = str(refresh.access_token)
        user_token.save()

        role = user.role

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': str(role),
        }

    class Meta:
        """
        Class Meta for SigninSerializer
        """
        model = User
        fields = ['username', 'password']


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout
    It blacklisted the refresh token after
    the authenticated user is logged-out
    """
    refresh = serializers.CharField(max_length=255)

    def validate(self, attrs):
        """
        Validate the refresh token from the user
        :param attrs: refresh
        :return: attrs
        """
        try:
            token = RefreshToken(attrs['refresh'])
            token_type = token.__class__.__name__
            if token_type != 'RefreshToken':
                raise serializers.ValidationError(VALIDATION['Invalid'])
            attrs['refresh_token'] = token
        except (InvalidToken, TokenError) as e:
            raise serializers.ValidationError(str(e))
        return attrs

    def create(self, validated_data):
        """
        Override create method to add refresh token
        to blacklist
        :param validated_data: refresh
        :return: success and error message
        """
        refresh_token = self.validated_data['refresh_token']
        refresh_token.blacklist()
        return {'success': True}

