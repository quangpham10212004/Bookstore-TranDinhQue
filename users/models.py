from django.db import models
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )
    dob = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username

class Customer(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='customer_profile')
    
    def __str__(self):
        return f"Customer: {self.member.username}"

class Admin(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='admin_profile')
    
    def __str__(self):
        return f"Admin: {self.member.username}"

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    num = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.num} {self.street}"

class UserSession(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

class UserActivityLog(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class NotificationType(models.Model):
    name = models.CharField(max_length=50)

class Notification(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    read_flag = models.BooleanField(default=False)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class EmailVerification(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class PasswordResetToken(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
