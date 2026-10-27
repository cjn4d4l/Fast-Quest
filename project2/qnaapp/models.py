from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic (models.Model):
    topic: str = models.TextField()
    count: int = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.topic} - {self.count}"

class Question (models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question: str = models.TextField()
    correct_answer: str = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} - {self.question} - {self.correct_answer}"