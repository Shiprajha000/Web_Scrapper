from django.db import models

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.job_title} at {self.company}'

