from django.shortcuts import render, get_object_or_404
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
