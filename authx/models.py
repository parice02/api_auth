from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class CustomUser(AbstractUser):
    phone = PhoneNumberField("Numéro de téléphone", unique=True, max_length=30)
    # birthdate = models.DateField("Date de naissance")
    # gender = models.CharField(max_length=10)
    # city = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ["id"]
