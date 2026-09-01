from django.db import models
from django.conf import settings

class Vehicle(models.Model):
    CATEGORY_CHOICES = (
        ('SUV', 'SUV (Ertiga, Innova)'),
        ('TEMPO', 'Tempo Traveller'),
        ('SEDAN', 'Sedan'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    seating_capacity = models.PositiveIntegerField()
    luggage_capacity = models.PositiveIntegerField()
    # JSONField allows flexible arrays like ["AC", "WiFi", "Recliner Seats"]
    features = models.JSONField(default=list , help_text="List of features")
    base_price_per_km = models.DecimalField(max_digits=8,decimal_places=2)
    image = models.ImageField(upload_to='vehicles/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"
    

class TourPackage(models.Model):
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='packages/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    # was: on_delete=CASCADE, required — now nullable so guests can book
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    tour_package = models.ForeignKey(TourPackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')  # NEW
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='bookings')

    guest_name = models.CharField(max_length=150, blank=True)   # NEW
    guest_email = models.EmailField(blank=True)                  # NEW
    guest_phone = models.CharField(max_length=20, blank=True)    # NEW

    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    passengers = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    special_requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.user.username if self.user else (self.guest_name or "Guest")
        return f"Booking {self.id} - {who}"
    

class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry from {self.name}"
    
class TourItineraryDay(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='itinerary_days')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, help_text="e.g., Chandigarh to Shimla")
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('tour_package', 'day_number')
        ordering = ['day_number']

    def __str__(self):
        return f"{self.tour_package.title} - Day {self.day_number}"
    
    
class GalleryPhoto(models.Model):
    CATEGORY_CHOICES = (
        ('VEHICLE', 'Fleet'),
        ('CUSTOMER', 'With Customers'),
        ('DESTINATION', 'On the Road'),
    )
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video = models.FileField(upload_to='gallery/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='CUSTOMER')
    caption = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=150, blank=True, help_text="e.g. Kunzum La, Spiti Valley")
    customer_name = models.CharField(max_length=100, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_photos')
    tour_package = models.ForeignKey(TourPackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_photos')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.caption or f"Photo #{self.id} ({self.get_category_display()})"