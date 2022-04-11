import uuid
from django.db import models


class Reservation(models.Model):
    reservationUid = models.UUIDField(default=uuid.uuid4, help_text="Unique ID for this app")
    username = models.CharField(max_length=80)
    payment_uid = models.UUIDField(default=uuid.uuid4, help_text="Unique ID for this payment")
    hotel_id = models.ForeignKey('Hotel', null=True, on_delete=models.SET_NULL)

    STATUS_CHOICES = (
        ('P', "PAID"),
        ('C', "CANCELED"),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.reservationUid)


class Hotel(models.Model):
    hotelUid = models.UUIDField(default=uuid.uuid4, help_text="Unique ID for this app")
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=255)
    stars = models.IntegerField(blank=True, null=True)
    price = models.IntegerField()

    def __str__(self):
        return str(self.hotelUid)

