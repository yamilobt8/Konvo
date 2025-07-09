from django.contrib.auth.models import User
from django.db import models


class Channel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_channels')
    # user.owned_channels.all()
    subscribers = models.ManyToManyField(User, related_name='subscribed_channels', blank=True)
    # user.subscribed_channels.all()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title