from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class CustomerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_numer = models.CharField(max_length=9, validators=[
        RegexValidator(regex=r'^\d{9}$', code="Invalid phone number")
    ], null=True)


class InvestorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_number = models.CharField(max_length=9, validators=[
        RegexValidator(regex=r'^\d{9}$', code="Invalid phone number")
    ], null=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
