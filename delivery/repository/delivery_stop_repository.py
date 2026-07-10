from ..models import DeliveryStop


class DeliveryStopRepository:
    @staticmethod
    def bulk_create_for_run(delivery_run, ordered_orders):
        stops = [
            DeliveryStop(
                delivery_run=delivery_run,
                order=order,
                stop_sequence=sequence,
            )
            for sequence, order in enumerate(ordered_orders, start=1)
        ]
        return DeliveryStop.objects.bulk_create(stops)
