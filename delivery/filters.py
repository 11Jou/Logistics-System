import django_filters
from .models import Driver, Status

class DriverFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Status.choices)
    active = django_filters.BooleanFilter()

    class Meta:
        model = Driver
        fields = ['status', 'active']
