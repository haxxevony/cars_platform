from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import (
    Vehicle, Part, Listing, SellerProfile, BuyRequest, AuctionBid,
    SellerFeedback, EVTelemetry, ADASCalibration, FuseBox, WiringDiagram,
    SensorReading, OBDDiagnostic, Sensor, Acronym, BlogPost,
    LegacyDiagnosticCode, LegacyGuestBlog, LegacyCarListing, LegacySellerFeedback
)

# Custom filter for sensor value ranges
class ValueRangeFilter(admin.SimpleListFilter):
    title = 'Sensor Value'
    parameter_name = 'value_range'

    def lookups(self, request, model_admin):
        return [('low', 'Low (<50)'), ('high', 'High (≥50)')]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(value__lt=50)
        if self.value() == 'high':
            return queryset.filter(value__gte=50)
        return queryset

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'price', 'seller', 'timestamp')
    search_fields = ('name', 'vehicle_make', 'vehicle_model')
    list_filter = ('vehicle_year', 'vehicle_make')

@admin.register(SellerFeedback)
class SellerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'seller', 'rating', 'timestamp')
    search_fields = ('reviewer__username', 'seller__username')
    list_filter = ('rating',)

@admin.register(EVTelemetry)
class EVTelemetryAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'battery_level', 'range_estimate_km', 'speed_kph', 'timestamp')
    list_filter = ('vehicle',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'currency', 'country', 'region', 'is_active', 'timestamp')
    search_fields = ('title', 'country', 'region')
    list_filter = ('currency', 'country', 'is_active')

@admin.register(ADASCalibration)
class ADASCalibrationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'sensor_type', 'calibrated_by', 'calibration_date', 'is_compliant')
    list_filter = ('sensor_type', 'is_compliant')
    search_fields = ('vehicle__id', 'sensor_type')

@admin.register(OBDDiagnostic)
class OBDDiagnosticAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'dtc_code', 'severity', 'timestamp')
    list_filter = ('severity', 'vehicle__make', 'vehicle__model')
    search_fields = ('dtc_code', 'description')

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location')
    list_filter = ('type',)
    search_fields = ('name', 'location')

@admin.register(Acronym)
class AcronymAdmin(admin.ModelAdmin):
    list_display = ('short_form', 'full_form')
    search_fields = ('short_form', 'full_form')

@admin.register(FuseBox)
class FuseBoxAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'location')
    list_filter = ('vehicle__make', 'vehicle__model')
    search_fields = ('location',)

@admin.register(WiringDiagram)
class WiringDiagramAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'system')
    list_filter = ('vehicle__make', 'vehicle__model')
    search_fields = ('system',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'timestamp')
    list_filter = ('published',)
    search_fields = ('title', 'author__username')

@admin.register(AuctionBid)
class AuctionBidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'amount', 'timestamp')
    list_filter = ('listing',)
    search_fields = ('bidder__username',)

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'website')
    search_fields = ('user__username',)

@admin.register(BuyRequest)
class BuyRequestAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'timestamp')
    search_fields = ('buyer__username',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'vin', 'owner')
    list_filter = ('make', 'model', 'year')
    search_fields = ('vin', 'make', 'model')

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'sensor_type', 'value', 'timestamp', 'compliance_status')
    list_filter = ('sensor_type', 'timestamp', ValueRangeFilter)
    search_fields = ('sensor_type', 'vehicle__vin')
    actions = ['export_as_csv']

    def compliance_status(self, obj):
        return "⚠️ High" if obj.value >= 80 else "✅ OK"
    compliance_status.short_description = "Compliance"

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=sensor_readings.csv'
        writer = csv.writer(response)
        writer.writerow(['Vehicle', 'Sensor Type', 'Value', 'Timestamp'])
        for obj in queryset:
            writer.writerow([obj.vehicle, obj.sensor_type, obj.value, obj.timestamp])
        return response

    export_as_csv.short_description = "Export selected as CSV"

# Register legacy models without custom admin (optional to enhance later)
admin.site.register(LegacyGuestBlog)
admin.site.register(LegacyCarListing)
admin.site.register(LegacySellerFeedback)

@admin.register(LegacyDiagnosticCode)
class LegacyDiagnosticCodeAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'dtc_code', 'severity', 'timestamp')
    list_filter = ('severity', 'vehicle__make', 'vehicle__model')
    search_fields = ('dtc_code', 'description')
