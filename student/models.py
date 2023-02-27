from django.db import models
import uuid

class Record(models.Model):
    #link the score with the student profile
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    result_status = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    subject = models.CharField(max_length=255)
    @property
    def get_result_status(self):
        if self.result_status is True:
            return "Passed"
        else:
            return'Failed'
    
    def __str__(self):
        status = self.get_result_status
        return f"{self.subject} - {status}"