from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('enable-2fa/', views.enable_2fa, name='enable_2fa'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
    path('disable-2fa/', views.disable_2fa, name='disable_2fa'),
    path('notification/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notification/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('verify-2fa-login/', views.verify_2fa_login, name='verify_2fa_login'),
    path('forgot-password/', views.forgot_password_request, name='forgot_password_request'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('choose-plan/', views.choose_plan, name='choose_plan'),
    path('purchase-plan/<int:plan_id>/', views.purchase_plan, name='purchase_plan'),
    path('admin-activate-subscription/<int:sub_id>/', views.admin_activate_subscription, name='admin_activate_subscription'),
    path('admin-reject-subscription/<int:sub_id>/', views.admin_reject_subscription, name='admin_reject_subscription'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('resend-2fa/', views.resend_2fa, name='resend_2fa'),
] 