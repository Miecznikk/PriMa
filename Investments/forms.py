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
    has_balcony = forms.ChoiceField(required=False, label='Balcony',
                                    choices=[(None, 'Don\'t care'), (True, 'Yes'), (False, 'No')],
                                    widget=forms.RadioSelect)
    has_garden = forms.ChoiceField(required=False, label='Garden',
                                   choices=[(None, 'Don\'t care'), (True, 'Yes'), (False, 'No')],
                                   widget=forms.RadioSelect)
    has_basement = forms.ChoiceField(required=False, label='Basement',
                                     choices=[(None, 'Don\'t care'), (True, 'Yes'), (False, 'No')],
                                     widget=forms.RadioSelect)
    has_garage = forms.ChoiceField(required=False, label='Garage',
                                   choices=[(None, 'Don\'t care'), (True, 'Yes'), (False, 'No')],
                                   widget=forms.RadioSelect)
    has_AC = forms.ChoiceField(required=False, label='Air Conditioning',
                               choices=[(None, 'Don\'t care'), (True, 'Yes'), (False, 'No')],
                               widget=forms.RadioSelect)
    two_floor_apartment = forms.ChoiceField(required=False, label='Two stories apartment',
                                            choices=[(None, 'Don\'t care'), (True, 'Yes'), (False, 'No')],
                                            widget=forms.RadioSelect)

    def clean(self):
        super().clean()
        cd = self.cleaned_data
        numeric_fields = {"area": float, "price": int, "rooms": int, "floor": int}
        for field in numeric_fields:
            min_value, max_value = cd.get(f"min_{field}"), cd.get(f"max_{field}")
            if (min_value is not None and max_value is not None) and (numeric_fields[field](min_value) >
                                                                      numeric_fields[field](max_value)):
                raise forms.ValidationError(f"Minimum {field} cannot be greater than maximum {field}")
        return cd
