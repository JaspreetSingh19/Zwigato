from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.authentication.models import ForgetPassword
from apps.authentication.serializers.reset_password import ResetPasswordSerializer
from apps.common.constants import PASSWORD_RESET_TIME


class ResetPasswordViewSet(viewsets.ViewSet):
    """
    View to handle resetting the user's password
    """
    serializer_class = ResetPasswordSerializer

    def create(self, request, token):
        """
        Create method to reset the new password by replacing the old
        password and verifying the token.
        :param request: new password
        :param token: forget password token
        :return: data
        """
        try:
            password_reset_token = ForgetPassword.objects.get(forget_password_token=token)
        except ForgetPassword.DoesNotExist:
            return Response({'error': 'Invalid token.'},
                            status=status.HTTP_400_BAD_REQUEST)

        time_difference = timezone.now() - password_reset_token.created_at
        if time_difference.total_seconds() > PASSWORD_RESET_TIME:
            password_reset_token.delete()
            return Response({'error': 'Token expired.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = password_reset_token.user
        serializer = self.serializer_class(
            data=request.data, context={'user': user}
        )
        if serializer.is_valid():
            serializer.save()
            password_reset_token.delete()
            return Response(
                {'success': 'Password reset successfully.'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Password reset failed.'},
            status=status.HTTP_400_BAD_REQUEST
        )
