from django.db import models
from django.core.validators import *

from django.contrib.auth.models import User

# Create your models here.
class Ebook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.title} - {self.author}"
    
class Review(models.Model):
    review_author = models.ForeignKey(User, on_delete=models.CASCADE)# 
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    review = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, related_name="reviews")
    
    
    def __str__(self) -> str:
        return f"{self.rating}"