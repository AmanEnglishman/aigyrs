from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField('Username', max_length=150, unique=True)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # теперь username обязателен при создании superuser

    objects = CustomUserManager()

    def __str__(self):
        return self.username or self.email

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)
