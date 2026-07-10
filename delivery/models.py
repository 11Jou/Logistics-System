from django.db import models
from authentication.models import User
from order.models import Order


class Status(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    ON_RUN = 'on_run', 'On Run'
    IN_ACTIVE = 'in_active', 'In Active'


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    active = models.BooleanField(default=True)
    max_stops = models.IntegerField(default=1)
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"


class DeleveryRunStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ASSIGNED = 'assigned', 'Assigned'
    EN_ROUTE = 'en_route', 'En Route'
    COMPLETED = 'completed', 'Completed'
    CASH_BANKED = 'cash_banked', 'Cash Banked'
    CANCELLED = 'cancelled', 'Cancelled'


class DeliveryRun(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=DeleveryRunStatus.choices, default=DeleveryRunStatus.DRAFT)
    total_cash_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    cash_banked_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.driver.name} - {self.status}"
        


class DeleveryStopStatus(models.TextChoices):
    ASSIGNED = 'assigned', 'Assigned'
    EN_ROUTE = 'en_route', 'En Route'
    DELIVERED = 'delivered', 'Delivered'
    FAILED = 'failed', 'Failed'


class DeliveryStop(models.Model):
    delivery_run = models.ForeignKey(DeliveryRun, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stop_sequence = models.IntegerField(default=0)
    stop_status = models.CharField(choices=DeleveryStopStatus.choices, default=DeleveryStopStatus.ASSIGNED)
    delivered_at = models.DateTimeField(null=True, blank=True)
    failed_reason = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.order.address}"