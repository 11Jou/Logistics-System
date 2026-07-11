from django.urls import path

from .views import *

urlpatterns = [
    # Dispatcher and Manager actions
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('build-run/', BuildDeliveryRunView.as_view(), name='build-delivery-run'),
    path('runs/', DeliveryRunListView.as_view(), name='delivery-run-list'),
    path('runs/<int:pk>/start/', DeliveryRunStartView.as_view(), name='delivery-run-start'),
    path('runs/<int:pk>/cash-banked/', DeliveryRunCashBankedView.as_view(), name='delivery-run-cash-banked'),


    # Driver actions
    path('runs/driver/', DriverDeliveryRunListView.as_view(), name='driver-delivery-run-list'),
    path('runs/driver/<int:pk>/', DriverDeliveryRunDetailView.as_view(), name='driver-delivery-run-detail'),
    path('runs/driver/<int:pk>/stops/<int:stop_pk>/start/', DriverDeliveryStopStartView.as_view(), name='driver-delivery-stop-start'),
    path('runs/driver/<int:pk>/stops/<int:stop_pk>/delivered/', DriverDeliveryStopDeliveredView.as_view(), name='driver-delivery-stop-delivered'),
    path('runs/driver/<int:pk>/stops/<int:stop_pk>/failed/', DriverDeliveryStopFailedView.as_view(), name='driver-delivery-stop-failed'),
    path('runs/driver/<int:pk>/complete/', DriverDeliveryRunCompleteView.as_view(), name='driver-delivery-run-complete'),
]