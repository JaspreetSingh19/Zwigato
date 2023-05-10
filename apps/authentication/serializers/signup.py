import re

from django.core.mail import send_mail
from rest_framework import serializers

from apps.authentication.models import User
from apps.common.constants import REGEX, OTP_LENGTH
from apps.common.messages.msg_validation import VALIDATION, MAX_LENGTH, MIN_LENGTH
from apps.common.utils import generate_otp


class SignupSerializer(serializers.ModelSerializer):
    """
    serializer for Registering requested user
    """
    first_name = serializers.CharField(
        max_length=MAX_LENGTH['first_name'], min_length=MIN_LENGTH['first_name'], required=True, allow_blank=False,
        trim_whitespace=True, error_messages=VALIDATION['first_name']
    )
    last_name = serializers.CharField(
        max_length=MAX_LENGTH['last_name'], min_length=MIN_LENGTH['last_name'], required=True, allow_blank=False,
        trim_whitespace=False, error_messages=VALIDATION['last_name']
    )
    username = serializers.CharField(
        min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'], required=True, allow_blank=False,
        trim_whitespace=False, error_messages=VALIDATION['username']
    )
    email = serializers.EmailField(
        required=True, allow_blank=False, error_messages=VALIDATION['email']
    )
    contact = serializers.CharField(
        min_length=MIN_LENGTH['contact'], max_length=MAX_LENGTH['contact'], required=True, allow_blank=False,
        error_messages=VALIDATION['contact']
    )
    password = serializers.CharField(
        write_only=True, min_length=MIN_LENGTH['password'], max_length=MAX_LENGTH['password'], allow_blank=False,
        error_messages=VALIDATION['password']
    )

    @staticmethod
    def validate_first_name(value):
        """
        check that the first_name should contain only alphabets
        :param value:first_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["first_name"], value):
            raise serializers.ValidationError(VALIDATION['first_name']['invalid'])
        return value

    @staticmethod
    def validate_last_name(value):
        """
        check that the last_name should contain only alphabets
        :param value:last_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["last_name"], value):
            raise serializers.ValidationError(VALIDATION['last_name']['invalid'])
        return value

    @staticmethod
    def validate_username(value):
        """
        check that the username length is from 8 to 16 characters,
        and it is alphanumeric with at least one special character
        :param value: username
        :return: if valid return value ,else return Validation error
        """
        if not re.match(REGEX["USERNAME"], value) or not any(char.isalpha() for char in value):
            raise serializers.ValidationError(VALIDATION['username']['invalid'])
        return value

    @staticmethod
    def validate_contact(value):
        """
        check that the contact should contain only digits
        :param value:contact
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["contact"], value):
            raise serializers.ValidationError(VALIDATION['contact']['invalid'])
        return value

    @staticmethod
    def validate_password(value):
        """
        checks password if valid : return value,
        else : return validation error
        """
        if not re.match(REGEX["PASSWORD"], value):
            raise serializers.ValidationError(VALIDATION['password']['invalid'])
        return value

    # pylint: disable=too-few-public-methods
    def create(self, validated_data):
        """
        creates a user
        """
        email_otp = generate_otp(OTP_LENGTH)
        user = User.objects.create(email_otp=email_otp, **validated_data)
        user.set_password(validated_data['password'])
        user.save()
        send_mail(
            'Welcome to Zwigato',
            f'Hi {user.first_name},\n this is your registered username: {user.username} \n'
            f'  This is your otp for email verification :\n {email_otp} \n',
            'projectgallery5@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return user

    class Meta:
        """
        class Meta for SignupSerializer
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'contact', 'password']
