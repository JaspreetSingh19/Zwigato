from django.contrib import admin

from apps.authentication.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'first_name', 'username', 'email', 'contact', 'password', 'role', 'token',
        'email_otp', 'is_email_verified', 'created_at', 'updated_at'
    )

    class Meta:
        model = User


admin.site.register(User, UserAdmin)
