import re

from rest_framework import serializers

from apps.common.constants import REGEX
from apps.common.messages.msg_validation import VALIDATION


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset password serializer to validate the password and if it
    is validated then save the new password with the old one in the database
    """
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(VALIDATION['password']['do_not_match'])

        return attrs

    @staticmethod
    def validate_new_password(value):
        """
        checks password if valid : return value,
        else : return validation error
        """
        if not re.match(REGEX["password"], value):
            raise serializers.ValidationError(VALIDATION['password']['invalid'])
        return value

    def create(self, validated_data):
        user = self.context.get('user')
        user.set_password(validated_data['new_password'])
        user.save()

        return user
