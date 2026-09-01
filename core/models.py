from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff/Driver'
        CUSTOMER = 'CUSTOMER', 'Customer'

    role = models.CharField(
        max_length= 10 ,
        choices = Role.choices ,
        default=Role.CUSTOMER
    )

    phone_number = models.CharField(max_length=15, blank=True,null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"