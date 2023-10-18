from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from Investments.models import Investment, Apartment
from .forms import ApartmentSearchForm


# Create your views here.
class AllInvestments(View):
    template_name = 'investments/all_investments.html'

    def get(self, request):
        investments = Investment.objects.all()
        return render(request, self.template_name, {'investments': investments})


class InvestmentDetail(View):
    template_name = 'investments/investment_detail.html'

    def get(self, request, id):
        investment = get_object_or_404(Investment, id=id)
        apartments = Apartment.objects.filter(investment=investment)
        return render(request, self.template_name,
                      {
                          "investment": investment,
                          "apartments": apartments
                      })


class ApartmentDetail(View):
    template_name = 'investments/apartment_detail.html'

    def get(self, request, id):
        apartment = get_object_or_404(Apartment, id=id)
        return render(request, self.template_name, {
            "apartment": apartment
        })


# TOUPDATE
class TmpSearchView(View):
    template_name = 'investments/search.html'

    def get(self, request):
        search_form = ApartmentSearchForm()
        return render(request, self.template_name, {
            "form": search_form
        })

    def post(self, request):
        search_form = ApartmentSearchForm(request.POST)
        if search_form.is_valid():
            apartments = Apartment.objects.all()
            cd = search_form.cleaned_data

            min_area = cd.get("min_area") if cd.get("min_area") else 10.0
            max_area = cd.get("max_area") if cd.get("max_area") else 300.0

            min_price = cd.get("min_price") if cd.get("min_price") else 1
            max_price = cd.get("max_price") if cd.get("max_price") else 100_000_000

            min_floor = cd.get("min_floor") if cd.get("min_floor") else 0
            max_floor = cd.get("max_floor") if cd.get("max_floor") else 20

            min_rooms = cd.get("min_rooms") if cd.get("min_rooms") else 1
            max_rooms = cd.get("max_rooms") if cd.get("max_rooms") else 10

            apartments = apartments.filter(area__gte=min_area,area__lte=max_area,
                                           price__gte=min_price,price__lte=max_price,
                                           floor__gte=min_floor,floor__lte=max_floor,
                                           rooms__gte=min_rooms,rooms__lte=max_rooms)

            has_balcony = cd.get("has_balcony") if cd.get("has_balcony") != '' else None
            has_garden = cd.get("has_garden") if cd.get("has_garden") != '' else None
            has_garage = cd.get("has_garage") if cd.get("has_garage") != '' else None
            has_AC = cd.get("has_AC") if cd.get("has_AC") != '' else None
            has_two_floors = cd.get("two_floor_apartment") if cd.get("two_floor_apartment") != '' else None

            if has_balcony is not None:
                apartments = apartments.filter(has_balcony=has_balcony)
            if has_garden is not None:
                apartments = apartments.filter(has_garden=has_garden)
            if has_garage is not None:
                apartments = apartments.filter(has_garage=has_garage)
            if has_AC is not None:
                apartments = apartments.filter(has_AC=has_AC)
            if has_two_floors is not None:
                apartments = apartments.filter(two_floor_apartment=has_two_floors)

            print(apartments)

            return redirect('/home')
        return render(request, self.template_name, {"form": search_form})
