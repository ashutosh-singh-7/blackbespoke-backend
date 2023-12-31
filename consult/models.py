from collections.abc import Iterable
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import Customer
from datetime import datetime, date, time
from django.utils import timezone
import uuid
# Create your models here.

def generate_short_uuid():
    return str(uuid.uuid4())[:6]

@receiver(post_save, sender=Customer)
def create_appointment(sender, instance, created, **kwargs):
    """
    Signal receiver function to create an Appointment instance when a Customer instance is saved.
    """
    if created:
        Appointment.objects.create(customer=instance)

class Appointment(models.Model):
    class appnt_types(models.TextChoices):
        CHOICE_ONE = 'CALLBACK', 'CALLBACK'
        CHOICE_TWO = 'MEASUREMENT', 'MEASUREMENT'
        CHOICE_THREE = 'CONSULTATION', 'CONSULTATION'
        CHOICE_FOUR = 'DRAFT', 'DRAFT'
    appnt_type = models.CharField(
        max_length=20,
        choices=appnt_types.choices,
        default=appnt_types.CHOICE_FOUR
    )
    is_active = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    suit = models.OneToOneField(to='suit.SuitBuild', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.OneToOneField(to='user.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='my_consult')
    identifier = models.CharField(max_length=100, null=False, blank=False, unique=True, editable=False, default=generate_short_uuid,
                            error_messages={
                                     "unique": "Appointment with this identifier already exists."
                                    })
    
    
    @property
    def customer_address(self):
        # Check if the appointment has a related customer
        if self.customer:
            # Access the 'address' field of the related Customer model
            return self.customer.address.id
        else:
            return None  # or any default value you prefer

    @property
    def customer_city(self):
        # Check if the appointment has a related customer
        if self.customer:
            # Access the 'address' field of the related Customer model
            return self.customer.address.city.id
        else:
            return None  # or any default value you prefer


    def __str__(self) -> str:
        return f"{self.appnt_type} • {self.customer} • {self.date}"
    
    def save(self, *args, **kwargs):
        # If the 'suit' field is set, update 'appnt_type' to 'MEASUREMENT'
        if self.suit and self.appnt_type != self.appnt_types.CHOICE_TWO:
            self.appnt_type = self.appnt_types.CHOICE_TWO
        if self.appnt_type == self.appnt_types.CHOICE_THREE:
            self.suit = None
        return super(Appointment, self).save(*args, **kwargs)
    
    