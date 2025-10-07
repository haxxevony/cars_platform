import csv
from django.http import HttpResponse
from vehicles.models import Vehicle

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vehicles.csv"'
    writer = csv.writer(response)
    writer.writerow(['Make', 'Model', 'Year', 'VIN'])

    for v in Vehicle.objects.all():
        writer.writerow([v.make, v.model, v.year, v.vin])

    return response
