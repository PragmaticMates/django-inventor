from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.db.models import Q


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def with_perm(self, perm_name):
        return self.filter(
            Q(is_superuser=True) |
            Q(user_permissions__codename=perm_name) |
            Q(groups__permissions__codename=perm_name)
        ).distinct()


class UserManager(DjangoUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_full_name(self, full_name, ignore_accent=False):
        first_name, last_name = full_name.split(' ', 1)
        first_name = first_name.strip()
        last_name = last_name.strip()

        if ignore_accent:
            return self.get(first_name__unaccent=first_name, last_name__unaccent=last_name)
        return self.get(first_name=first_name, last_name=last_name)

    def filter_by_full_name(self, full_name):
        try:
            first_name, last_name = full_name.split(' ', 1)
            first_name = first_name.strip()
            last_name = last_name.strip()
            return self.filter(first_name__unaccent__icontains=first_name, last_name__unaccent__icontains=last_name)
        except ValueError:
            return self.filter(Q(first_name__unaccent__icontains=full_name) | Q(last_name__unaccent__icontains=full_name))

    def active(self):
        return self.get_queryset().active()

    def with_perm(self, perm_name):
        return self.get_queryset().with_perm(perm_name)
