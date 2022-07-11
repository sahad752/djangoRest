from django.db import models

# Create your models here.


class appointment(models.Model):
    """
    Student
    """
    name = models.CharField(max_length=100)
    type = models.IntegerField() # 1: candidate 2: interviewer
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    def __str__(self):
        return self.name