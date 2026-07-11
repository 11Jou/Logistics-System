from django.db.models import Sum
from django.utils import timezone

from delivery.models import (
    DeleveryRunStatus,
    DeliveryRun,
    Driver,
    Status as DriverStatus,
)
from order.models import Order, Status as OrderStatus


def get_dashboard_stats():
    today = timezone.localdate()

    total_cash_today = DeliveryRun.objects.filter(
        status=DeleveryRunStatus.CASH_BANKED,
        cash_banked_at__date=today,
    ).aggregate(total_cash=Sum('total_cash_collected'))['total_cash']

    return {
        'total_open_orders': Order.objects.filter(status=OrderStatus.OPEN).count(),
        'total_completed_orders': Order.objects.filter(
            status__in=[OrderStatus.DELIVERED, OrderStatus.CASH_BANKED],
        ).count(),
        'total_active_drivers': Driver.objects.filter(
            active=True,
        ).exclude(status=DriverStatus.IN_ACTIVE).count(),
        'total_runs_drivers': DeliveryRun.objects.filter(
            status=DeleveryRunStatus.COMPLETED,
        ).count(),
        'total_cash_today': total_cash_today or 0,
    }
