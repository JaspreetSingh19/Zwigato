"""
This file contains URL patterns for authentication
It uses a DefaultRouter to generate views
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.authentication.views import signup, verification, auth, forgot, reset_password

router = DefaultRouter()
"""
Routing for signup, signin, sign-out, setpassword, logged-in-users,
userprofile, resend-setpassword. 
"""
router.register('signup', signup.SignupView, basename='signup')
router.register('verify-otp', verification.OTPVerificationView, basename='verify_otp')
router.register('login', auth.LoginView, basename='login')
router.register('logout', auth.LogoutView, basename='logout')
router.register('forget_password', forgot.ForgotPasswordView, basename='forget_password')
router.register(
    r'reset_password/(?P<token>[^/.]+)', reset_password.ResetPasswordViewSet, basename='reset_password'
)

urlpatterns = [
    path('', include(router.urls)),
]
