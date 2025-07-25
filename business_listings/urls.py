from django.urls import path
from . import views
from accounts import views as account_views

app_name = 'business_listings'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('businesses/', views.business_list, name='business_list'),
    path('business/<int:business_id>/', views.business_detail, name='business_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    
    # Business management
    path('business/add/', views.add_business, name='add_business'),
    path('business/<int:business_id>/edit/', views.edit_business, name='edit_business'),
    path('my-businesses/', views.my_businesses, name='my_businesses'),
    
    # Reviews
    path('business/<int:business_id>/review/', views.add_review, name='add_review'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    
    # AJAX endpoints
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
]

urlpatterns += [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('business/<int:business_id>/approve/', views.approve_business, name='approve_business'),
    path('business/<int:business_id>/reject/', views.reject_business, name='reject_business'),
    path('business/<int:business_id>/delete/', views.delete_business, name='delete_business'),
    path('contact/<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),
    path('admin-dashboard/export/<str:format>/', views.export_businesses, name='export_businesses'),
    path('admin-dashboard/plans/', account_views.admin_plan_list, name='admin_plan_list'),
    path('admin-dashboard/plans/add/', account_views.admin_plan_add, name='admin_plan_add'),
    path('admin-dashboard/plans/<int:plan_id>/edit/', account_views.admin_plan_edit, name='admin_plan_edit'),
    path('admin-dashboard/plans/<int:plan_id>/delete/', account_views.admin_plan_delete, name='admin_plan_delete'),
    path('admin/reply-contact/<int:contact_id>/', views.admin_reply_contact, name='admin_reply_contact'),
    path('admin/delete-contact/<int:contact_id>/', views.admin_delete_contact, name='admin_delete_contact'),
    path('my-contact-messages/', views.my_contact_messages, name='my_contact_messages'),
] 