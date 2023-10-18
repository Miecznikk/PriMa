from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class ApartmentSearchForm(forms.Form):
    min_area = forms.FloatField(required=False, label='Minimum area (sq. meters)',
                                validators=[MinValueValidator(10.0, message="Value must be greater than 10 square "
                                                                            "meters"),
                                            MaxValueValidator(300.0,
                                                              message="Value cannot be greater than 300 square meters")])
    max_area = forms.FloatField(required=False, label='Maximum area (sq. meters)',
                                validators=[MinValueValidator(10.0, message="Value must be greater than 10 square "
                                                                            "meters"),
                                            MaxValueValidator(300.0,
                                                              message="Value cannot be greater than 300 square meters")])

    min_rooms = forms.IntegerField(required=False, label='Minimum number of rooms', validators=[
        MinValueValidator(1, message="Value must be greater or exual 1"),
        MaxValueValidator(10, message="Value cannot be greater than 10")
    ])
    max_rooms = forms.IntegerField(required=False, label='Maximum number of rooms', validators=[
        MinValueValidator(1, message="Value must be greater or exual 1"),
        MaxValueValidator(10, message="Value cannot be greater than 10")
    ])
    min_price = forms.IntegerField(required=False, label='Minimum price', validators=[
        MinValueValidator(1, message="Value must be greater than 0"),
        MaxValueValidator(100_000_000, message="Value cannot exceed 100 million")])
    max_price = forms.IntegerField(required=False, label='Maximum price', validators=[
        MinValueValidator(1, message="Value must be greater than 0"),
        MaxValueValidator(100_000_000, message="Value cannot exceed 100 million")])
    min_floor = forms.IntegerField(required=False, label='Minimum apartment floor', validators=[MaxValueValidator(20)])
    max_floor = forms.IntegerField(required=False, label='Maximum apartment floor', validators=[MaxValueValidator(20)])
    has_balcony = forms.BooleanField(required=False, label='Balcony')
    has_garden = forms.BooleanField(required=False, label='Garden')
    has_basement = forms.BooleanField(required=False, label='Basement')
    has_garage = forms.BooleanField(required=False, label='Garage')
    has_AC = forms.BooleanField(required=False, label='Air Conditioning')
    two_floor_apartment = forms.BooleanField(required=False, label='Two stories apartment')
