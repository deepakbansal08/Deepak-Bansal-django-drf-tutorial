from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models


class UserManager(BaseUserManager):
    """
    Add manager methods here to create user and super user
    """

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("insert user")
        if not first_name:
            raise ValueError("insert first name")
        if not last_name:
            raise ValueError("insert last name")
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Needed fields
    - password (already inherited from AbstractBaseUser; encrypt password before saving to database)
    - last_login (already inherited from AbstractBaseUser)
    - is_superuser
    - first_name (max_length=30)
    - email (should be unique)
    - is_staff
    - date_joined (default should be time of object creation)
    - last_name (max_length=150)
    """

    first_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=150)
    date_joined = models.DateTimeField(default=datetime.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
