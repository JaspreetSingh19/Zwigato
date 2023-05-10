from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import TimeStampedModel


# Create your models here.
class Role(models.TextChoices):
    """ Role choices """
    ADMIN = 'Admin',
    MANAGER = 'Manager',
    CUSTOMER = 'Customer',
    DELIVERY = 'Delivery',


class User(AbstractUser, TimeStampedModel):
    """
    Custom user model that extends the built-in Django User model
    with additional fields for User model
    * username and email are unique
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=16, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    contact = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    token = models.CharField(max_length=255, null=True, blank=True)
    email_otp = models.IntegerField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the database table
        for User model
        """
        db_table = 'User'


class ForgetPassword(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=255, unique=True, null=True, blank=False)
    objects = models.Manager()

    def __str__(self):
        return str(self.user.email)

    class Meta:
        """
        Use the Meta class to specify the database table
        for ForgetPassword model
        """
        db_table = 'ForgetPassword'
