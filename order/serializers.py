from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        if attrs['cash_amount'] < 0:
            raise serializers.ValidationError({'cash_amount': 'Cash amount must be positive'})
        return attrs
