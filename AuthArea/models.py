from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
# from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        
        if email is None:
            raise TypeError('Email must be provided')

        email = self.normalize_email(email)

        new_user = self.model(email, **extra_fields)

        new_user.set_password(password)

        new_user.save()
        return new_user


    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise TypeError("Super user must be a staff")

        if extra_fields.get('is_superuser') is not True:
            raise TypeError("Superuser should be set to True")

        if extra_fields.get('is_active') is not True:
            raise TypeError("Superuser must be True")

        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=70, unique=True, db_index=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=15, null=False, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

