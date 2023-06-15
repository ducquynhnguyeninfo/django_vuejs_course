from django.db import models

# Create your models here.
class JobOffer(models.Model):
    # id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=200)
    company_email = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    salary = models.FloatField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField()
    
    def __str__(self) -> str:
        return f"{self.company_name} {self.job_title} {self.salary}"
    