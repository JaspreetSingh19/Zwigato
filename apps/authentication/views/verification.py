from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.authentication.models import User
from apps.authentication.serializers.verification import VerifyOTPSerializer
from apps.common.messages.msg_app import SUCCESS_MESSAGES


class OTPVerificationView(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = User
    serializer_class = VerifyOTPSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        queryset = User.objects.filter(email=email)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'success': SUCCESS_MESSAGES['verification']['email'],
                             }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
