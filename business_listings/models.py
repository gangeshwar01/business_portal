from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import os
import time
from multiselectfield import MultiSelectField

# Removed business_image_path function

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For FontAwesome icons
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Business(models.Model):
    BUSINESS_STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
    ]
    BUSINESS_TYPE_CHOICES = [
        ('Hotel', 'Hotel'),
        ('Restaurant', 'Restaurant'),
        ('Cafe', 'Café'),
        ('Dhaba', 'Dhaba'),
        ('Cab Service', 'Cab Service'),
        ('Home Stay', 'Home Stay'),
        ('Dharamshala', 'Dharamshala'),
        ('Adventure', 'Adventure'),
        ('Water Park', 'Water Park'),
        ('ParkTravel', 'ParkTravel'),
        ('Agency Tour Packages', 'Agency Tour Packages'),
        ('Guide Services', 'Guide Services'),
        ('Car/Bike Rental', 'Car/Bike Rental'),
        ('Temple/Pilgrimage Services', 'Temple/Pilgrimage Services'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='businesses', null=True, blank=True)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.FileField(upload_to='business_images/', blank=True, null=True)
    cover_image = models.FileField(upload_to='business_images/', blank=True, null=True)
    hours_of_operation = models.TextField(blank=True)
    operating_days = models.CharField(
        max_length=100,
        choices=[
            ('Monday-Friday', 'Monday-Friday'),
            ('Monday-Saturday', 'Monday-Saturday'),
            ('Monday-Sunday', 'Monday-Sunday'),
            ('Tuesday-Saturday', 'Tuesday-Saturday'),
            ('Wednesday-Sunday', 'Wednesday-Sunday'),
            ('Thursday-Monday', 'Thursday-Monday'),
            ('Friday-Tuesday', 'Friday-Tuesday'),
            ('Saturday-Wednesday', 'Saturday-Wednesday'),
            ('Sunday-Thursday', 'Sunday-Thursday'),
            ('All Days', 'All Days (7 days a week)'),
            ('Weekends Only', 'Weekends Only'),
            ('Weekdays Only', 'Weekdays Only'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    services = models.TextField(blank=True)
    business_types = MultiSelectField(choices=BUSINESS_TYPE_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=BUSINESS_STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year_of_establishment = models.IntegerField(blank=True, null=True)
    google_business_profile = models.URLField(blank=True, null=True)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    owner_first_name = models.CharField(max_length=50, blank=True, null=True)
    owner_last_name = models.CharField(max_length=50, blank=True, null=True)
    owner_phone_number = models.CharField(max_length=20, blank=True, null=True)
    owner_whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    owner_email = models.EmailField(blank=True, null=True)
    owner_alternate_phone_number = models.CharField(max_length=20, blank=True, null=True)
    owner_area_code = models.CharField(max_length=10, blank=True, null=True)
    vehicle_types = MultiSelectField(
        choices=[
            ('Sedan', 'Sedan'),
            ('SUV', 'SUV'),
            ('Auto', 'Auto'),
            ('Bike', 'Bike'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    vehicle_types_other = models.CharField(max_length=100, blank=True, null=True)
    service_area_coverage = MultiSelectField(
        choices=[
            ('Within City', 'Within City'),
            ('Outstation', 'Outstation'),
            ('Both', 'Both'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    service_area_coverage_other = models.CharField(max_length=100, blank=True, null=True)
    available_drivers = models.CharField(
        max_length=10,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    available_drivers_other = models.CharField(max_length=100, blank=True, null=True)
    ac_nonac = models.CharField(
        max_length=10,
        choices=[
            ('AC', 'AC'),
            ('Non-AC', 'Non-AC'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    ac_nonac_other = models.CharField(max_length=100, blank=True, null=True)
    pricing = models.CharField(max_length=100, blank=True, null=True)
    total_rides_activities = models.CharField(max_length=100, blank=True, null=True)
    entry_fee = models.CharField(max_length=100, blank=True, null=True)
    safety_certification = models.CharField(
        max_length=3,
        choices=[('YES', 'YES'), ('NO', 'NO')],
        blank=True,
        null=True
    )
    safety_certification_file = models.FileField(upload_to='verification_uploads/', blank=True, null=True)
    changing_rooms_lockers = models.CharField(
        max_length=3,
        choices=[('YES', 'YES'), ('NO', 'NO')],
        blank=True,
        null=True
    )
    package_types_offered = MultiSelectField(
        choices=[
            ('Solo', 'Solo'),
            ('Family', 'Family'),
            ('Honeymoon', 'Honeymoon'),
            ('Group', 'Group'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    package_types_offered_other = models.CharField(max_length=100, blank=True, null=True)
    live_music_pet_friendly = MultiSelectField(
        choices=[
            ('Live Music', 'Live Music'),
            ('Pet Friendly', 'Pet Friendly'),
            ('Family Seating', 'Family Seating'),
        ],
        blank=True,
        null=True
    )
    live_music_pet_friendly_other = models.CharField(max_length=100, blank=True, null=True)
    available_services = MultiSelectField(
        choices=[
            ('Online Booking', 'Online Booking'),
            ('Walk-in Customers', 'Walk-in Customers'),
            ('Home Delivery', 'Home Delivery'),
            ('Pickup/Drop Service', 'Pickup/Drop Service'),
            ('24x7 Helpline', '24x7 Helpline'),
            ('Reservation Required', 'Reservation Required'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    available_services_other = models.CharField(max_length=100, blank=True, null=True)
    destinations_covered = models.CharField(max_length=255, blank=True, null=True)
    price_range = models.CharField(max_length=100, blank=True, null=True)
    transport_accommodation_included = models.CharField(
        max_length=10,
        choices=[('YES', 'YES'), ('NO', 'NO'), ('Other', 'Other')],
        blank=True,
        null=True
    )
    transport_accommodation_included_other = models.CharField(max_length=100, blank=True, null=True)
    customization_available = models.CharField(
        max_length=3,
        choices=[('YES', 'YES'), ('NO', 'NO')],
        blank=True,
        null=True
    )
    special_offers_discounts = models.CharField(max_length=255, blank=True, null=True)
    menu_tariff_card = models.FileField(upload_to='verification_uploads/', blank=True, null=True)
    license_certification = models.FileField(upload_to='verification_uploads/', blank=True, null=True)
    gst_certification = models.FileField(upload_to='verification_uploads/', blank=True, null=True)
    brochure_flyer = models.FileField(upload_to='verification_uploads/', blank=True, null=True)
    payment_modes_accepted = MultiSelectField(
        choices=[
            ('UPI', 'UPI'),
            ('Debit/Credit Card', 'Debit/Credit Card'),
            ('Net Banking', 'Net Banking'),
            ('Cash', 'Cash'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    payment_modes_accepted_other = models.CharField(max_length=100, blank=True, null=True)
    ongoing_discounts = models.CharField(max_length=255, blank=True, null=True)
    declaration_agreed = models.BooleanField(default=False)
    admin_review = models.TextField(blank=True, null=True)
    
    # Additional fields for category-specific information
    category_specific_additions = models.CharField(
        max_length=50,
        choices=[
            ('hotels', 'Hotels / Home Stays / Resorts'),
            ('restaurants', 'Restaurants / Cafes / Dhabas'),
            ('cab', 'Cab / Taxi / Rental Services'),
            ('water_parks', 'Water Parks / Adventure Parks / VR-Zone etc'),
            ('travel', 'Travel & Tour Packages'),
        ],
        blank=True,
        null=True
    )
    
    # Hotel/Resort specific fields
    room_types_offered = MultiSelectField(
        choices=[
            ('Single', 'Single'),
            ('Double', 'Double'),
            ('Suite', 'Suite'),
            ('Dormitory', 'Dormitory'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    total_number_of_rooms = models.IntegerField(blank=True, null=True)
    facilities = MultiSelectField(
        choices=[
            ('Wi-Fi', 'Wi-Fi'),
            ('AC', 'AC'),
            ('Parking', 'Parking'),
            ('Breakfast', 'Breakfast'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    facilities_other = models.CharField(max_length=100, blank=True, null=True)
    
    # Restaurant/Cafe specific fields
    cuisine_type = MultiSelectField(
        choices=[
            ('North Indian', 'North Indian'),
            ('South Indian', 'South Indian'),
            ('Fast Food', 'Fast Food'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    cuisine_type_other = models.CharField(max_length=100, blank=True, null=True)
    seating_capacity = models.IntegerField(blank=True, null=True)
    veg_nonveg = MultiSelectField(
        choices=[
            ('Veg', 'Veg'),
            ('Non-Veg', 'Non-Veg'),
            ('Both', 'Both'),
            ('Other', 'Other'),
        ],
        blank=True,
        null=True
    )
    veg_nonveg_other = models.CharField(max_length=100, blank=True, null=True)
    
    # Other business type field
    other_business_type = models.CharField(max_length=100, blank=True, null=True)
    
    # Add or update payment screenshot field
    payment_screenshot = models.FileField(upload_to='subscription_payments/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/business/{self.id}/'
    
    def update_rating(self):
        """Update business rating based on reviews"""
        reviews = self.reviews.all()
        if reviews:
            avg_rating = sum(review.rating for review in reviews) / len(reviews)
            self.rating = round(avg_rating, 2)
            self.total_reviews = len(reviews)
            self.save()

class Review(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['business', 'user']  # One review per user per business
    
    def __str__(self):
        return f"{self.user.username} - {self.business.name} - {self.rating} stars"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.business.update_rating()

class Contact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('support', 'Support'),
        ('business', 'Business Listing'),
        ('feedback', 'Feedback'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to='business_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.business.name} - {self.caption or 'Image'}"

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
