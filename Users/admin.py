from django.contrib import admin
from .models import CustomerUser, InvestorUser


@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(InvestorUser)
class InvestorUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number']
# Register your models here.
