from django.db import transaction
from django.utils import timezone

from order.models import Order, Status as OrderStatus

from ..models import (
    DeleveryRunStatus,
    DeleveryStopStatus,
    DeliveryRun,
    DeliveryStop,
    Driver,
    Status as DriverStatus,
)
from .helpers import get_driver_for_user, get_driver_run

PRIORITY_RANK = {'high': 0, 'medium': 1, 'low': 2}


def _sequence_by_priority(orders):
    return sorted(
        orders,
        key=lambda order: (PRIORITY_RANK[order.priority], order.created_at),
    )


def _validate_all_stops_finished(run):
    unfinished_stops = DeliveryStop.objects.filter(
        delivery_run=run,
    ).exclude(
        stop_status__in=[DeleveryStopStatus.DELIVERED, DeleveryStopStatus.FAILED],
    ).exists()

    if unfinished_stops:
        raise Exception('All delivery stops must be delivered or failed before completing the run')


@transaction.atomic
def build_run(driver_id):
    driver = Driver.objects.filter(
        pk=driver_id,
        active=True,
        status=DriverStatus.AVAILABLE,
    ).first()
    if driver is None:
        raise Exception('Driver does not exist or is not available')

    selected_orders = list(
        Order.objects.select_for_update()
        .filter(status=OrderStatus.OPEN)
        .order_by('created_at')[:driver.max_stops]
    )

    ordered_orders = _sequence_by_priority(selected_orders)

    run = DeliveryRun.objects.create(
        driver=driver,
        status=DeleveryRunStatus.ASSIGNED,
        start_date=timezone.now(),
    )

    DeliveryStop.objects.bulk_create([
        DeliveryStop(
            delivery_run=run,
            order=order,
            stop_sequence=sequence,
        )
        for sequence, order in enumerate(ordered_orders, start=1)
    ])

    if selected_orders:
        Order.objects.filter(
            pk__in=[order.pk for order in selected_orders]
        ).update(status=OrderStatus.ASSIGNED)

    driver.status = DriverStatus.ON_RUN
    driver.save(update_fields=['status'])

    return run


def complete_run(user, run_id):
    driver = get_driver_for_user(user)
    run = get_driver_run(driver, run_id)

    if run.status != DeleveryRunStatus.EN_ROUTE:
        raise Exception('Delivery run must be in en route status')

    _validate_all_stops_finished(run)

    with transaction.atomic():
        run.status = DeleveryRunStatus.COMPLETED
        run.completed_at = timezone.now()
        run.save(update_fields=['status', 'completed_at'])

        driver.status = DriverStatus.AVAILABLE
        driver.save(update_fields=['status'])

    return run

@transaction.atomic
def cash_banked_run(run_id):
    try:
        run = DeliveryRun.objects.prefetch_related(
            'deliverystop_set__order',
        ).get(pk=run_id)
    except DeliveryRun.DoesNotExist:
        raise Exception('Delivery run not found')

    if run.status != DeleveryRunStatus.COMPLETED:
        raise Exception('Delivery run must be in completed status')

    for stop in run.deliverystop_set.all():
        if stop.stop_status == DeleveryStopStatus.FAILED:
            continue

        if stop.stop_status != DeleveryStopStatus.DELIVERED:
            raise Exception('All delivery stops must be delivered or failed before cash banking')

        if stop.order.status != OrderStatus.DELIVERED:
            raise Exception('Delivered stops must have orders in delivered status before cash banking')

        stop.order.status = OrderStatus.CASH_BANKED
        stop.order.save(update_fields=['status'])

    run.status = DeleveryRunStatus.CASH_BANKED
    run.cash_banked_at = timezone.now()
    run.save(update_fields=['status', 'cash_banked_at'])

    return run

