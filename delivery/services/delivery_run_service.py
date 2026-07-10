from django.db import transaction
from django.utils import timezone

from ..models import DeleveryRunStatus, Status as DriverStatus
from ..repository.delivery_run_repository import DeliveryRunRepository
from ..repository.delivery_stop_repository import DeliveryStopRepository
from ..repository.driver_repository import DriverRepository
from order.repository import OrderRepository

PRIORITY_RANK = {'high': 0, 'medium': 1, 'low': 2}


class DeliveryRunService:
    @staticmethod
    def _sequence_by_priority(orders):
        return sorted(
            orders,
            key=lambda order: (PRIORITY_RANK[order.priority], order.created_at),
        )

    @classmethod
    @transaction.atomic
    def build_run(cls, driver_id):
        driver = DriverRepository.get_available_driver(driver_id)
        if driver is None:
            raise Exception(
                'Driver does not exist or is not available'
            )

        selected_orders = OrderRepository.get_open_orders_for_update(driver.max_stops)
        ordered_orders = cls._sequence_by_priority(selected_orders)

        run = DeliveryRunRepository.create(
            driver=driver,
            status=DeleveryRunStatus.ASSIGNED,
            start_date=timezone.now(),
        )

        DeliveryStopRepository.bulk_create_for_run(run, ordered_orders)
        OrderRepository.mark_assigned([order.pk for order in selected_orders])
        DriverRepository.set_status(driver, DriverStatus.ON_RUN)

        return run
