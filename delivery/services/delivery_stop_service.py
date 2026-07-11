from django.db import transaction
from django.utils import timezone

from order.models import Status as OrderStatus

from ..models import DeleveryStopStatus, DeliveryStop
from .helpers import get_driver_for_user, get_driver_stop


def _validate_stop_is_ready(stop):
    if stop.stop_status != DeleveryStopStatus.ASSIGNED:
        raise Exception('Delivery stop must be in assigned status')

    another_en_route = DeliveryStop.objects.filter(
        delivery_run=stop.delivery_run,
        stop_status=DeleveryStopStatus.EN_ROUTE,
    ).exclude(pk=stop.pk).exists()

    if another_en_route:
        raise Exception('Another delivery stop is already en route')


def _validate_stop_sequence_order(stop):
    previous_incomplete = DeliveryStop.objects.filter(
        delivery_run=stop.delivery_run,
        stop_sequence__lt=stop.stop_sequence,
    ).exclude(
        stop_status__in=[DeleveryStopStatus.DELIVERED, DeleveryStopStatus.FAILED],
    ).exists()

    if previous_incomplete:
        raise Exception('Driver must follow the stop sequence order')

@transaction.atomic
def start_stop(user, run_id, stop_id):
    driver = get_driver_for_user(user)
    stop = get_driver_stop(driver, run_id, stop_id)

    _validate_stop_is_ready(stop)
    _validate_stop_sequence_order(stop)

    stop.stop_status = DeleveryStopStatus.EN_ROUTE
    stop.save(update_fields=['stop_status'])

    stop.order.status = OrderStatus.EN_ROUTE
    stop.order.save(update_fields=['status'])

    return stop


@transaction.atomic
def deliver_stop(user, run_id, stop_id):
    driver = get_driver_for_user(user)
    stop = get_driver_stop(driver, run_id, stop_id)

    if stop.stop_status != DeleveryStopStatus.EN_ROUTE:
        raise Exception('Delivery stop must be in en route status')

    stop.stop_status = DeleveryStopStatus.DELIVERED
    stop.delivered_at = timezone.now()
    stop.save(update_fields=['stop_status', 'delivered_at'])

    stop.delivery_run.total_cash_collected += stop.order.cash_amount
    stop.delivery_run.save(update_fields=['total_cash_collected'])

    stop.order.status = OrderStatus.DELIVERED
    stop.order.save(update_fields=['status'])

    return stop


@transaction.atomic
def fail_stop(user, run_id, stop_id, failed_reason):
    driver = get_driver_for_user(user)
    stop = get_driver_stop(driver, run_id, stop_id)

    if stop.stop_status != DeleveryStopStatus.EN_ROUTE:
        raise Exception('Delivery stop must be in en route status')

    stop.stop_status = DeleveryStopStatus.FAILED
    stop.failed_reason = failed_reason
    stop.save(update_fields=['stop_status', 'failed_reason'])

    stop.order.status = OrderStatus.FAILED
    stop.order.save(update_fields=['status'])

    return stop
