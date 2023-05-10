from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.account.serializers.update_profile import UserProfileSerializer
from apps.authentication.models import User
from apps.common.messages.msg_app import ERROR_MESSAGES, SUCCESS_MESSAGES


class UserProfileView(viewsets.ModelViewSet):
    """
    This view perform retrieving the data of the logged-in user
    and update their data according to their provided values.
    """
    http_method_names = ['get', 'put', 'patch']
    queryset = User
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of User objects that
        includes only the currently authenticated user.
        """
        return User.objects.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        """
        Display the single instance of the User
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        :param request: It gets the data that is requested by the user
        :param args: This returns the validated data in the form of list
        :param kwargs: This return the validated data in the form of dictionary
        :return: This return the updated data to the user with status
        """
        userprofile = self.request.user
        serializer = self.serializer_class(userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(userprofile, serializer.validated_data)
            return Response({
                'message': SUCCESS_MESSAGES['user_profile']['successfully'],
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        return Response({'error': ERROR_MESSAGES['user_profile']['failed']}, status=status.HTTP_400_BAD_REQUEST)
