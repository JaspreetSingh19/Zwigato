"""
Permissions module to check user has permission
"""
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAccessPermission(BasePermission, IsAuthenticated):
    """
    To create is access permission: To access Frontend
    """

    @staticmethod
    def has_permission(request):
        """
        To check user account is active, email and phone is verified
        """
        user = request.user
        if user.is_email_verified:
            return True
        return False


class IsManagerPermission(IsAccessPermission):
    """
    To create permission for only manager
    """

    @staticmethod
    def has_permission(request):
        """
        To check user account is active, email and phone is verified
        """
        user = request.user
        if user.role == 'Manager':
            return True
        return False


class IsAdminPermission(IsAccessPermission):
    """
    To create permission for only manager
    """
    @staticmethod
    def has_permission(request):
        """
        To create permission for only admin
        """
        user = request.user
        if user.role == 'Admin':
            return True
        return False


class IsDeliveryPermission(IsAccessPermission):
    """
    To create permission for only delivery
    """
    @staticmethod
    def has_permission(request):
        """
        To create permission for only admin
        """
        user = request.user
        if user.role == 'Delivery':
            return True
        return False

