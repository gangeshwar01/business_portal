from django import forms
from django.contrib.auth.models import User
from .models import SubscriptionPlan, UserSubscription

class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the OTP sent to your email'}))

class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data 

class SubscriptionPurchaseForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=[('paytm', 'Paytm'), ('googlepay', 'Google Pay'), ('upi', 'UPI')],
        widget=forms.RadioSelect,
        required=True,
        label='Payment Method'
    )
    upi_reference = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'UPI Transaction/Reference ID'}),
        label='UPI Reference/Transaction ID'
    )
    payment_screenshot = forms.FileField(
        required=True,
        label='Upload Payment Screenshot (Image or PDF)'
    )
    class Meta:
        model = UserSubscription
        fields = ['payment_method', 'upi_reference', 'payment_screenshot'] 

class SubscriptionPlanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': 2, 'class': 'form-control'})
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'price', 'duration_days', 'description', 'features', 'badge_color', 'is_active'] 