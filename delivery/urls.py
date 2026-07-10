from django.urls import path

from .views import BuildDeliveryRunView, DeliveryRunListView, DriverListView

urlpatterns = [
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('build-run/', BuildDeliveryRunView.as_view(), name='build-delivery-run'),
    path('runs/', DeliveryRunListView.as_view(), name='delivery-run-list'),
]