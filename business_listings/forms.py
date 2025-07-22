from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Business, Review, Contact, Newsletter, BusinessImage
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import ClearableFileInput
from .models import Category



class BusinessForm(forms.ModelForm):
    business_types = forms.MultipleChoiceField(
        choices=Business.BUSINESS_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Business Type'
    )
    year_of_establishment = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2005'}),
        label='Year of Establishment'
    )
    google_business_profile = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        label='Google Business Profile Link (if available)'
    )
    owner_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner Name'}),
        label='Owner Name'
    )
    owner_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
        label='Email'
    )
    owner_area_code = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Area Code'}),
        label='Area Code'
    )
    owner_phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        label='Phone Number'
    )
    owner_whatsapp_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp Number'}),
        label='WhatsApp Number'
    )
    owner_alternate_phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        label='Alternate Contact Phone Number'
    )
    
    # Category-specific additions
    CATEGORY_SPECIFIC_CHOICES = [
        ('', 'Please Select'),
        ('hotels', 'Hotels / Home Stays / Resorts'),
        ('restaurants', 'Restaurants / Cafes / Dhabas'),
        ('cab', 'Cab / Taxi / Rental Services'),
        ('water_parks', 'Water Parks / Adventure Parks / VR-Zone etc'),
        ('travel', 'Travel & Tour Packages'),
    ]  

    category_specific_additions = forms.ChoiceField(
        choices=CATEGORY_SPECIFIC_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Category-Specific Additions'
    )
    
    # Hotel/Resort specific fields
    room_types_offered = forms.MultipleChoiceField(
        choices=[('Single', 'Single'), ('Double', 'Double'), ('Suite', 'Suite'), ('Dormitory', 'Dormitory'), ('Other', 'Other')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Room Types Offered'
    )
    total_number_of_rooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Total Number of Rooms'
    )
    facilities = forms.MultipleChoiceField(
        choices=[('Wi-Fi', 'Wi-Fi'), ('AC', 'AC'), ('Parking', 'Parking'), ('Breakfast', 'Breakfast'), ('Other', 'Other')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Facilities'
    )
    
    # Restaurant/Cafe specific fields
    cuisine_type = forms.MultipleChoiceField(
        choices=[('North Indian', 'North Indian'), ('South Indian', 'South Indian'), ('Fast Food', 'Fast Food'), ('Other', 'Other')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Cuisine Type'
    )
    seating_capacity = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Seating Capacity'
    )
    veg_nonveg = forms.MultipleChoiceField(
        choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg'), ('Both', 'Both'), ('Other', 'Other')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Veg / Non-Veg / Both'
    )
    live_music_pet_friendly = forms.MultipleChoiceField(
        choices=[('Live Music', 'Live Music'), ('Pet Friendly', 'Pet Friendly'), ('Family Seating', 'Family Seating')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Live Music / Pet Friendly / Family Seating'
    )
    
    # Other business type field
    other_business_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify if Other'}),
        label='If Other, please specify'
    )
    
    # Available services fields
    available_services = forms.MultipleChoiceField(
        choices=[
            ('Online Booking', 'Online Booking'),
            ('Walk-in Customers', 'Walk-in Customers'),
            ('Home Delivery', 'Home Delivery'),
            ('Pickup/Drop Service', 'Pickup/Drop Service'),
            ('24x7 Helpline', '24x7 Helpline'),
            ('Reservation Required', 'Reservation Required'),
            ('Other', 'Other'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Available Services'
    )
    available_services_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
        label='Other Available Services'
    )
    
    vehicle_types = forms.MultipleChoiceField(
        choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Auto', 'Auto'), ('Bike', 'Bike'), ('Other', 'Other')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Type of Vehicle(s)'
    )
    service_area_coverage = forms.MultipleChoiceField(
        choices=[('Within City', 'Within City'), ('Outstation', 'Outstation'), ('Both', 'Both'), ('Other', 'Other')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Service Area Coverage'
    )
    available_drivers = forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('No', 'No'), ('Other', 'Other')],
        required=False,
        widget=forms.RadioSelect,
        label='Available Drivers'
    )
    ac_nonac = forms.ChoiceField(
        choices=[('AC', 'AC'), ('Non-AC', 'Non-AC'), ('Other', 'Other')],
        required=False,
        widget=forms.RadioSelect,
        label='AC/Non-AC'
    )
    pricing = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pricing details'}),
        label='Pricing (Per KM or Per Trip Basis)'
    )
    vehicle_types_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
        label='Other Vehicle Type'
    )
    service_area_coverage_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
        label='Other Service Area Coverage'
    )
    available_drivers_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
        label='Other Available Drivers'
    )
    ac_nonac_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
        label='Other AC/Non-AC'
    )
    total_rides_activities = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Total Rides/Activities'
    )
    entry_fee = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Entry Fee (Adults, Kids, Family Pass, etc.)'
    )
    safety_certification = forms.ChoiceField(
        choices=[('YES', 'YES'), ('NO', 'NO')],
        required=False,
        widget=forms.RadioSelect,
        label='Safety Certification'
    )
    safety_certification_file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Upload Safety Certification'
    )
    changing_rooms_lockers = forms.ChoiceField(
        choices=[('YES', 'YES'), ('NO', 'NO')],
        required=False,
        widget=forms.RadioSelect,
        label='Changing Rooms / Lockers Availability'
    )
    package_types_offered = forms.MultipleChoiceField(
        choices=[('Solo', 'Solo'), ('Family', 'Family'), ('Honeymoon', 'Honeymoon'), ('Group', 'Group'), ('Other', 'Other')],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Types of Packages Offered'
    )
    package_types_offered_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify package type'}),
        label='Other Package Type'
    )
    destinations_covered = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Destinations Covered'
    )
    price_range = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Price Range (Approx)'
    )
    transport_accommodation_included = forms.ChoiceField(
        choices=[('YES', 'YES'), ('NO', 'NO'), ('Other', 'Other')],
        required=False,
        widget=forms.RadioSelect,
        label='Transport & Accommodation Included'
    )
    transport_accommodation_included_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
        label='Other Transport & Accommodation Option'
    )
    customization_available = forms.ChoiceField(
        choices=[('YES', 'YES'), ('NO', 'NO')],
        required=False,
        widget=forms.RadioSelect,
        label='Customization Available'
    )
    special_offers_discounts = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Special Offers or Discounts (if any)'
    )
    menu_tariff_card = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Upload Menu / Tariff Card'
    )
    license_certification = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Any License or Certification'
    )
    gst_certification = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='GST Number or Certification'
    )
    brochure_flyer = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Upload Brochure / Flyer'
    )
    payment_modes_accepted = forms.MultipleChoiceField(
        choices=[('UPI', 'UPI'), ('Debit/Credit Card', 'Debit/Credit Card'), ('Net Banking', 'Net Banking'), ('Cash', 'Cash'), ('Other', 'Other')],
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label='Payment Modes Accepted'
    )
    payment_modes_accepted_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify payment mode'}),
        label='Other Payment Mode'
    )
    ongoing_discounts = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Ongoing Discounts / Packages / Coupons'
    )
    declaration_agreed = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I agree to the terms and conditions'
    )

    class Meta:
        model = Business
        fields = [
            'name', 'category', 'business_types', 'other_business_type', 'year_of_establishment', 'google_business_profile',
            'category_specific_additions', 'room_types_offered', 'total_number_of_rooms', 'facilities',
            'cuisine_type', 'seating_capacity', 'veg_nonveg', 'live_music_pet_friendly',
            'available_services', 'available_services_other',
            'owner_name', 'owner_email', 'owner_area_code', 'owner_phone_number',
            'owner_whatsapp_number', 'owner_alternate_phone_number',
            'description', 'address', 'city', 'state', 'zip_code', 'country', 'phone', 'email', 'website', 'logo', 'cover_image', 'hours_of_operation', 'operating_days', 'services',
            'vehicle_types', 'service_area_coverage', 'available_drivers', 'ac_nonac', 'pricing',
            'vehicle_types_other', 'service_area_coverage_other', 'available_drivers_other', 'ac_nonac_other',
            'total_rides_activities', 'entry_fee', 'safety_certification', 'safety_certification_file', 'changing_rooms_lockers',
            'package_types_offered', 'package_types_offered_other', 'destinations_covered', 'price_range', 'transport_accommodation_included', 'transport_accommodation_included_other', 'customization_available', 'special_offers_discounts',
            'menu_tariff_card', 'license_certification', 'gst_certification', 'brochure_flyer',
            'payment_modes_accepted', 'payment_modes_accepted_other', 'ongoing_discounts',
            'declaration_agreed'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Business name'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category_other': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please specify category'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your business...'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter full address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ZIP Code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Website URL (optional)'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'hours_of_operation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Business hours (e.g., Mon-Fri: 9AM-5PM)'
            }),
            'operating_days': forms.Select(attrs={
                'class': 'form-select'
            }),
            'services': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List your services...'
            }),
            'vehicle_types': forms.CheckboxSelectMultiple,
            'service_area_coverage': forms.CheckboxSelectMultiple,
            'available_drivers': forms.RadioSelect,
            'ac_nonac': forms.RadioSelect,
            'vehicle_types_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
            'service_area_coverage_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
            'available_drivers_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
            'ac_nonac_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
            'total_rides_activities': forms.TextInput(attrs={'class': 'form-control'}),
            'entry_fee': forms.TextInput(attrs={'class': 'form-control'}),
            'safety_certification': forms.RadioSelect,
            'safety_certification_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'changing_rooms_lockers': forms.RadioSelect,
            'package_types_offered': forms.CheckboxSelectMultiple,
            'package_types_offered_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
            'destinations_covered': forms.TextInput(attrs={'class': 'form-control'}),
            'price_range': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_accommodation_included': forms.RadioSelect,
            'transport_accommodation_included_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
            'customization_available': forms.RadioSelect,
            'special_offers_discounts': forms.TextInput(attrs={'class': 'form-control'}),
            'menu_tariff_card': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'license_certification': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gst_certification': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'brochure_flyer': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'payment_modes_accepted': forms.CheckboxSelectMultiple,
            'payment_modes_accepted_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify'}),
            'ongoing_discounts': forms.TextInput(attrs={'class': 'form-control'}),
            'declaration_agreed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Basic phone validation - you can enhance this
        if phone and len(phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) < 10:
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone
    


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(choices=[
                (1, '1 - Poor'),
                (2, '2 - Fair'),
                (3, '3 - Good'),
                (4, '4 - Very Good'),
                (5, '5 - Excellent')
            ], attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'mobile_no', 'subject', 'message', 'contact_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email'
            }),
            'mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile No.'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your message...'
            }),
            'contact_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address'
    }))
    mobile_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mobile number'
    }))
    terms = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }), label="I agree to the Terms of Service and Privacy Policy")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_number', 'password1', 'password2', 'terms']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if mobile and len(mobile.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) < 10:
            raise forms.ValidationError('Please enter a valid mobile number.')
        return mobile

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search businesses, categories, or locations...',
            'id': 'search-input'
        })
    )
    category = forms.ChoiceField(
        choices=[('', 'All Categories')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        })
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('newest', 'Newest First'),
            ('oldest', 'Oldest First'),
            ('rating', 'Highest Rated'),
            ('name', 'Name A-Z')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate category choices
        categories = Category.objects.all()
        self.fields['category'].choices = [('', 'All Categories')] + [
            (cat.id, cat.name) for cat in categories
        ] 

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    ) 