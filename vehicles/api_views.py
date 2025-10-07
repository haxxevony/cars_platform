from rest_framework import viewsets
from .models import (
    Vehicle, Part, Listing, SellerProfile, BuyRequest, AuctionBid,
    SellerFeedback, EVTelemetry, ADASCalibration, FuseBox, WiringDiagram,
    SensorReading, OBDDiagnostic, Sensor, Acronym, BlogPost,
    LegacyDiagnosticCode, LegacyGuestBlog, LegacyCarListing, LegacySellerFeedback
)
from .serializers import (
    VehicleSerializer, PartSerializer, ListingSerializer, SellerProfileSerializer,
    BuyRequestSerializer, AuctionBidSerializer, SellerFeedbackSerializer,
    EVTelemetrySerializer, ADASCalibrationSerializer, FuseBoxSerializer,
    WiringDiagramSerializer, SensorReadingSerializer, OBDDiagnosticSerializer,
    SensorSerializer, AcronymSerializer, BlogPostSerializer,
    LegacyDiagnosticCodeSerializer, LegacyGuestBlogSerializer,
    LegacyCarListingSerializer, LegacySellerFeedbackSerializer
)

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer

class BuyRequestViewSet(viewsets.ModelViewSet):
    queryset = BuyRequest.objects.all()
    serializer_class = BuyRequestSerializer

class AuctionBidViewSet(viewsets.ModelViewSet):
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer

class SellerFeedbackViewSet(viewsets.ModelViewSet):
    queryset = SellerFeedback.objects.all()
    serializer_class = SellerFeedbackSerializer

class EVTelemetryViewSet(viewsets.ModelViewSet):
    queryset = EVTelemetry.objects.all()
    serializer_class = EVTelemetrySerializer

class ADASCalibrationViewSet(viewsets.ModelViewSet):
    queryset = ADASCalibration.objects.all()
    serializer_class = ADASCalibrationSerializer

class FuseBoxViewSet(viewsets.ModelViewSet):
    queryset = FuseBox.objects.all()
    serializer_class = FuseBoxSerializer

class WiringDiagramViewSet(viewsets.ModelViewSet):
    queryset = WiringDiagram.objects.all()
    serializer_class = WiringDiagramSerializer

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer

class OBDDiagnosticViewSet(viewsets.ModelViewSet):
    queryset = OBDDiagnostic.objects.all()
    serializer_class = OBDDiagnosticSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class AcronymViewSet(viewsets.ModelViewSet):
    queryset = Acronym.objects.all()
    serializer_class = AcronymSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class LegacyDiagnosticCodeViewSet(viewsets.ModelViewSet):
    queryset = LegacyDiagnosticCode.objects.all()
    serializer_class = LegacyDiagnosticCodeSerializer

class LegacyGuestBlogViewSet(viewsets.ModelViewSet):
    queryset = LegacyGuestBlog.objects.all()
    serializer_class = LegacyGuestBlogSerializer

class LegacyCarListingViewSet(viewsets.ModelViewSet):
    queryset = LegacyCarListing.objects.all()
    serializer_class = LegacyCarListingSerializer

class LegacySellerFeedbackViewSet(viewsets.ModelViewSet):
    queryset = LegacySellerFeedback.objects.all()
    serializer_class = LegacySellerFeedbackSerializer
