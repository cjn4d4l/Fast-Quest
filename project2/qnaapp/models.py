from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question (models.Model):
    topic: str = models.TextField()
    question: str = models.TextField()
    correct_answer: str = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} - {self.question} - {self.correct_answer}"