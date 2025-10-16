from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

class Vehicle(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    vin = models.CharField(max_length=17, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['vin']), models.Index(fields=['make', 'model'])]

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) - {self.vin}"

class Part(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parts')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_year = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['vehicle_make', 'vehicle_model', 'vehicle_year'])]

    def __str__(self):
        return f"{self.name} for {self.vehicle_make} {self.vehicle_model} ({self.vehicle_year})"

class Listing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')])
    location = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['is_active', 'location'])]

    def __str__(self):
        return f"{self.title} - {self.price} {self.currency}"

class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    rating = models.FloatField(default=0.0)
    website = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Seller Profile'
        verbose_name_plural = 'Seller Profiles'

    def __str__(self):
        return f"{self.user.email} - {self.company_name or 'No Company'}"

class BuyRequest(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buy_requests')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='buy_requests')
    message = models.TextField(blank=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['buyer', 'listing'])]

    def __str__(self):
        return f"Buy Request for {self.listing.title} by {self.buyer.email}"

class AuctionBid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='auction_bids')
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auction_bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['listing', 'bidder'])]

    def __str__(self):
        return f"Bid of {self.amount} on {self.listing.title} by {self.bidder.email}"

class SellerFeedback(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_received')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_given')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['seller', 'reviewer'])]

    def __str__(self):
        return f"Feedback for {self.seller.email} by {self.reviewer.email} ({self.rating})"

class EVTelemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='telemetry')
    battery_level = models.FloatField()
    range_estimate_km = models.FloatField()
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    speed_kph = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['vehicle', 'timestamp'])]

    def __str__(self):
        return f"Telemetry for {self.vehicle.vin} at {self.timestamp}"

class ADASCalibration(models.Model):
    SENSOR_TYPES = [
        ('radar', 'Radar'),
        ('lidar', 'Lidar'),
        ('camera', 'Camera'),
        ('ultrasonic', 'Ultrasonic'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='adas_calibrations')
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    calibrated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='calibrations_performed')
    calibration_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    is_compliant = models.BooleanField(default=True)

    class Meta:
        ordering = ['-calibration_date']
        indexes = [models.Index(fields=['vehicle', 'sensor_type'])]

    def __str__(self):
        return f"{self.sensor_type} Calibration for {self.vehicle.vin}"

class FuseBox(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True, related_name='fuse_boxes')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=100)
    diagram_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=['make', 'model', 'year'])]

    def __str__(self):
        return f"FuseBox for {self.make} {self.model} ({self.year})"

class WiringDiagram(models.Model):
    SYSTEM_TYPES = [
        ('electrical', 'Electrical'),
        ('lighting', 'Lighting'),
        ('audio', 'Audio'),
        ('engine', 'Engine'),
        ('hvac', 'HVAC'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='wiring_diagrams')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='diagrams/images/', blank=True, null=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    diagram_file = models.FileField(upload_to='diagrams/files/', blank=True, null=True)
    system = models.CharField(max_length=20, choices=SYSTEM_TYPES, blank=True, null=True)

    class Meta:
        ordering = ['-uploaded_at']
        indexes = [models.Index(fields=['vehicle', 'system'])]

    def __str__(self):
        return f"{self.title} for {self.vehicle.vin}"

class SensorReading(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='sensor_readings')
    sensor_type = models.CharField(max_length=50)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['vehicle', 'sensor_type'])]

    def __str__(self):
        return f"{self.sensor_type} Reading for {self.vehicle.vin}: {self.value}"

class OBDDiagnostic(models.Model):
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='obd_diagnostics')
    dtc_code = models.CharField(max_length=5)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['vehicle', 'dtc_code'])]

    def __str__(self):
        return f"OBD {self.dtc_code} for {self.vehicle.vin}"

class Sensor(models.Model):
    SENSOR_TYPES = [
        ('temperature', 'Temperature'),
        ('pressure', 'Pressure'),
        ('speed', 'Speed'),
        ('proximity', 'Proximity'),
        ('oxygen', 'Oxygen'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    location = models.CharField(max_length=100)

    class Meta:
        indexes = [models.Index(fields=['type'])]

    def __str__(self):
        return f"{self.name} ({self.type})"

class Acronym(models.Model):
    short_form = models.CharField(max_length=20, unique=True)
    full_form = models.CharField(max_length=200)

    class Meta:
        indexes = [models.Index(fields=['short_form'])]

    def __str__(self):
        return f"{self.short_form}: {self.full_form}"

class LegacyDiagnosticCode(models.Model):
    code = models.CharField(max_length=10, unique=True, default='UNKNOWN')  # ✅ Add default
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['code'])]

    def __str__(self):
        return f"{self.code}: {self.description}"


class LegacyGuestBlog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class LegacyCarListing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='legacy_listings')
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)

    class Meta:
        indexes = [models.Index(fields=['seller'])]

    def __str__(self):
        return f"{self.title} - {self.price}"

class LegacySellerFeedback(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='legacy_feedback_received')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='legacy_feedback_given')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['seller', 'reviewer'])]

    def __str__(self):
        return f"Legacy Feedback for {self.seller.email} by {self.reviewer.email} ({self.rating})"