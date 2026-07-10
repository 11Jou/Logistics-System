from django.db import transaction
from django.utils import timezone
from order.models import Order, Status as OrderStatus
from ..models import DeleveryRunStatus, DeliveryRun, DeliveryStop, Driver, Status as DriverStatus

PRIORITY_RANK = {'high': 0, 'medium': 1, 'low': 2}


def _sequence_by_priority(orders):
    return sorted(
        orders,
        key=lambda order: (PRIORITY_RANK[order.priority], order.created_at),
    )


@transaction.atomic
def build_run(driver_id):
    driver = Driver.objects.filter(
        pk=driver_id,
        active=True,
        status=DriverStatus.AVAILABLE,).first()
    if driver is None:
        raise Exception('Driver does not exist or is not available')

    selected_orders = list(
        Order.objects.select_for_update()
        .filter(status=OrderStatus.OPEN)
        .order_by('created_at')[:driver.max_stops])

    ordered_orders = _sequence_by_priority(selected_orders)

    run = DeliveryRun.objects.create(driver=driver,
        status=DeleveryRunStatus.ASSIGNED,
        start_date=timezone.now(),)

    DeliveryStop.objects.bulk_create([
        DeliveryStop(
            delivery_run=run,
            order=order,
            stop_sequence=sequence,)
        for sequence, order in enumerate(ordered_orders, start=1)])

    if selected_orders:
        Order.objects.filter(pk__in=[order.pk for order in selected_orders]).update(status=OrderStatus.ASSIGNED)

    driver.status = DriverStatus.ON_RUN
    driver.save(update_fields=['status'])

    return run
