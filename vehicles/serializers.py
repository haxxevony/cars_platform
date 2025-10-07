from rest_framework import serializers
from .models import (
    Acronym, AuctionBid, BlogPost, BuyRequest, FuseBox, Listing, ADASCalibration,
    OBDDiagnostic, SellerProfile, Sensor, SensorReading, Vehicle, EVTelemetry, WiringDiagram, Part, SellerFeedback, LegacyDiagnosticCode, LegacyGuestBlog, LegacyCarListing, LegacySellerFeedback  # ✅ Add these
)

class ADASCalibrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADASCalibration
        fields = '__all__'
        read_only_fields = ['calibration_date']


class EVTelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EVTelemetry
        fields = '__all__'
        read_only_fields = ['timestamp']

class SellerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerFeedback
        fields = '__all__'
        read_only_fields = ['timestamp']

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'
        read_only_fields = ['timestamp']


class AcronymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acronym
        fields = '__all__'

class AuctionBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionBid
        fields = '__all__'
        read_only_fields = ['timestamp']

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = ['timestamp']

class BuyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyRequest
        fields = '__all__'
        read_only_fields = ['timestamp']

class FuseBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuseBox
        fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['timestamp']

class OBDDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = OBDDiagnostic
        fields = '__all__'
        read_only_fields = ['timestamp']

class SellerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = SellerProfile
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = '__all__'
        read_only_fields = ['timestamp']

class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['created_at']

class VehicleDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'year']

class WiringDiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = WiringDiagram
        fields = '__all__'
        read_only_fields = ['uploaded_at']

class LegacyGuestBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegacyGuestBlog
        fields = '__all__'

class LegacyCarListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegacyCarListing
        fields = '__all__'

class LegacySellerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegacySellerFeedback
        fields = '__all__'

class LegacyDiagnosticCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegacyDiagnosticCode
        fields = '__all__'
        read_only_fields = ['timestamp']
