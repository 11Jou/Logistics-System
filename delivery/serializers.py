from rest_framework import serializers

from order.serializers import OrderSerializer

from .models import DeliveryRun, DeliveryStop, Driver


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class BuildDeliveryRunSerializer(serializers.Serializer):
    driver_id = serializers.IntegerField()


class DeliveryStopSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = DeliveryStop
        fields = ['id', 'order', 'stop_sequence', 'stop_status', 'delivered_at', 'failed_reason']


class DeliveryRunSerializer(serializers.ModelSerializer):
    stops = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryRun
        fields = [
            'id',
            'driver',
            'status',
            'total_cash_collected',
            'start_date',
            'completed_at',
            'cash_banked_at',
            'stops',
        ]

    def get_stops(self, obj):
        stops = obj.deliverystop_set.all().order_by('stop_sequence')
        return DeliveryStopSerializer(stops, many=True).data
