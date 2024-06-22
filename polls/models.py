from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

# poll model
class Poll(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question')
    token = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'polls'
    
    def __str__(self) -> str:
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
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    possibilities = models.ManyToManyField('Possibility', through='QuestionPossibility', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'

    def __str__(self) -> str:
        return f"Question (type = {self.type.label}, label = \"{self.label}\")"
    
# possibility model
class Possibility(models.Model):
    label = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question, through='QuestionPossibility', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'possibilities'
        verbose_name_plural = "Possibliities"

    def __str__(self) -> str:
        return f"Possibility (label = {self.label})"
    
# intermediary table betwenn question and possibility
class QuestionPossibility(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    possibility = models.ForeignKey(Possibility, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions_possibilities'
        verbose_name_plural = "Questions-Possibilities"
    
    def __str__(self) -> str:
        return f"QuestionPossibility (question = {self.question.label}, possibility = {self.possibility.label})"
    

# Participant model
class Participant(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=15)
    token = models.UUIDField(editable=False, unique=True, blank=True, null=True)
    has_submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'participants'
    
    def __str__(self) -> str:
        if self.poll:
            return f"Participant (poll = {self.poll.title}, token = {self.token}), email = {self.email})"
        return f"Participant (email = {self.email})"
    
class Answer(models.Model):
    question_possibiity = models.ForeignKey(QuestionPossibility, on_delete=models.CASCADE, null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'answers'