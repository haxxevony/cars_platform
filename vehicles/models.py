from django.db import models
from django.conf import settings
from django.utils import timezone

# 🚗 Vehicle
class Vehicle(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='vehicles'
    )
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    vin = models.CharField(max_length=17, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['vin']),
            models.Index(fields=['make', 'model', 'year']),
        ]

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

# 🧩 Part
class Part(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_year = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.name} for {self.vehicle_make} {self.vehicle_model} ({self.vehicle_year})"

# 📦 Listing
class Listing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

# 🧑‍💼 Seller Profile
class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name or self.user.username

# 📥 Buy Request
class BuyRequest(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.buyer} → {self.listing} @ {self.offer_price}"

# 🏷️ Auction Bid
class AuctionBid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.bidder} bid {self.amount} on {self.listing}"

# ⭐ Seller Feedback
class SellerFeedback(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_received')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_given')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.reviewer} → {self.seller} ({self.rating})"

# ⚡ EV Telemetry
class EVTelemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    battery_level = models.DecimalField(max_digits=5, decimal_places=2)
    range_estimate_km = models.PositiveIntegerField()
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    speed_kph = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.vehicle} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

# 🛠️ ADAS Calibration
class ADASCalibration(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=50)
    calibrated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    calibration_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    is_compliant = models.BooleanField(default=False)

    class Meta:
        ordering = ['-calibration_date']

    def __str__(self):
        status = '✔' if self.is_compliant else '✘'
        return f"{self.sensor_type} for {self.vehicle} ({status})"

# 🔌 Fuse Box
class FuseBox(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    make = models.CharField(max_length=50, default='Unknown')
    model = models.CharField(max_length=50, default='Generic')
    year = models.PositiveIntegerField(default=2000)
    location = models.CharField(max_length=100)
    diagram_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('make', 'model', 'year', 'location')
        ordering = ['make', 'model', 'year']

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) FuseBox @ {self.location}"

# 🧷 Wiring Diagram
class WiringDiagram(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Untitled Diagram')
    image = models.ImageField(upload_to='wiring_diagrams/', default='wiring_diagrams/default.jpg')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    diagram_file = models.FileField(upload_to='diagrams/', blank=True, null=True)
    system = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.vehicle} - {self.system or self.title}"

# 📊 Sensor Reading
class SensorReading(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=50)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor_type} for {self.vehicle} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

# 🧠 OBD Diagnostic
class OBDDiagnostic(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    dtc_code = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.vehicle} - {self.dtc_code}"

# 📡 Sensor
class Sensor(models.Model):
    SENSOR_TYPES = [
        ('temperature', 'Temperature'),
        ('pressure', 'Pressure'),
        ('voltage', 'Voltage'),
        ('current', 'Current'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.type})"

# 🔤 Acronym
class Acronym(models.Model):
    short_form = models.CharField(max_length=20, unique=True)
    full_form = models.CharField(max_length=255)

    class Meta:
        ordering = ['short_form']

    def __str__(self):
        return f"{self.short_form} → {self.full_form}"

# 📝 Blog Post
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    content = models.TextField()
    published = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title
# 🧠 Legacy Diagnostic Code
class LegacyDiagnosticCode(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    dtc_code = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.vehicle} - {self.dtc_code} ({self.severity})"

# 📝 Legacy Guest Blog
class LegacyGuestBlog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

# 📦 Legacy Car Listing
class LegacyCarListing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.title} ({self.currency} {self.price})"

# ⭐ Legacy Seller Feedback
class LegacySellerFeedback(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.seller} ({self.rating})"

