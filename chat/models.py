from django.db import models
from django.contrib.auth.models import User # If you want to associate conversations with users

class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='messages')
    sender = models.CharField(max_length=50)  # "User" or "Mentor"
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] # Ensure messages are ordered by time