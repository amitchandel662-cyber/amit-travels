from rest_framework import serializers
from .models import Vehicle, TourPackage, Booking, Inquiry

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class TourPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPackage
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'status']

    def validate(self, data):
        vehicle = data.get('vehicle')
        passengers = data.get('passengers')
        if vehicle and passengers and passengers > vehicle.seating_capacity:
            raise serializers.ValidationError({
                "passengers": f"{vehicle.name} seats up to {vehicle.seating_capacity} passengers."
            })

        start_date, end_date = data.get('start_date'), data.get('end_date')
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError({"end_date": "End date must be after the start date."})

        request = self.context.get('request')
        is_authenticated = bool(request and request.user and request.user.is_authenticated)
        if not is_authenticated:
            for field in ('guest_name', 'guest_phone'):
                if not data.get(field):
                    raise serializers.ValidationError({field: "Required when booking without an account."})
        return data

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'