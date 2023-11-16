from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


def is_investor(self):
    if hasattr(self, 'investoruser'):
        return True
    return False


def __str__(self):
    if is_investor(self):
        return f"{self.first_name} {self.last_name} ({self.investoruser.company_name})"
    elif self.is_superuser:
        return f"{self.first_name} {self.last_name} (Administrator)"
    return f"{self.first_name} {self.last_name}"


User.add_to_class("__str__", __str__)
User.add_to_class("is_investor", is_investor)


class CustomerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_numer = models.CharField(max_length=9, validators=[
        RegexValidator(regex=r'^\d{9}$', code="Invalid phone number")
    ], null=True)


class InvestorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    company_name = models.CharField(max_length=50,null=False)
    company_logo = models.ImageField(upload_to='images/users/investors_logos', null=True, blank=True)
    phone_number = models.CharField(max_length=9, validators=[
        RegexValidator(regex=r'^\d{9}$', code="Invalid phone number")
    ], null=False)
    webpage = models.CharField(max_length=50, validators=[
        RegexValidator(regex=r'^https:\/\/[www]?.+\..+$', code="Invalid web address")
    ])

    def __str__(self):
        return f"{self.company_name}"

    def get_investments_count(self):
        from Investments.models import Investment
        return len(Investment.objects.filter(investor=self))

    def get_apartments_count(self):
        from Investments.models import Apartment
        return len(Apartment.objects.filter(investment__investor=self))
