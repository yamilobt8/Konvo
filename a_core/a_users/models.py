from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return f"{self.user.username}'s Profile"


class PasswordHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    old_password = models.CharField(max_length=128)
    new_password = models.CharField(max_length=128, default='none')
    password_changed = models.BooleanField(default=False)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.old_password} -> {self.new_password}"

