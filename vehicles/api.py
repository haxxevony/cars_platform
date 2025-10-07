from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from collections import Counter

from .models import (
    Vehicle, OBDDiagnostic, Sensor, Acronym, FuseBox, BlogPost,
    AuctionBid, SellerProfile, BuyRequest, WiringDiagram
)
from .serializers import (
    VehicleSerializer, OBDDiagnosticSerializer, SensorSerializer, AcronymSerializer,
    FuseBoxSerializer, BlogPostSerializer, AuctionBidSerializer,
    SellerProfileSerializer, BuyRequestSerializer, WiringDiagramSerializer
)
from .export import export_queryset_to_csv

# ✅ Vehicle dropdown for frontend filters
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    @action(detail=False, methods=['get'])
    def dropdown(self, request):
        vehicles = Vehicle.objects.all().values('id', 'make', 'model', 'year')
        return Response(list(vehicles))

# ✅ OBD diagnostics with export and chart endpoints
class OBDDiagnosticViewSet(viewsets.ModelViewSet):
    queryset = OBDDiagnostic.objects.all()
    serializer_class = OBDDiagnosticSerializer

    @action(detail=False, methods=['get'])
    def export(self, request):
        fields = ['dtc_code', 'description', 'severity']
        return export_queryset_to_csv(self.get_queryset(), fields, filename='obd_diagnostics.csv')

    @action(detail=False, methods=['get'])
    def chart(self, request):
        data = self.get_queryset().values_list('severity', flat=True)
        counts = Counter(data)
        return Response(dict(counts))

# ✅ Remaining model viewsets
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class AcronymViewSet(viewsets.ModelViewSet):
    queryset = Acronym.objects.all()
    serializer_class = AcronymSerializer

class FuseBoxViewSet(viewsets.ModelViewSet):
    queryset = FuseBox.objects.all()
    serializer_class = FuseBoxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vehicle__make', 'vehicle__model', 'location']

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class AuctionBidViewSet(viewsets.ModelViewSet):
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer

class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer

class BuyRequestViewSet(viewsets.ModelViewSet):
    queryset = BuyRequest.objects.all()
    serializer_class = BuyRequestSerializer

class WiringDiagramViewSet(viewsets.ModelViewSet):
    queryset = WiringDiagram.objects.all()
    serializer_class = WiringDiagramSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vehicle__make', 'vehicle__model', 'system']
