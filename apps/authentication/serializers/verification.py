from rest_framework import serializers

from apps.authentication.models import User
from apps.common.messages.msg_validation import VALIDATION


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages=VALIDATION['email'])
    email_otp = serializers.IntegerField(required=True, error_messages=VALIDATION['email_otp'])

    def validate(self, attrs):
        """
        Check if the OTP is correct for the given email
        and delete the OTP from the database if it matches
        """
        try:
            user = User.objects.get(email=attrs['email'])
            if user.email_otp == attrs['email_otp']:
                user.is_email_verified = True
                user.email_otp = None  # delete the OTP from the database
                user.save()
            else:
                raise serializers.ValidationError("Invalid OTP")
        except User.DoesNotExist:
            raise serializers.ValidationError("Email does not exist")
        return attrs

    def create(self, validated_data):
        return validated_data
