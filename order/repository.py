from .models import Order, Status as OrderStatus


class OrderRepository:
    @staticmethod
    def get_open_orders_for_update(limit):
        return list(
            Order.objects.select_for_update()
            .filter(status=OrderStatus.OPEN)
            .order_by('created_at')[:limit]
        )

    @staticmethod
    def mark_assigned(order_ids):
        if not order_ids:
            return 0
        return Order.objects.filter(pk__in=order_ids).update(
            status=OrderStatus.ASSIGNED
        )
