from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from business_listings.forms import UserRegistrationForm
from .models import UserProfile
from .models import Notification
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import sys
from .forms import PasswordResetEmailForm, OTPVerificationForm, SetNewPasswordForm
from .models import PasswordResetOTP
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, UserSubscription
from .forms import SubscriptionPurchaseForm
from django.contrib.admin.views.decorators import staff_member_required
from .forms import SubscriptionPlanForm
from django.urls import reverse
from django.http import JsonResponse
import json

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('business_listings:home')
    
    if request.method == 'POST':
        print('[DEBUG] Registration POST received', file=sys.stderr)
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Split full name
            full_name = request.POST.get('full_name', '').strip()
            first_name = ''
            last_name = ''
            if full_name:
                parts = full_name.split()
                first_name = parts[0]
                last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
            user = form.save(commit=False)
            user.first_name = first_name
            user.last_name = last_name
            # Set password properly
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # Debug output
            print(f"[DEBUG] User: {user}", file=sys.stderr)
            print(f"[DEBUG] Username: {user.username}", file=sys.stderr)
            print(f"[DEBUG] Password hash: {user.password}", file=sys.stderr)
            # Save UserProfile with mobile number
            mobile_number = form.cleaned_data.get('mobile_number')
            UserProfile.objects.create(user=user, mobile_number=mobile_number)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('accounts:login')
        else:
            print('[DEBUG] Registration form invalid', file=sys.stderr)
            print(form.errors, file=sys.stderr)
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'accounts/register.html', context)

