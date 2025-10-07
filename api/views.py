from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from audit.models import AuditLog
from notifications.models import Notification
from vehicles.models import EVTelemetry
from api.serializers import (
    CustomUserSerializer,
    AuditLogSerializer,
    NotificationSerializer,
    EVTelemetrySerializer
)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

class EVTelemetryListView(generics.ListAPIView):
    queryset = EVTelemetry.objects.all()
    serializer_class = EVTelemetrySerializer
    permission_classes = [IsAuthenticated]

# --- PDF Export View ---
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf(request):
    user = request.user
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"diagnostics_{user.username}_{timestamp}.pdf"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    p = canvas.Canvas(response)
    p.setTitle("Diagnostics Report")
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Hello {user.username}, your diagnostics report is ready.")
    p.drawString(100, 730, f"Role: {user.role}")
    p.drawString(100, 710, "This PDF was generated dynamically using ReportLab.")
    p.drawString(100, 690, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p.showPage()
    p.save()

    return response
