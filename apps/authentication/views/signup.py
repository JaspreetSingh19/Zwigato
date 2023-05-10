from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.authentication.models import User
from apps.authentication.serializers.signup import SignupSerializer
from apps.common.messages.msg_app import SUCCESS_MESSAGES


class SignupView(viewsets.ModelViewSet):
    """
    SignupView class to register a new user
    """
    http_method_names = ['post']
    queryset = User
    serializer_class = SignupSerializer

    def get_queryset(self):
        """
        Queryset to provide list of users by filtering their
        on the basis of various criteria.
        """
        user = User.objects.filter()
        return user

    def create(self, request, *args, **kwargs):
        """
        creates a new requested user
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({
                'data': serializer.data,
                'success': SUCCESS_MESSAGES['signup']['successfully'],
                'message': SUCCESS_MESSAGES['signup']['email'],
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
