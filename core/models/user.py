from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from core.models.permission import Permission
from utils.ulid import generate_ulid


class CustomUserManager(BaseUserManager):
    def create_user(self, permission, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')

        user = self.model(username=username, **extra_fields)
        user.permission = permission
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        permission = Permission.objects.get(code='SUPER_ADMIN')

        return self.create_user(permission, username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'users'

    user_id = models.UUIDField(primary_key=True, editable=False, default=generate_ulid)
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE)

    username = models.CharField(
        max_length=20, unique=True, null=False, verbose_name='Username'
    )
    name = models.CharField(
        max_length=20, unique=False, null=False, verbose_name='Name'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
