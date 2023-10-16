from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from Users.models import InvestorUser


class Investment(models.Model):
    name = models.CharField(max_length=60, null=False)
    image = models.ImageField(upload_to='images/investments')
    resized_image = models.ImageField(upload_to='images/investments/resized', blank=True, null=True)
    street = models.CharField(max_length=60, null=False)
    city = models.CharField(max_length=60, null=False)
    investor = models.ForeignKey(InvestorUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_reversed_url(self):
        return reverse('investments:investment_detail', args=[str(self.id)])


class Apartment(models.Model):
    building_number = models.CharField(max_length=10, null=False)
    apartment_number = models.CharField(max_length=10, null=True)
    area = models.FloatField(validators=[
        MinValueValidator(10.0, message="Value must be greater than 10 square meters"),
        MaxValueValidator(300.0, message="Value cannot be greater than 300 square meters")
    ])
    rooms = models.IntegerField(validators=[
        MinValueValidator(1, message="Value must be greater or exual 1"),
        MaxValueValidator(10, message="Value cannot be greater than 10")
    ])
    investment = models.ForeignKey(Investment,on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.investment.name}: {self.get_full_address()}"

    def get_full_address(self):
        return (f"{self.investment.street} {self.building_number}"
                f"{"/" + self.apartment_number if self.apartment_number else ""}")

class ApartmentImage(models.Model):
    image = models.ImageField(upload_to='images/apartments')
    caption = models.CharField(max_length=60)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
# Create your models here.
