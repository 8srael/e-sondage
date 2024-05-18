from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# poll model
class Poll(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Poll ({self.title})"