import logging
import threading
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db.models import Min, Max, Q

from Messages.models import Message
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

    def get_number_parameter_range(self, parameter: str) -> str:
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

    def get_reversed_url(self):
        return reverse('investments:apartment_detail', args=[str(self.id)])


class ApartmentSearchResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    min_area = models.FloatField(validators=[
        MinValueValidator(10.0, message="Value must be greater or equal than 10"),
        MaxValueValidator(300.0, message="Value must be less or equal than 300")
    ])
    max_area = models.FloatField(validators=[
        MinValueValidator(10.0, message="Value must be greater or equal than 10"),
        MaxValueValidator(300.0, message="Value must be less or equal than 300")
    ])
    min_price = models.IntegerField(validators=[
        MinValueValidator(1, message="Value must be greater than 1"),
        MaxValueValidator(100_000_000, message="Value cannot exceed 100 milion")
    ])
    max_price = models.IntegerField(validators=[
        MinValueValidator(1, message="Value must be greater than 1"),
        MaxValueValidator(100_000_000, message="Value cannot exceed 100 milion")
    ])
    min_floor = models.PositiveIntegerField(validators=[
        MaxValueValidator(20)
    ])
    max_floor = models.PositiveIntegerField(validators=[
        MaxValueValidator(20)
    ])
    min_rooms = models.PositiveIntegerField(validators=[
        MinValueValidator(1, "Value must be a positive integer"),
        MaxValueValidator(10, "Value cannot exceed 10")
    ])
    max_rooms = models.PositiveIntegerField(validators=[
        MinValueValidator(1, "Value must be a positive integer"),
        MaxValueValidator(10, "Value cannot exceed 10")
    ])

    has_balcony = models.BooleanField(null=True)
    has_garden = models.BooleanField(null=True)
    has_basement = models.BooleanField(null=True)
    has_garage = models.BooleanField(null=True)
    has_AC = models.BooleanField(null=True)
    has_two_floors = models.BooleanField(null=True)

    @classmethod
    def filter_compatibility(cls, apartment: Apartment, request) -> None:
        search_results = cls.objects.all()
        search_results = (search_results.filter(
            min_area__lte=apartment.area,
            max_area__gte=apartment.area,
            min_price__lte=apartment.price,
            max_price__gte=apartment.price,
            min_floor__lte=apartment.floor,
            max_floor__gte=apartment.floor,
            min_rooms__lte=apartment.rooms,
            max_rooms__gte=apartment.rooms,
        ).filter(Q(has_balcony=apartment.has_balcony) | Q(has_balcony__isnull=True))
                          .filter(Q(has_garden=apartment.has_garden) | Q(has_garden__isnull=True))
                          .filter(Q(has_garage=apartment.has_garage) | Q(has_garage__isnull=True))
                          .filter(Q(has_basement=apartment.has_basement) | Q(has_basement__isnull=True))
                          .filter(Q(has_AC=apartment.has_AC) | Q(has_AC__isnull=True))
                          .filter(Q(has_two_floors=apartment.two_floor_apartment) | Q(has_two_floors__isnull=True)))

        if search_results.exists():
            from EmailService.service import EmailService
            for result in search_results:
                admin_user = User.objects.filter(is_superuser=True).first()
                Message.objects.create(sender=admin_user, receiver=result.user, title="idk",
                                       description="jest mieszkanko wariacie")
                threading.Thread(target=EmailService.send_apartment_available_email_to_user,
                                 args=(request, result.user, apartment.get_reversed_url())).start()


class ApartmentImage(models.Model):
    image = models.ImageField(upload_to='images/apartments')
    caption = models.CharField(max_length=60, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
# Create your models here.
