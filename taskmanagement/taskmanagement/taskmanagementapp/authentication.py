from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import CustomUser


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                return user

        except CustomUser.DoesNotExist:
            try:
                adminuser = User.objects.get(username=username)
                if adminuser.check_password(password):
                    return adminuser
            except CustomUser.DoesNotExist:
                return None
