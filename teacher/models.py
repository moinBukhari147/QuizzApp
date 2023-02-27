from django.db import models

# Create your models here.
import uuid
import random

# Create your models here.
class Subject(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    subject_name = models.CharField(max_length=255, default=None)
    def __str__(self) -> str:
        return self.subject_name
class Question(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    subject = models.ForeignKey(Subject, related_name='subject_quest', on_delete=models.CASCADE)
    marks = models.IntegerField(default=5)
    question = models.CharField(max_length=255)
    correct_ans = models.CharField(max_length=255)
    @property
    def get_ans(self):
        ans_objs = list(self.question_ans.all())
        ans = [anss.answer for anss in ans_objs]
        random.shuffle(ans)
        return ans
    def __str__(self) -> str:
        return self.question
class Answer(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_ans')
    answer = models.CharField(max_length=255, default=None)
    def __str__(self) -> str:
        return self.answer