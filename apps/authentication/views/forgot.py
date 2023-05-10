from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.authentication.models import User
from apps.authentication.serializers.forgot import ForgetPasswordSerializer
from apps.common.messages.msg_app import SUCCESS_MESSAGES, ERROR_MESSAGES


class ForgotPasswordView(viewsets.ModelViewSet):
    """
    View to perform send mail operation with a
    link attached to it to reset password
    """
    serializer_class = ForgetPasswordSerializer
    queryset = User

    def get_queryset(self):
        return User.objects.filter(email='email').first()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(
                {'message': SUCCESS_MESSAGES['forgot_password']['email_sent']}, status=status.HTTP_200_OK
            )
        return Response(
            {'message': ERROR_MESSAGES['forgot_password']['email_failed']}, status=status.HTTP_400_BAD_REQUEST
        )
