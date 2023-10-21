import logging

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db.models import Min, Max
from Users.models import InvestorUser
from django.core.exceptions import FieldDoesNotExist


class Investment(models.Model):
    logger = logging.getLogger(__name__)

    name = models.CharField(max_length=60, null=False)
    image = models.ImageField(upload_to='images/investments')
    street = models.CharField(max_length=60, null=False)
    city = models.CharField(max_length=60, null=False)
    investor = models.ForeignKey(InvestorUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_reversed_url(self):
        return reverse('investments:investment_detail', args=[str(self.id)])

    def get_area_range(self):
        return self.get_number_parameter_range("area")

    def get_price_range(self):
        return self.get_number_parameter_range("price")

    def get_number_parameter_range(self, parameter):
        try:
            field = Apartment._meta.get_field(parameter)
            if isinstance(field, (models.IntegerField, models.PositiveIntegerField, models.FloatField)):
                apartments = Apartment.objects.filter(investment=self).aggregate(min_value=Min(parameter),
                                                                                 max_value=Max(parameter))
                if apartments['min_value'] is None:
                    return ""
                return f"{apartments['min_value']} - {apartments['max_value']}"
            else:
                return ""
        except FieldDoesNotExist as e:
            self.logger.error(str(e))

    def get_apartments_count(self):
        return len(Apartment.objects.filter(investment=self))


class Apartment(models.Model):
    building_number = models.CharField(max_length=10, null=False)
    apartment_number = models.CharField(max_length=10, null=True)
    area = models.FloatField(validators=[
        MinValueValidator(10.0, message="Value must be greater than 10 square meters"),
        MaxValueValidator(300.0, message="Value cannot be greater than 300 square meters")
    ], null=False)
    rooms = models.IntegerField(validators=[
        MinValueValidator(1, message="Value must be greater or exual 1"),
        MaxValueValidator(10, message="Value cannot be greater than 10")
    ], null=False)
    price = models.PositiveIntegerField(validators=[
        MinValueValidator(1, message="Value must be greater than 0"),
        MaxValueValidator(100_000_000, message="Value cannot exceed 100 million")],
        null=False)
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, null=False)
    floor = models.PositiveIntegerField(validators=[MaxValueValidator(20)])
    has_balcony = models.BooleanField(null=False)
    has_garden = models.BooleanField(null=False)
    has_basement = models.BooleanField(null=False)
    has_garage = models.BooleanField(null=False)
    has_AC = models.BooleanField(null=False)
    two_floor_apartment = models.BooleanField(null=False)

    def __str__(self):
        return f"{self.investment.name}: {self.get_full_address()}"

    def get_full_address(self):
        return (f"{self.investment.street} {self.building_number}"
                f"{"/" + self.apartment_number if self.apartment_number else ""}")

    def get_price_per_square_meter(self):
        return f"{round(self.price / self.area, 2)}"

    def get_rooms_str(self):
        return f"{self.rooms} rooms" if self.rooms > 1 else f"{self.rooms} room"

    def get_additional_info_string(self):
        addons = [f"floor {self.floor}"]
        if self.has_balcony:
            addons.append("Balcony")
        if self.has_garden:
            addons.append("Garden")
        if self.has_garage:
            addons.append("Garage")
        if self.has_AC:
            addons.append("Air conditioning")
        if self.two_floor_apartment:
            addons.append("Two-floor apartment")
        return ", ".join(addons)


class ApartmentImage(models.Model):
    image = models.ImageField(upload_to='images/apartments')
    caption = models.CharField(max_length=60)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
# Create your models here.