def user_login(request):
    """User login view with 2FA enforcement"""
    if request.user.is_authenticated:
        return redirect('business_listings:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if 2FA is enabled
            if hasattr(user, 'profile') and user.profile.otp_enabled:
                # Generate a one-time code
                code = ''.join(random.choices(string.digits, k=6))
                request.session['2fa_code'] = code
                request.session['2fa_user_id'] = user.id
                send_mail(
                    'Your Login 2FA Verification Code',
                    f'Your verification code is: {code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return render(request, 'accounts/verify_2fa.html', {'email': user.email, 'login_flow': True})
            else:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'business_listings:home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    context = {
        'title': 'Login'
    }
    return render(request, 'accounts/login.html', context)

# 2FA verification for login
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def verify_2fa_login(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user_id = request.session.get('2fa_user_id')
        user = User.objects.filter(id=user_id).first()
        if user and code and code == request.session.get('2fa_code'):
            login(request, user)
            # Clean up session
            request.session.pop('2fa_code', None)
            request.session.pop('2fa_user_id', None)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('business_listings:home')
        else:
            messages.error(request, 'Invalid verification code.')
            return render(request, 'accounts/verify_2fa.html', {'email': user.email if user else '', 'login_flow': True})
    # If GET or no session, redirect to login
    return redirect('accounts:login')

@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('business_listings:home')

@login_required
def profile(request):
    """User profile view"""
    user_businesses = request.user.businesses.all().order_by('-created_at')
    user_reviews = request.user.reviews.all().order_by('-created_at')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    # Get all reviews written by admin for this user's businesses
    from django.contrib.auth.models import User
    admin_users = User.objects.filter(is_staff=True)
    admin_reviews_for_user_businesses = []
    if user_businesses.exists():
        from business_listings.models import Review
        admin_reviews_for_user_businesses = Review.objects.filter(business__in=user_businesses, user__in=admin_users).order_by('-created_at')
    admin_reviews_count = admin_reviews_for_user_businesses.count() if admin_reviews_for_user_businesses else 0
    all_subscriptions = request.user.subscriptions.all().order_by('-created_at')
    user_subscription = UserSubscription.objects.filter(user=request.user, status='active').first()

    context = {
        'user_businesses': user_businesses,
        'user_reviews': user_reviews,
        'notifications': notifications,
        'unread_notification_count': unread_count,
        'admin_reviews_for_user_businesses': admin_reviews_for_user_businesses,
        'admin_reviews_count': admin_reviews_count,
        'title': 'My Profile',
        'all_subscriptions': all_subscriptions,
        'user_subscription': user_subscription,
    }
    return render(request, 'accounts/profile.html', context)

# 2FA Enable/Disable Views
from django.views.decorators.http import require_POST

@login_required
@require_POST
def enable_2fa(request):
    user = request.user
    if not user.profile.otp_enabled:
        # Generate a one-time code
        code = ''.join(random.choices(string.digits, k=6))
        # Store code in session for verification
        request.session['2fa_code'] = code
        request.session['2fa_email'] = user.email
        # Send code via email
        send_mail(
            'Your 2FA Verification Code',
            f'Your verification code is: {code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return render(request, 'accounts/verify_2fa.html', {'email': user.email})
    return redirect('accounts:profile')

@login_required
@require_POST
def verify_2fa(request):
    user = request.user
    code = request.POST.get('code')
    if code and code == request.session.get('2fa_code'):
        user.profile.otp_enabled = True
        user.profile.save()
        Notification.objects.create(user=user, message='2FA enabled on your account.')
        # Clean up session
        request.session.pop('2fa_code', None)
        request.session.pop('2fa_email', None)
        messages.success(request, 'Two-Factor Authentication enabled!')
        return redirect('accounts:profile')
    else:
        messages.error(request, 'Invalid verification code.')
        return render(request, 'accounts/verify_2fa.html', {'email': user.email})

@login_required
@require_POST
def disable_2fa(request):
    user = request.user
    if user.profile.otp_enabled:
        user.profile.otp_enabled = False
        user.profile.save()
        Notification.objects.create(user=user, message='2FA disabled on your account.')
        messages.success(request, 'Two-Factor Authentication disabled.')
    return redirect('accounts:profile')

# Mark notification as read
@login_required
@require_POST
def mark_notification_read(request, notification_id):
    notif = Notification.objects.filter(id=notification_id, user=request.user).first()
    if notif:
        notif.is_read = True
        notif.save()
    
    # Redirect to admin dashboard if user is staff, otherwise to profile
    if request.user.is_staff:
        return redirect('business_listings:admin_dashboard')
    else:
        return redirect('accounts:profile')

@login_required
@require_POST
def delete_notification(request, notification_id):
    notif = Notification.objects.filter(id=notification_id, user=request.user).first()
    if notif:
        notif.delete()
        messages.success(request, 'Notification deleted successfully.')
    
    # Redirect to admin dashboard if user is staff, otherwise to profile
    if request.user.is_staff:
        return redirect('business_listings:admin_dashboard')
    else:
        return redirect('accounts:profile')

# Password Reset: Step 1 - Request

def forgot_password_request(request):
    if request.method == 'POST':
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                # Generate OTP
                otp = ''.join(random.choices(string.digits, k=6))
                expires_at = timezone.now() + timedelta(minutes=10)
                PasswordResetOTP.objects.create(user=user, otp=otp, expires_at=expires_at)
                # Send OTP email
                send_mail(
                    'Your Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                request.session['reset_email'] = email
                messages.success(request, 'An OTP has been sent to your email.')
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, 'No user found with that email address.')
    else:
        form = PasswordResetEmailForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})

# Password Reset: Step 2 - Verify OTP

def verify_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('accounts:forgot_password_request')
    user = User.objects.filter(email=email).first()
    if not user:
        messages.error(request, 'No user found with that email address.')
        return redirect('accounts:forgot_password_request')
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp, used=False, expires_at__gte=timezone.now()).order_by('-created_at').first()
            if otp_obj:
                otp_obj.used = True
                otp_obj.save()
                request.session['otp_verified'] = True
                messages.success(request, 'OTP verified. Please set your new password.')
                return redirect('accounts:set_new_password')
            else:
                messages.error(request, 'Invalid or expired OTP.')
    else:
        form = OTPVerificationForm()
    return render(request, 'accounts/verify_otp.html', {'form': form, 'email': email})

# Password Reset: Step 3 - Set New Password

