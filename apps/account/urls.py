"""
This file contains URL patterns for authentication
It uses a DefaultRouter to generate views
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.account.views import user_profile

router = DefaultRouter()
"""
Routing for signup, signin, sign-out, setpassword, logged-in-users,
userprofile, resend-setpassword. 
"""
router.register('user-profile', user_profile.UserProfileView, basename='user_profile')

urlpatterns = [
    path('', include(router.urls)),
]
