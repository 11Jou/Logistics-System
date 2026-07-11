from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    total_open_orders = serializers.IntegerField()
    total_completed_orders = serializers.IntegerField()
    total_active_drivers = serializers.IntegerField()
    total_runs_drivers = serializers.IntegerField()
    total_cash_today = serializers.DecimalField(max_digits=10, decimal_places=2)
