from django.db import models
from users.models import Customer
from catalog.models import Book

class RecommendationModel(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)

class UserRecommendation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    model = models.ForeignKey(RecommendationModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class RecommendedBook(models.Model):
    recommendation = models.ForeignKey(UserRecommendation, on_delete=models.CASCADE, related_name='books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class Report(models.Model):
    report_type = models.CharField(max_length=100)
    content = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)

class ErrorLog(models.Model):
    message = models.TextField()
    stack_trace = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class SystemConfig(models.Model):
    config_key = models.CharField(max_length=255, unique=True)
    config_value = models.TextField()
