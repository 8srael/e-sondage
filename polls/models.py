from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# poll model
class Poll(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'polls'
    
    def __str__(self):
        return f"Poll ({self.title})"

# type model
class Type(models.Model):
    label = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'types'
    
    def __str__(self):
        return f"Type ({self.label})"

# question model
class Question(models.Model):
    label = models.CharField(max_length=250)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    possibilities = models.ManyToManyField('Possibility', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'

    def __str__(self):
        return f"Question (type = {self.type.label}, label = \"{self.label}\")"
    
class Possibility(models.Model):
    label = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'possibilities'

    def __str__(self) -> str:
        return f"Possibility (label = {self.label})"