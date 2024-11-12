from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')

    phone = models.CharField(max_length=35, verbose_name='телефон', blank=True, null=True)
    # Для верификации почты ползователя:
    token = models.CharField(max_length=100, verbose_name='token', blank=True, null=True)

    login = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

        permissions = [('can_view_users', 'can view users')]
