from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customuser_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set'
    )


class TaskModel(models.Model):
    title = models.CharField(max_length=100, blank=False)
    due_date = models.DateField(auto_now=False)
    assigned_to = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=100, blank=False)
    is_in_progress = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    comments = models.CharField(max_length=1000, blank=True)