def set_new_password(request):
    email = request.session.get('reset_email')
    otp_verified = request.session.get('otp_verified')
    if not (email and otp_verified):
        return redirect('accounts:forgot_password_request')
    user = User.objects.filter(email=email).first()
    if not user:
        messages.error(request, 'No user found with that email address.')
        return redirect('accounts:forgot_password_request')
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            # Clean up session
            request.session.pop('reset_email', None)
            request.session.pop('otp_verified', None)
            messages.success(request, 'Your password has been reset. You can now log in.')
            return redirect('accounts:login')
    else:
        form = SetNewPasswordForm()
    return render(request, 'accounts/set_new_password.html', {'form': form, 'email': email})

@login_required
def choose_plan(request):
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
    user_sub = UserSubscription.objects.filter(user=request.user, status='active').first()
    return render(request, 'accounts/choose_plan.html', {
        'plans': plans,
        'user_subscription': user_sub
    })

@login_required
def purchase_plan(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    if request.method == 'POST':
        form = SubscriptionPurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if user has an active subscription
            current_subscription = UserSubscription.objects.filter(user=request.user, status='active').first()
            is_upgrade = current_subscription is not None
            
            sub = form.save(commit=False)
            sub.user = request.user
            sub.plan = plan
            sub.status = 'pending'
            sub.save()
            print(f"[DEBUG] Saved UserSubscription: {sub}", file=sys.stderr)
            print(f"[DEBUG] payment_screenshot: {sub.payment_screenshot}", file=sys.stderr)
            
            # Determine notification message based on whether it's an upgrade or new subscription
            if is_upgrade:
                admin_message = f'Subscription upgrade request from {request.user.username}: {current_subscription.plan.get_name_display()} → {plan.get_name_display()}. Payment proof uploaded.'
                user_message = f'Your subscription upgrade request from {current_subscription.plan.get_name_display()} to {plan.get_name_display()} has been submitted successfully. Admin will review and activate it soon.'
            else:
                admin_message = f'New subscription request from {request.user.username} for {plan.get_name_display()} plan. Payment proof uploaded.'
                user_message = f'Your subscription request for {plan.get_name_display()} has been submitted successfully. Admin will review and activate it soon.'
            
            # Notify all admins about subscription request
            admin_users = User.objects.filter(is_staff=True)
            for admin in admin_users:
                Notification.objects.create(
                    user=admin, 
                    message=admin_message
                )
            
            # Notify user about successful submission
            Notification.objects.create(
                user=request.user,
                message=user_message
            )
            
            messages.success(request, 'Your payment proof has been submitted. Admin will verify and activate your plan soon.')
            return redirect(f"{reverse('accounts:choose_plan')}?success=true")
        else:
            print('[DEBUG] SubscriptionPurchaseForm invalid', file=sys.stderr)
            print(form.errors, file=sys.stderr)
            print('[DEBUG] FILES:', request.FILES, file=sys.stderr)
    else:
        form = SubscriptionPurchaseForm()
    return render(request, 'accounts/purchase_plan.html', {'plan': plan, 'form': form})



@staff_member_required
def admin_plan_list(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'admin/plan_list.html', {'plans': plans})

@staff_member_required
def admin_plan_add(request):
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan added successfully!')
            return redirect('business_listings:admin_plan_list')
        else:
            # If not valid, form will show errors
            pass
    else:
        form = SubscriptionPlanForm()
    return render(request, 'admin/plan_form.html', {'form': form, 'action': 'Add'})

@staff_member_required
def admin_plan_edit(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('business_listings:admin_plan_list')
    else:
        form = SubscriptionPlanForm(instance=plan)
    return render(request, 'admin/plan_form.html', {'form': form, 'action': 'Edit'})

@staff_member_required
def admin_plan_delete(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    if request.method == 'POST':
        plan.delete()
        return redirect('business_listings:admin_plan_list')
    return render(request, 'admin/plan_confirm_delete.html', {'plan': plan})

@staff_member_required
def admin_activate_subscription(request, sub_id):
    sub = get_object_or_404(UserSubscription, id=sub_id, status='pending')
    if request.method == 'POST':
        # Check if user has an existing active subscription (for upgrades)
        existing_subscription = UserSubscription.objects.filter(user=sub.user, status='active').first()
        is_upgrade = existing_subscription is not None
        
        # Deactivate existing subscription if upgrading
        if is_upgrade:
            existing_subscription.status = 'expired'
            existing_subscription.save()
        
        # Activate new subscription
        sub.status = 'active'
        sub.start_date = timezone.now()
        if sub.plan:
            sub.end_date = sub.start_date + timezone.timedelta(days=sub.plan.duration_days)
        sub.save()
        
        # Create appropriate notification messages
        if is_upgrade:
            user_message = f'Your subscription has been upgraded from {existing_subscription.plan.get_name_display()} to {sub.plan.get_name_display()} and is now active!'
            admin_message = f'Subscription upgrade for {sub.user.username}: {existing_subscription.plan.get_name_display()} → {sub.plan.get_name_display()} activated.'
        else:
            user_message = f'Your subscription for {sub.plan.get_name_display()} has been activated!'
            admin_message = f'New subscription for {sub.user.username} ({sub.plan.get_name_display()}) activated.'
        
        Notification.objects.create(user=sub.user, message=user_message)
        messages.success(request, f'Subscription for {sub.user.username} activated.')
        
        # Notify all admins
        for admin in User.objects.filter(is_staff=True):
            Notification.objects.create(user=admin, message=admin_message)
        
        return redirect(reverse('business_listings:admin_dashboard'))
    return redirect(reverse('business_listings:admin_dashboard'))

@staff_member_required
def admin_reject_subscription(request, sub_id):
    sub = get_object_or_404(UserSubscription, id=sub_id, status='pending')
    if request.method == 'POST':
        sub.status = 'rejected'
        sub.save()
        Notification.objects.create(user=sub.user, message=f'Your subscription request for {sub.plan.get_name_display()} was rejected. Please contact support for details.')
        messages.success(request, f'Subscription for {sub.user.username} rejected.')
        # Notify all admins
        for admin in User.objects.filter(is_staff=True):
            Notification.objects.create(user=admin, message=f'Subscription for {sub.user.username} ({sub.plan.get_name_display()}) was rejected.')
        return redirect(reverse('business_listings:admin_dashboard'))
    return redirect(reverse('business_listings:admin_dashboard'))

def user_subscription_context(request):
    if request.user.is_authenticated:
        user_subscription = request.user.subscriptions.filter(status='active').first()
        unread_notification_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {
            'user_subscription': user_subscription,
            'unread_notification_count': unread_notification_count
        }
    return {}

@csrf_exempt
def resend_otp(request):
    """Resend OTP for password reset"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            if not email:
                return JsonResponse({'success': False, 'message': 'Email is required'})
            
            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'success': False, 'message': 'No user found with that email address'})
            
            # Generate new OTP
            otp = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timedelta(minutes=10)
            
            # Create new OTP record
            PasswordResetOTP.objects.create(user=user, otp=otp, expires_at=expires_at)
            
            # Send OTP email
            send_mail(
                'Your Password Reset OTP (Resent)',
                f'Your new OTP for password reset is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({'success': True, 'message': 'OTP has been resent successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid request data'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred while resending OTP'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def resend_2fa(request):
    """Resend 2FA verification code"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            login_flow = data.get('login_flow', 'false').lower() == 'true'
            
            if not email:
                return JsonResponse({'success': False, 'message': 'Email is required'})
            
            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'success': False, 'message': 'No user found with that email address'})
            
            # Generate new verification code
            code = ''.join(random.choices(string.digits, k=6))
            
            if login_flow:
                # For login flow, store in session
                request.session['2fa_code'] = code
                request.session['2fa_user_id'] = user.id
            else:
                # For 2FA enable flow, store in session
                request.session['2fa_code'] = code
                request.session['2fa_email'] = user.email
            
            # Send verification code email
            subject = 'Your 2FA Verification Code (Resent)'
            if login_flow:
                subject = 'Your Login 2FA Verification Code (Resent)'
            
            send_mail(
                subject,
                f'Your new verification code is: {code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({'success': True, 'message': 'Verification code has been resent successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid request data'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred while resending verification code'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
