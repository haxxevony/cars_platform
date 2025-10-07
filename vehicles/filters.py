import django_filters
from .models import FuseBox, Vehicle

class FuseBoxFilter(django_filters.FilterSet):
    make = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter()

    class Meta:
        model = FuseBox
        fields = ['make', 'model', 'year']

class VehicleFilter(django_filters.FilterSet):
    make = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter()

    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year']
