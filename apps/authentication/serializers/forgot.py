from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.authentication.models import ForgetPassword, User
from apps.common.constants import FP_TOKEN_LENGTH
from apps.common.messages.msg_validation import VALIDATION
from apps.common.utils import generate_otp


class ForgetPasswordSerializer(serializers.ModelSerializer):
    """
    forget password serializer to verify the email of the user
    and send the mail to its register email.
    """
    email = serializers.EmailField()

    @staticmethod
    def validate_email(email):
        """
        Validate the user's email using Django's PasswordResetForm
        """
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(VALIDATION['email']['does_not_exists'])

        PasswordResetForm({'email': email})

        return email

    def create(self, validated_data):
        """
        Generate a password reset token and URL for the user
        :param validated_data: email
        :return: validated data
        """
        request = self.context.get('request')
        user = User.objects.get(email=validated_data['email'])
        token = generate_otp(FP_TOKEN_LENGTH)
        reset_url = request.build_absolute_uri(
            reverse('reset_password-list', kwargs={'token': token})
        )

        ForgetPassword.objects.update_or_create(
            user=user,
            forget_password_token=token,
        )
        send_mail(
            'Password Reset Request',
            f'Please follow this link to reset your password: {reset_url}',
            'projectgalleria5@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return validated_data

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Class meta to define the model and the field
        of that model.
        """
        model = User
        fields = ['email']
