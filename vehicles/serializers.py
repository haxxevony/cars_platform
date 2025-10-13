from rest_framework import serializers
from .models import (
    Vehicle, Part, Listing, SellerProfile, BuyRequest, AuctionBid, SellerFeedback,
    EVTelemetry, ADASCalibration, FuseBox, WiringDiagram, SensorReading, OBDDiagnostic,
    Sensor, Acronym, LegacyDiagnosticCode, LegacyGuestBlog, LegacyCarListing, LegacySellerFeedback
)
from accounts.models import CustomUser
from django.core.validators import FileExtensionValidator

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'get_full_name', 'role']

class VehicleSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    image = serializers.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])

    class Meta:
        model = Vehicle
        fields = ['id', 'owner', 'make', 'model', 'year', 'vin', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_vin(self, value):
        if len(value) != 17:
            raise serializers.ValidationError("VIN must be exactly 17 characters.")
        if Vehicle.objects.filter(vin=value).exists():
            raise serializers.ValidationError("A vehicle with this VIN already exists.")
        return value

    def validate(self, data):
        if self.context['request'].user.is_authenticated and not self.context['request'].user.is_seller():
            raise serializers.ValidationError("Only sellers can create or update vehicles.")
        return data

class PartSerializer(serializers.ModelSerializer):
    seller = CustomUserSerializer(read_only=True)

    class Meta:
        model = Part
        fields = ['id', 'seller', 'name', 'description', 'price', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

class ListingSerializer(serializers.ModelSerializer):
    seller = CustomUserSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), source='vehicle', write_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'seller', 'vehicle', 'vehicle_id', 'title', 'description', 'price', 'currency', 'location', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if self.context['request'].user.is_authenticated and not self.context['request'].user.is_seller():
            raise serializers.ValidationError("Only sellers can create or update listings.")
        return data

class SellerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = SellerProfile
        fields = ['id', 'user', 'bio', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['rating', 'created_at', 'updated_at']

class BuyRequestSerializer(serializers.ModelSerializer):
    buyer = CustomUserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all(), source='listing', write_only=True)

    class Meta:
        model = BuyRequest
        fields = ['id', 'buyer', 'listing', 'listing_id', 'message', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']

    def validate(self, data):
        if self.context['request'].user.is_authenticated and not self.context['request'].user.is_buyer():
            raise serializers.ValidationError("Only buyers can create buy requests.")
        return data

class AuctionBidSerializer(serializers.ModelSerializer):
    bidder = CustomUserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all(), source='listing', write_only=True)

    class Meta:
        model = AuctionBid
        fields = ['id', 'bidder', 'listing', 'listing_id', 'amount', 'created_at']
        read_only_fields = ['created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Bid amount must be greater than zero.")
        return value

class SellerFeedbackSerializer(serializers.ModelSerializer):
    reviewer = CustomUserSerializer(read_only=True)
    seller = CustomUserSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='seller', write_only=True)

    class Meta:
        model = SellerFeedback
        fields = ['id', 'reviewer', 'seller', 'seller_id', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class EVTelemetrySerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), source='vehicle', write_only=True)

    class Meta:
        model = EVTelemetry
        fields = ['id', 'vehicle', 'vehicle_id', 'battery_level', 'range_remaining', 'timestamp']

class ADASCalibrationSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), source='vehicle', write_only=True)
    calibrated_by = CustomUserSerializer(read_only=True)

    class Meta:
        model = ADASCalibration
        fields = ['id', 'vehicle', 'vehicle_id', 'sensor_type', 'calibration_data', 'calibrated_by', 'timestamp']

class FuseBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuseBox
        fields = ['id', 'make', 'model', 'year', 'fuse_layout', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class WiringDiagramSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), source='vehicle', write_only=True)

    class Meta:
        model = WiringDiagram
        fields = ['id', 'vehicle', 'vehicle_id', 'system', 'diagram_file', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_diagram_file(self, value):
        validator = FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg'])
        validator(value)
        return value

class SensorReadingSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), source='vehicle', write_only=True)

    class Meta:
        model = SensorReading
        fields = ['id', 'vehicle', 'vehicle_id', 'sensor_type', 'value', 'timestamp']

class OBDDiagnosticSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), source='vehicle', write_only=True)

    class Meta:
        model = OBDDiagnostic
        fields = ['id', 'vehicle', 'vehicle_id', 'dtc_code', 'description', 'timestamp']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'type', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class AcronymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acronym
        fields = ['id', 'short_form', 'full_form', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class LegacyDiagnosticCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegacyDiagnosticCode
        fields = ['id', 'code', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class LegacyGuestBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegacyGuestBlog
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class LegacyCarListingSerializer(serializers.ModelSerializer):
    seller = CustomUserSerializer(read_only=True)

    class Meta:
        model = LegacyCarListing
        fields = ['id', 'seller', 'title', 'description', 'price', 'location', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class LegacySellerFeedbackSerializer(serializers.ModelSerializer):
    reviewer = CustomUserSerializer(read_only=True)
    seller = CustomUserSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='seller', write_only=True)

    class Meta:
        model = LegacySellerFeedback
        fields = ['id', 'reviewer', 'seller', 'seller_id', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']