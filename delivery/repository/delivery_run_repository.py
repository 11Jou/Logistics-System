from ..models import DeliveryRun


class DeliveryRunRepository:
    @staticmethod
    def get_all_with_driver():
        return (
            DeliveryRun.objects.all()
            .select_related('driver')
            .order_by('-start_date')
        )

    @staticmethod
    def create(driver, status, start_date):
        return DeliveryRun.objects.create(
            driver=driver,
            status=status,
            start_date=start_date,
        )
