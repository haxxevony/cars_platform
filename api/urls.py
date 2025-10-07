from django.urls import path
from .views import generate_pdf
from .views import (
    UserListView,
    AuditLogListView,
    NotificationListView,
    EVTelemetryListView
)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('users/', UserListView.as_view(), name='api-users'),
    path('audit/', AuditLogListView.as_view(), name='api-audit'),
    path('notifications/', NotificationListView.as_view(), name='api-notifications'),
    path('ev-telemetry/', EVTelemetryListView.as_view(), name='api-ev-telemetry'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('export/pdf/', generate_pdf, name='generate_pdf'),
]
