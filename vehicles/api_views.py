from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfgen import canvas
import csv
from datetime import datetime

from .pagination import StandardResultsSetPagination
from .models import (
    Vehicle, Part, Listing, SellerProfile, BuyRequest, AuctionBid, SellerFeedback,
    EVTelemetry, ADASCalibration, FuseBox, WiringDiagram, SensorReading, OBDDiagnostic,
    Sensor, Acronym, LegacyDiagnosticCode, LegacyGuestBlog, LegacyCarListing, LegacySellerFeedback
)
from .serializers import (
    VehicleSerializer, PartSerializer, ListingSerializer, SellerProfileSerializer,
    BuyRequestSerializer, AuctionBidSerializer, SellerFeedbackSerializer,
    EVTelemetrySerializer, ADASCalibrationSerializer, FuseBoxSerializer,
    WiringDiagramSerializer, SensorReadingSerializer, OBDDiagnosticSerializer,
    SensorSerializer, AcronymSerializer,
    LegacyDiagnosticCodeSerializer, LegacyGuestBlogSerializer,
    LegacyCarListingSerializer, LegacySellerFeedbackSerializer
)
from .filters import (
    VehicleFilter, PartFilter, ListingFilter, SellerProfileFilter, BuyRequestFilter,
    AuctionBidFilter, SellerFeedbackFilter, EVTelemetryFilter, ADASCalibrationFilter,
    FuseBoxFilter, WiringDiagramFilter, SensorReadingFilter, OBDDiagnosticFilter,
    SensorFilter, AcronymFilter,
    LegacyDiagnosticCodeFilter, LegacyGuestBlogFilter,
    LegacyCarListingFilter, LegacySellerFeedbackFilter
)

class VehicleMetadataView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        metadata = Vehicle.objects.values('make', 'model', 'year').distinct()
        return Response(list(metadata))

class FuseBoxLookupView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        data = FuseBox.objects.values('vehicle__vin', 'location', 'make', 'model', 'year').distinct()
        return Response(list(data))

class SensorChartView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        data = (
            SensorReading.objects
            .values('sensor_type')
            .annotate(avg_value=Avg('value'))
            .order_by('sensor_type')
        )
        chart_data = {
            "labels": [entry['sensor_type'] for entry in data],
            "values": [round(float(entry['avg_value']), 2) for entry in data],
        }
        return Response(chart_data)

class ExportCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="vehicles_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Make', 'Model', 'Year', 'VIN'])

        for vehicle in Vehicle.objects.all():
            writer.writerow([vehicle.make, vehicle.model, vehicle.year, vehicle.vin])

        return response

class ExportPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="vehicles_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'

        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, "Vehicle Export")

        y = 780
        for vehicle in Vehicle.objects.all():
            line = f"{vehicle.make} {vehicle.model} ({vehicle.year}) - VIN: {vehicle.vin}"
            p.drawString(100, y, line)
            y -= 20
            if y < 50:
                p.showPage()
                p.setFont("Helvetica", 12)
                y = 800

        p.save()
        return response

class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
        model_name = self.get_serializer().Meta.model.__name__.lower()
        user = self.request.user
        serializer.save(
            owner=user if model_name == 'vehicle' else None,
            seller=user if model_name in ['part', 'listing', 'legacycarlisting'] else None,
            bidder=user if model_name == 'auctionbid' else None,
            reviewer=user if model_name in ['sellerfeedback', 'legacysellerfeedback'] else None,
            buyer=user if model_name == 'buyrequest' else None,
            calibrated_by=user if model_name == 'adascalibration' else None
        )


class VehicleViewSet(BaseViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filterset_class = VehicleFilter
    model = Vehicle

    def get_queryset(self):
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return Vehicle.objects.filter(owner=self.request.user)
        return super().get_queryset()

class PartViewSet(BaseViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    filterset_class = PartFilter
    model = Part

class ListingViewSet(BaseViewSet):
    queryset = Listing.objects.filter(is_active=True)
    serializer_class = ListingSerializer
    filterset_class = ListingFilter
    model = Listing

class SellerProfileViewSet(BaseViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    filterset_class = SellerProfileFilter
    model = SellerProfile

    def get_queryset(self):
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return SellerProfile.objects.filter(user=self.request.user)
        return super().get_queryset()

class BuyRequestViewSet(BaseViewSet):
    queryset = BuyRequest.objects.all()
    serializer_class = BuyRequestSerializer
    filterset_class = BuyRequestFilter
    model = BuyRequest

class AuctionBidViewSet(BaseViewSet):
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer
    filterset_class = AuctionBidFilter
    model = AuctionBid

class SellerFeedbackViewSet(BaseViewSet):
    queryset = SellerFeedback.objects.all()
    serializer_class = SellerFeedbackSerializer
    filterset_class = SellerFeedbackFilter
    model = SellerFeedback

class EVTelemetryViewSet(BaseViewSet):
    queryset = EVTelemetry.objects.all()
    serializer_class = EVTelemetrySerializer
    filterset_class = EVTelemetryFilter
    model = EVTelemetry

class ADASCalibrationViewSet(BaseViewSet):
    queryset = ADASCalibration.objects.all()
    serializer_class = ADASCalibrationSerializer
    filterset_class = ADASCalibrationFilter
    model = ADASCalibration

class FuseBoxViewSet(BaseViewSet):
    queryset = FuseBox.objects.all()
    serializer_class = FuseBoxSerializer
    filterset_class = FuseBoxFilter
    model = FuseBox

class WiringDiagramViewSet(BaseViewSet):
    queryset = WiringDiagram.objects.all()
    serializer_class = WiringDiagramSerializer
    filterset_class = WiringDiagramFilter
    model = WiringDiagram

class SensorReadingViewSet(BaseViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    filterset_class = SensorReadingFilter
    model = SensorReading

class OBDDiagnosticViewSet(BaseViewSet):
    queryset = OBDDiagnostic.objects.all()
    serializer_class = OBDDiagnosticSerializer
    filterset_class = OBDDiagnosticFilter
    model = OBDDiagnostic

class SensorViewSet(BaseViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    filterset_class = SensorFilter
    model = Sensor

class AcronymViewSet(BaseViewSet):
    queryset = Acronym.objects.all()
    serializer_class = AcronymSerializer
    filterset_class = AcronymFilter
    model = Acronym

class LegacyDiagnosticCodeViewSet(BaseViewSet):
    queryset = LegacyDiagnosticCode.objects.all()
    serializer_class = LegacyDiagnosticCodeSerializer
    filterset_class = LegacyDiagnosticCodeFilter
    model = LegacyDiagnosticCode

class LegacyGuestBlogViewSet(BaseViewSet):
    queryset = LegacyGuestBlog.objects.all()
    serializer_class = LegacyGuestBlogSerializer
    filterset_class = LegacyGuestBlogFilter
    model = LegacyGuestBlog

class LegacyCarListingViewSet(BaseViewSet):
    queryset = LegacyCarListing.objects.all()
    serializer_class = LegacyCarListingSerializer
    filterset_class = LegacyCarListingFilter
    model = LegacyCarListing

class LegacySellerFeedbackViewSet(BaseViewSet):
    queryset = LegacySellerFeedback.objects.all()
    serializer_class = LegacySellerFeedbackSerializer
    filterset_class = LegacySellerFeedbackFilter
    model = LegacySellerFeedback