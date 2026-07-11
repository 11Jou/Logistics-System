from ..models import DeliveryRun, DeliveryStop, Driver


def get_driver_for_user(user):
    try:
        return Driver.objects.get(user=user)
    except Driver.DoesNotExist:
        raise Exception('No driver profile linked to this user')


def get_driver_stop(driver, run_id, stop_id):
    try:
        return DeliveryStop.objects.select_related(
            'order',
            'delivery_run',
            'delivery_run__driver',
        ).get(
            pk=stop_id,
            delivery_run_id=run_id,
            delivery_run__driver=driver,
        )
    except DeliveryStop.DoesNotExist:
        raise Exception('Delivery stop not found or does not belong to this driver')


def get_driver_run(driver, run_id):
    try:
        return DeliveryRun.objects.select_related('driver').get(
            pk=run_id,
            driver=driver,
        )
    except DeliveryRun.DoesNotExist:
        raise Exception('Delivery run not found or does not belong to this driver')
