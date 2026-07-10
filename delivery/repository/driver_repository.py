from ..models import Driver, Status


class DriverRepository:
    @staticmethod
    def get_all_ordered():
        return Driver.objects.all().order_by('-created_at')

    @staticmethod
    def get_available_driver(driver_id):
        return Driver.objects.filter(
            pk=driver_id,
            active=True,
            status=Status.AVAILABLE,
        ).first()

    @staticmethod
    def set_status(driver, status):
        driver.status = status
        driver.save(update_fields=['status'])
        return driver
