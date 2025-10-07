from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (  # ✅ Use api_views.py, not .api
    VehicleViewSet, PartViewSet, ListingViewSet, SellerProfileViewSet,
    BuyRequestViewSet, AuctionBidViewSet, SellerFeedbackViewSet,
    EVTelemetryViewSet, ADASCalibrationViewSet, FuseBoxViewSet,
    WiringDiagramViewSet, SensorReadingViewSet, OBDDiagnosticViewSet,
    SensorViewSet, AcronymViewSet, BlogPostViewSet,
    LegacyDiagnosticCodeViewSet, LegacyGuestBlogViewSet,
    LegacyCarListingViewSet, LegacySellerFeedbackViewSet
)
from .views import (
    home,
    VehicleMetadataView,
    FuseBoxLookupView,
    SensorChartView,
    ExportCSVView,
    ExportPDFView,
)

# Register all viewsets with DRF router
router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'parts', PartViewSet)
router.register(r'listings', ListingViewSet)
router.register(r'sellerprofiles', SellerProfileViewSet)
router.register(r'buyrequests', BuyRequestViewSet)
router.register(r'auctions', AuctionBidViewSet)
router.register(r'feedback', SellerFeedbackViewSet)
router.register(r'telemetry', EVTelemetryViewSet)
router.register(r'adas', ADASCalibrationViewSet)
router.register(r'fuseboxes', FuseBoxViewSet)
router.register(r'wiringdiagrams', WiringDiagramViewSet)
router.register(r'sensorreadings', SensorReadingViewSet)
router.register(r'obd', OBDDiagnosticViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'acronyms', AcronymViewSet)
router.register(r'blogposts', BlogPostViewSet)
router.register(r'legacy/dtc', LegacyDiagnosticCodeViewSet)
router.register(r'legacy/blogs', LegacyGuestBlogViewSet)
router.register(r'legacy/listings', LegacyCarListingViewSet)
router.register(r'legacy/feedback', LegacySellerFeedbackViewSet)

# Combine router URLs and custom views
urlpatterns = [
    path('', home, name='vehicle-home'),  # Health check or homepage
    path('api/', include(router.urls)),   # All viewsets under /api/
    path('metadata/', VehicleMetadataView.as_view(), name='vehicle-metadata'),
    path('fusebox/', FuseBoxLookupView.as_view(), name='fusebox-lookup'),
    path('sensor-chart/', SensorChartView.as_view(), name='sensor-chart'),
    path('export/csv/', ExportCSVView.as_view(), name='export-csv'),
    path('export/pdf/', ExportPDFView.as_view(), name='export-pdf'),
]
