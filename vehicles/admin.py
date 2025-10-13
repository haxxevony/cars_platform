from django.contrib import admin
from .models import (
    Vehicle, Part, Listing, SellerProfile, BuyRequest, AuctionBid, SellerFeedback,
    EVTelemetry, ADASCalibration, FuseBox, WiringDiagram, SensorReading, OBDDiagnostic,
    Sensor, Acronym, LegacyDiagnosticCode, LegacyGuestBlog, LegacyCarListing, LegacySellerFeedback
)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'vin', 'owner', 'created_at')
    list_filter = ('make', 'model', 'year')
    search_fields = ('vin', 'make', 'model')
    readonly_fields = ('created_at',)
    list_per_page = 25

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'price', 'seller', 'timestamp')
    list_filter = ('vehicle_make', 'vehicle_model', 'vehicle_year')
    search_fields = ('name', 'description')
    readonly_fields = ('timestamp',)
    list_per_page = 25

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'currency', 'location', 'is_active', 'timestamp')
    list_filter = ('is_active', 'currency', 'location')
    search_fields = ('title', 'description')
    readonly_fields = ('timestamp',)
    list_per_page = 25

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'rating', 'contact_number')
    list_filter = ('rating',)
    search_fields = ('company_name', 'user__email')
    readonly_fields = ('rating',)
    list_per_page = 25

@admin.register(BuyRequest)
class BuyRequestAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'offer_price', 'is_approved', 'timestamp')
    list_filter = ('is_approved',)
    search_fields = ('listing__title', 'buyer__email', 'message')
    readonly_fields = ('timestamp',)
    list_per_page = 25

@admin.register(AuctionBid)
class AuctionBidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'amount', 'timestamp')
    list_filter = ('listing',)
    search_fields = ('listing__title', 'bidder__email')
    readonly_fields = ('timestamp',)
    list_per_page = 25

@admin.register(SellerFeedback)
class SellerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('seller', 'reviewer', 'rating', 'timestamp')
    list_filter = ('rating',)
    search_fields = ('seller__email', 'reviewer__email', 'comment')
    readonly_fields = ('timestamp',)
    list_per_page = 25

@admin.register(EVTelemetry)
class EVTelemetryAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'battery_level', 'range_estimate_km', 'speed_kph', 'timestamp')
    list_filter = ('vehicle',)
    search_fields = ('vehicle__vin',)
    readonly_fields = ('timestamp',)
    list_per_page = 25

@admin.register(ADASCalibration)
class ADASCalibrationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'sensor_type', 'calibrated_by', 'calibration_date', 'is_compliant')
    list_filter = ('sensor_type', 'is_compliant')
    search_fields = ('vehicle__vin', 'notes')
    readonly_fields = ('calibration_date',)
    list_per_page = 25

@admin.register(FuseBox)
class FuseBoxAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'make', 'model', 'year', 'location')
    list_filter = ('make', 'model', 'year')
    search_fields = ('vehicle__vin', 'location', 'notes')
    list_per_page = 25

@admin.register(WiringDiagram)
class WiringDiagramAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'title', 'system', 'uploaded_at')
    list_filter = ('system',)
    search_fields = ('title', 'vehicle__vin', 'description')
    readonly_fields = ('uploaded_at',)
    list_per_page = 25

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'sensor_type', 'value', 'timestamp')
    list_filter = ('sensor_type',)
    search_fields = ('vehicle__vin', 'sensor_type')
    readonly_fields = ('timestamp',)
    list_per_page = 25

@admin.register(OBDDiagnostic)
class OBDDiagnosticAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'dtc_code', 'severity', 'timestamp')
    list_filter = ('severity',)
    search_fields = ('dtc_code', 'vehicle__vin', 'description')
    readonly_fields = ('timestamp',)
    list_per_page = 25

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location')
    list_filter = ('type',)
    search_fields = ('name', 'location')
    list_per_page = 25

@admin.register(Acronym)
class AcronymAdmin(admin.ModelAdmin):
    list_display = ('short_form', 'full_form')
    search_fields = ('short_form', 'full_form')
    list_per_page = 25

@admin.register(LegacyDiagnosticCode)
class LegacyDiagnosticCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'timestamp')
    search_fields = ('code', 'description')
    readonly_fields = ('timestamp',)
    list_per_page = 25

@admin.register(LegacyGuestBlog)
class LegacyGuestBlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author', 'content')
    readonly_fields = ('published_date', 'slug')
    prepopulated_fields = {'slug': ('title',)}  # ✅ enhancement
    list_per_page = 25

@admin.register(LegacyCarListing)
class LegacyCarListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'location')
    search_fields = ('title', 'location')
    list_per_page = 25

@admin.register(LegacySellerFeedback)
class LegacySellerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('seller', 'reviewer', 'rating', 'timestamp')
    list_filter = ('rating',)
    search_fields = ('seller__email', 'reviewer__email', 'comment')
    readonly_fields = ('timestamp',)
    list_per_page = 25