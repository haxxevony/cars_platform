# Cleaned version of 0004_alter_fusebox_options_and_more.py

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_acronym_sensor_wiringdiagram_sellerprofile_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fusebox',
            options={'ordering': ['make', 'model', 'year']},
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='offer_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fusebox',
            name='make',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='fusebox',
            name='model',
            field=models.CharField(default='Generic', max_length=50),
        ),
        migrations.AlterField(
            model_name='fusebox',
            name='year',
            field=models.PositiveIntegerField(default=2000),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='company_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='contact_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='wiringdiagram',
            name='diagram_file',
            field=models.FileField(blank=True, null=True, upload_to='diagrams/'),
        ),
        migrations.AlterField(
            model_name='wiringdiagram',
            name='image',
            field=models.ImageField(default='wiring_diagrams/default.jpg', upload_to='wiring_diagrams/'),
        ),
        migrations.AlterField(
            model_name='wiringdiagram',
            name='title',
            field=models.CharField(default='Untitled Diagram', max_length=200),
        ),
        migrations.AlterField(
            model_name='wiringdiagram',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='acronym',
            name='full_form',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='acronym',
            name='short_form',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='auctionbid',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='author',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='message',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fusebox',
            name='diagram_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fusebox',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicles.vehicle'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='listing',
            name='currency',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='region',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='obddiagnostic',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='obddiagnostic',
            name='dtc_code',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='obddiagnostic',
            name='severity',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=20),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='type',
            field=models.CharField(choices=[('temperature', 'Temperature'), ('pressure', 'Pressure'), ('voltage', 'Voltage'), ('current', 'Current')], max_length=20),
        ),
        migrations.AlterField(
            model_name='wiringdiagram',
            name='system',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='fusebox',
            unique_together={('make', 'model', 'year', 'location')},
        ),
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_type', models.CharField(max_length=50)),
                ('value', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicles.vehicle')),
            ],
        ),
    ]
