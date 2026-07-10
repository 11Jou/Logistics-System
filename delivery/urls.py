from django.urls import path

from .views import *

urlpatterns = [
    # Dispatcher and Manager actions
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('build-run/', BuildDeliveryRunView.as_view(), name='build-delivery-run'),
    path('runs/', DeliveryRunListView.as_view(), name='delivery-run-list'),
    path('runs/<int:pk>/start/', DeliveryRunStartView.as_view(), name='delivery-run-start'),
]