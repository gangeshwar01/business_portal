from django.contrib import admin
from .models import UserProfile, Notification, SubscriptionPlan, UserSubscription

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Notification)

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'plan')
    search_fields = ('user__username', 'plan__name', 'upi_reference')
    readonly_fields = ('created_at', 'updated_at', 'payment_screenshot')
    actions = ['activate_subscription', 'reject_subscription']

    def activate_subscription(self, request, queryset):
        queryset.update(status='active')
    activate_subscription.short_description = 'Mark selected subscriptions as active'

    def reject_subscription(self, request, queryset):
        queryset.update(status='rejected')
    reject_subscription.short_description = 'Mark selected subscriptions as rejected'
