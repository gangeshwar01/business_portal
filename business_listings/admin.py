from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Business, Review, Contact, BusinessImage, Newsletter

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'city', 'state', 'status', 'rating', 'is_featured', 'created_at', 'vehicle_types', 'service_area_coverage', 'available_drivers', 'ac_nonac', 'pricing']
    list_filter = ['status', 'is_featured', 'city', 'state', 'created_at']
    search_fields = ['name', 'owner__username', 'city', 'state', 'description']
    list_editable = ['status', 'is_featured']
    readonly_fields = ['rating', 'total_reviews', 'views', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'owner', 'description')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Media', {
            'fields': ('logo', 'cover_image')
        }),
        ('Business Details', {
            'fields': ('hours_of_operation', 'operating_days', 'services')
        }),
        ('Status & Statistics', {
            'fields': ('status', 'is_featured', 'rating', 'total_reviews', 'views')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['business', 'user', 'rating', 'title', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['business__name', 'user__username', 'title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('business', 'user')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile_no', 'subject', 'contact_type', 'is_read', 'created_at']
    list_filter = ['contact_type', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'mobile_no', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected contacts as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected contacts as unread"

@admin.register(BusinessImage)
class BusinessImageAdmin(admin.ModelAdmin):
    list_display = ['business', 'caption', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['business__name', 'caption']
    list_editable = ['is_primary']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('business')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']
    readonly_fields = ['subscribed_at']
    ordering = ['-subscribed_at']
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"
