"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Import both API viewsets and the template frontend view
from travel.api_views import VehicleViewSet, TourPackageViewSet, BookingViewSet
from travel.views import homepage , tour_detail , booking_confirmation , vehicle_booking , gallery  , trip_planner , why_us

# Initialize the API Router
router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='api-vehicles')
router.register(r'packages', TourPackageViewSet, basename='api-packages')
router.register(r'bookings', BookingViewSet, basename='api-bookings')

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),
    
    # Web Frontend (Premium HTML Homepage)
    path('', homepage, name='home'), 
    
    # REST API Endpoints (Prefixed with api/ to keep clean separation)
    path('api/', include(router.urls)), 
    path('tour/detail/', tour_detail, name='tour_detail'),
    path('tour/<int:tour_id>/', tour_detail, name='tour_detail'),
    path('booking/<int:booking_id>/confirmation/', booking_confirmation, name='booking_confirmation'),
    path('vehicle/<int:vehicle_id>/', vehicle_booking, name='vehicle_booking'),
    path('gallery/', gallery, name='gallery'),
    path('plan/<int:vehicle_id>/', trip_planner, name='trip_planner'),
    path('why-us/', why_us, name='why_us'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)