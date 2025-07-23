from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_number = models.CharField(max_length=15)
    otp_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=64, blank=True, null=True)  # For future use (TOTP, etc.)

    def __str__(self):
        return f"{self.user.username} Profile"

# Notification model for user/admin notifications
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}..."

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_otps')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.username} ({'used' if self.used else 'active'})"

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    features = models.TextField(blank=True)
    badge_color = models.CharField(max_length=20, default='#888')
    badge_icon = models.CharField(max_length=50, blank=True, help_text='FontAwesome icon class')
    is_active = models.BooleanField(default=True)
    paytm_qr = models.FileField(upload_to='plan_qr_codes/', blank=True, null=True)
    google_pay_qr = models.FileField(upload_to='plan_qr_codes/', blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.get_name_display()

class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=30, blank=True)
    upi_reference = models.CharField(max_length=100, blank=True)
    payment_screenshot = models.FileField(upload_to='subscription_payments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"

    class Meta:
        ordering = ['-created_at']
