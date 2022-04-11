from django.db import models
import uuid


class Payment(models.Model):
    paymentUid = models.UUIDField(default=uuid.uuid4, help_text="Unique ID for this payment")
    STATUS_CHOICES = (
        ('P', "PAID"),
        ('C', "CANCELED"),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    price = models.IntegerField()

    def __str__(self):
        return str(self.paymentUid)
