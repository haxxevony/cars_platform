import pandas as pd
from django.core.management.base import BaseCommand
from vehicles.models import OBDDiagnostic, Sensor, Acronym, Vehicle

class Command(BaseCommand):
    help = "Seed OBD codes, sensors, and acronyms from Excel files"

    def handle(self, *args, **kwargs):
        # Dummy vehicle for linking diagnostics
        vehicle = Vehicle.objects.first()
        if not vehicle:
            self.stdout.write(self.style.ERROR("No vehicles found. Add one first."))
            return

        # 1. Seed OBDDiagnostic from CVS.xlsx
        try:
            df_obd = pd.read_excel('CVS.xlsx')
            for _, row in df_obd.iterrows():
                OBDDiagnostic.objects.create(
                    vehicle=vehicle,
                    dtc_code=row['dtc_code'],
                    description=row['description'],
                    severity=row['severity']
                )
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(df_obd)} OBD codes."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"OBD error: {e}"))

        # 2. Seed Sensor from sensors.xlsx
        try:
            df_sensors = pd.read_excel('sensors.xlsx')
            for _, row in df_sensors.iterrows():
                Sensor.objects.create(
                    name=row['name'],
                    type=row['type'],
                    location=row['location'],
                    function=row['function']
                )
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(df_sensors)} sensors."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Sensor error: {e}"))

        # 3. Seed Acronym from acronyms.xlsx
        try:
            df_acronyms = pd.read_excel('acronyms.xlsx')
            for _, row in df_acronyms.iterrows():
                Acronym.objects.create(
                    short_form=row['short_form'],
                    full_form=row['full_form'],
                    description=row['description']
                )
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(df_acronyms)} acronyms."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Acronym error: {e}"))
