from django.contrib import admin
from .models import Investment, Apartment, ApartmentImage, ApartmentSearchResult


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'street', 'city', 'investor']


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['building_number', 'apartment_number', 'area', 'rooms']


@admin.register(ApartmentImage)
class ApartmentImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'caption', 'apartment']


# Register your models here.

@admin.register(ApartmentSearchResult)
class ApartmentSearchResultAdmin(admin.ModelAdmin):
    list_display = ['user', ]
