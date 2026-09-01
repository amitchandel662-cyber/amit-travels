from rest_framework import viewsets, permissions
from .models import Vehicle, TourPackage , Booking , Inquiry
from .serializers import VehicleSerializer, TourPackageSerializer, BookingSerializer, InquirySerializer

class VehicleViewSet(viewsets.ReadOnlyModelViewSet):
    """Public API to view available vehicles"""
    queryset = Vehicle.objects.filter(is_available = True)
    serializer_class = VehicleSerializer

# class TourPackageViewSet(viewsets.ModelViewSet):
#     """Public API to view active tour packages"""
#     queryset = TourPackage.objects.filter(is_active = True)
#     serializer_class = TourPackageSerializer

# class BookingViewSet(viewsets.ModelViewSet):
#     """Authenticated API to manage customer bookings"""
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     def get_queryset(self):
#         # Customers only see their own bookings; admins see everything
#         if self.request.user.is_staff or self.request.user.role == "Admin":
#             return Booking.objects.all()
#         return Booking.objects.filter(user = self.request.user)
    
#     def perform_create(self , serializer):
#         serializer.save(user = self.request.user)

class TourPackageViewSet(viewsets.ModelViewSet):
    queryset = TourPackage.objects.filter(is_active=True)
    serializer_class = TourPackageSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]   # was wide open to anyone before — fix this regardless of the rest


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]   # guests can submit requests
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Booking.objects.none()
        if user.is_staff or getattr(user, 'role', None) == 'Admin':   # fixed: was crashing on stock User
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)

