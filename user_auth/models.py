from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)  # Optional profile picture
    bio = models.TextField(blank=True, null=True)  # User bio

    def __str__(self):
        return self.user.username
