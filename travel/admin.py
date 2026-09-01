from django.contrib import admin
from .models import Vehicle, TourPackage, TourItineraryDay, Booking, Inquiry , GalleryPhoto

class TourItineraryDayInline(admin.TabularInline):
    model = TourItineraryDay
    extra = 8  # Shows 8 empty rows automatically for the itinerary

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_days', 'price', 'is_active')
    inlines = [TourItineraryDayInline] # This adds the itinerary days to the tour package page!

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'seating_capacity', 'is_available')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vehicle', 'start_date', 'status')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_resolved')

@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'caption', 'customer_name', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('caption', 'customer_name', 'location')
