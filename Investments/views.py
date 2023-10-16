from django.shortcuts import render, get_object_or_404
from django.views import View

from Investments.models import Investment, Apartment


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
