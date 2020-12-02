from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.conf import settings



class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, is_active=True, is_staff=True, is_admin=False, type=2):
        if not phone:
            raise ValueError("Users must have a valid phone number")
        if not password:
            raise ValueError("Users must have a password")
        user = self.model(phone=phone)
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.type = type
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True

        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True

        )
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    phone = models.CharField(max_length=12, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    type = models.IntegerField(default=1)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.id)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.is_admin


class Products(models.Model):

    name = models.CharField(max_length=50)
    descritpion = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    price = models.BigIntegerField()
    category = models.CharField(max_length=20)
    seller = models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name