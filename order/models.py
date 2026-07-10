from django.db import models

class Priority(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'

class Status(models.TextChoices):
    OPEN = 'open', 'Open'
    ASSIGNED = 'assigned', 'Assigned'
    EN_ROUTE = 'en_route', 'En Route'
    DELIVERED = 'delivered', 'Delivered'
    FAILED = 'failed', 'Failed'
    CASH_BANKED = 'cash_banked', 'Cash Banked'

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=11)
    address = models.TextField()
    cash_amount = models.DecimalField(max_digits=10, decimal_places=2)
    priority = models.CharField(choices=Priority.choices, default=Priority.LOW)
    status = models.CharField(choices=Status.choices, default=Status.OPEN)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.customer_phone}"