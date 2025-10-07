from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .models import Vehicle, FuseBox, SensorReading
from .serializers import VehicleSerializer, FuseBoxSerializer, SensorReadingSerializer
from .filters import VehicleFilter, FuseBoxFilter
from .utils import fetch_external_metadata
from accounts.permissions import IsAdmin, IsTechnician, IsSeller

from io import BytesIO
import csv
from reportlab.pdfgen import canvas
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

# 🏠 Unified Home View: HTML or JSON Health Check
def home(request):
    if request.headers.get('Accept') == 'text/html':
        return render(request, 'vehicles/dashboard.html')
    return JsonResponse({"status": "OK", "message": "Vehicle diagnostics API is running"})

# 🚗 Vehicle ViewSet
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VehicleFilter

# 🔌 FuseBox ViewSet
class FuseBoxViewSet(viewsets.ModelViewSet):
    queryset = FuseBox.objects.all()
    serializer_class = FuseBoxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FuseBoxFilter

# 🔍 FuseBox Lookup API
class FuseBoxLookupView(APIView):
    def get(self, request):
        make = request.query_params.get('make')
        model = request.query_params.get('model')
        year = request.query_params.get('year')

        if not (make and model and year):
            return Response(
                {"error": "Missing required query parameters: make, model, year"},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = FuseBox.objects.filter(make=make, model=model, year=year)
        serializer = FuseBoxSerializer(results, many=True)
        return Response(serializer.data)

# 📊 Sensor Chart API
class SensorChartView(APIView):
    def get(self, request):
        readings = SensorReading.objects.all().order_by('timestamp')
        data = [
            {
                'timestamp': r.timestamp.isoformat(),
                'value': r.value,
                'sensor': r.sensor_type,
                'vehicle': str(r.vehicle)
            }
            for r in readings
        ]
        return Response(data)

# 📤 CSV Export API with Token Validation
class ExportCSVView(APIView):
    authentication_classes = []  # ✅ Disable default auth
    permission_classes = []      # ✅ Disable permission check

    def get(self, request):
        token = request.GET.get('token')
        print("Received token:", token)  # Optional debug

        try:
            access = AccessToken(token)
            user_id = access['user_id']
            request.user = User.objects.get(id=user_id)
        except Exception:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sensor_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['Timestamp', 'Sensor', 'Value'])
        for r in SensorReading.objects.all():
            writer.writerow([r.timestamp.isoformat(), r.sensor_type, r.value])
        return response


# 📤 PDF Export API with Token Validation
class ExportPDFView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        token = request.GET.get('token')
        print("Received token:", token)

        try:
            access = AccessToken(token)
            user_id = access['user_id']
            request.user = User.objects.get(id=user_id)
        except Exception:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setTitle("Sensor Report")
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, "Sensor Report")

        y = 780
        for r in SensorReading.objects.all():
            line = f"{r.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {r.sensor_type}: {r.value}"
            p.drawString(100, y, line)
            y -= 20
            if y < 50:
                p.showPage()
                y = 800

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='sensor_report.pdf')


# 🚗 Vehicle Metadata API with Role-Based Access + Enrichment
class VehicleMetadataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if hasattr(user, 'role') and user.role == 'seller':
            vehicles = Vehicle.objects.filter(owner=user)
        else:
            vehicles = Vehicle.objects.all()

        enriched_data = []
        for v in vehicles:
            base = {
                "make": v.make,
                "model": v.model,
                "year": v.year,
                "vin": v.vin
            }

            external = fetch_external_metadata(v.vin)
            if external:
                base.update({
                    "engine": external.get("engine"),
                    "transmission": external.get("transmission"),
                    "country": external.get("country_of_origin")
                })

            enriched_data.append(base)

        return Response(enriched_data)
