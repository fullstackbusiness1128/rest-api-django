from django.contrib.auth.models import AbstractUser
from django.db import models

from users.helper import RandomFileName


class Media(models.Model):
    class Meta:
        db_table = 'table_media'

    title = models.CharField(max_length=512, blank=True)
    file = models.FileField(upload_to=RandomFileName('uploads'))
    order = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Create your models here.
class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_users'

    PENDING = 'P'
    ACTIVE = 'A'
    BLOCKED = 'B'
    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (ACTIVE, 'active'),
        (BLOCKED, 'blocked'),
    )

    EDITOR = 'E'
    ADMIN = 'A'
    SUPERADMIN = 'S'
    ROLE_CHOICES = (
        (EDITOR, 'editor'),
        (ADMIN, 'admin'),
        (SUPERADMIN, 'superadmin'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField('email', max_length=200, unique=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default=EDITOR)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    avatar = models.ForeignKey(Media, blank=True, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=30, default=None, blank=True, null=True)

    def get_verbose_status(self):
        return self.get_status_display()
