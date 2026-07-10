import django_filters

from .models import Order, Priority, Status


class OrderFilter(django_filters.FilterSet):
    priority = django_filters.ChoiceFilter(choices=Priority.choices)
    status = django_filters.ChoiceFilter(choices=Status.choices)

    class Meta:
        model = Order
        fields = ['priority', 'status']
