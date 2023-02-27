from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class QuizUser(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    is_student = models.BooleanField()
    is_verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="quizuser")
    otp = models.CharField(max_length=5, default="0")
    number = models.CharField(max_length=11, default='0')
    number_verified = models.BooleanField(default=False)