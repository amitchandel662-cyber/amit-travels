from django.shortcuts import render, get_object_or_404
from .models import Vehicle, TourPackage, Booking, GalleryPhoto
import os
from django.conf import settings

# Create your views here.


def homepage(request):
    vehicles = Vehicle.objects.filter(is_available=True)
    packages = TourPackage.objects.filter(is_active=True)

    # Map static station data to packages for the elevation chart
    # In a real app, you might move this into your database models
    tour_data = {
        "Spiti Valley Expedition": {
            "kms": "850",
            "stations": [
                {"name": "Shimla", "x": 10, "y": 140},
                {"name": "Kalpa", "x": 130, "y": 100},
                {"name": "Kaza", "x": 300, "y": 30},
                {"name": "Manali", "x": 490, "y": 140},
            ],
        },
        "Leh Ladakh Odyssey": {
            "kms": "1200",
            "stations": [
                {"name": "Manali", "x": 10, "y": 140},
                {"name": "Baralacha", "x": 150, "y": 20},
                {"name": "Tanglang", "x": 350, "y": 10},
                {"name": "Leh", "x": 490, "y": 120},
            ],
        },
        # Add entries for other packages as needed...
    }

    # Attach chart data to package objects
    for pkg in packages:
        data = tour_data.get(pkg.title, {"kms": "---", "stations": []})
        pkg.chart_data = data

    return render(
        request, "homepage.html", {"vehicles": vehicles, "packages": packages}
    )


# def tour_detail(request, tour_id=None):
#     # For demonstration, we will pass all available vehicles to the booking form
#     vehicles = Vehicle.objects.filter(is_available=True)

#     # If using real database data:
#     # package = get_object_or_404(TourPackage, id=tour_id)
#     # itinerary = package.itinerary_days.all()

#     context = {
#         'vehicles': vehicles,
#     }
#     return render(request, 'tour_detail.html', context)


def tour_detail(request, tour_id=None):
    # If a specific tour ID is passed in the URL (e.g., /tour/1/)
    if tour_id:
        package = get_object_or_404(
            TourPackage.objects.prefetch_related("itinerary_days"),
            id=tour_id,
            is_active=True,
        )
        vehicles = Vehicle.objects.filter(is_available=True)
        return render(
            request,
            "tour_detail.html",
            {
                "package": package,
                "itinerary": package.itinerary_days.all(),
                "vehicles": vehicles,
            },
        )

    # If NO ID is passed (e.g., /tour/detail/) -> Load for Frontend Testing
    return render(request, "tour_detail.html")


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "booking_confirmation.html", {"booking": booking})


def vehicle_booking(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return render(request, "vehicle_booking.html", {"vehicle": vehicle})


# travel/views.py
def gallery(request):
    # 1. Fetch database photos
    photos = GalleryPhoto.objects.select_related("vehicle", "tour_package").all()
    
    # 2. Scan the local media/fleet directory
    fleet_dir = os.path.join(settings.MEDIA_ROOT, 'fleet')
    fleet_images = []
    
    if os.path.exists(fleet_dir):
        valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        fleet_images = [
            f"{settings.MEDIA_URL}fleet/{f}"
            for f in os.listdir(fleet_dir)
            if f.lower().endswith(valid_extensions)
        ]

    # 3. Calculate counts (adding the local fleet images to the DB vehicle count)
    db_vehicle_count = photos.filter(category="VEHICLE").count()
    total_vehicle_count = db_vehicle_count + len(fleet_images)

    return render(
        request,
        "gallery.html",
        {
            "photos": photos,
            "fleet_images": fleet_images,
            "vehicle_count": total_vehicle_count,
            "customer_count": photos.filter(category="CUSTOMER").count(),
            "destination_count": photos.filter(category="DESTINATION").count(),
        },
    )


def trip_planner(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, is_available=True)
    return render(request, "trip_planner.html", {"vehicle": vehicle})


def why_us(request):
    """Renders the 'Why Choose Us' page."""
    return render(request, "why_us.html")
