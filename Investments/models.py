from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from Users.models import InvestorUser


class Investment(models.Model):
    name = models.CharField(max_length=60, null=False)
    image = models.ImageField(upload_to='images/investments')
    street = models.CharField(max_length=60, null=False)
    city = models.CharField(max_length=60, null=False)
    investor = models.ForeignKey(InvestorUser, on_delete=models.SET_NULL, null=True)


class Apartment(models.Model):
    building_numer = models.CharField(max_length=10, null=False)
    apartment_numer = models.CharField(max_length=10, null=True)
    area = models.FloatField(validators=[
        MinValueValidator(10.0, message="Value must be greater than 10 square meters"),
        MaxValueValidator(300.0, message="Value cannot be greater than 300 square meters")
    ])
    rooms = models.IntegerField(validators=[
        MinValueValidator(1, message="Value must be greater or exual 1"),
        MaxValueValidator(10, message="Value cannot be greater than 10")
    ])


class ApartmentImage(models.Model):
    image = models.ImageField(upload_to='images/apartments')
    caption = models.CharField(max_length=60)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
# Create your models here.
