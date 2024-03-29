from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from Investments.decorators import investor_required
import googlemaps
from django.conf import settings


class Home(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name, {})


@method_decorator([login_required, investor_required], name='dispatch')
class InvestorPanelView(View):
    template_name = 'navigation/investor_panel.html'

    def get(self, request):
        investor = request.user.investoruser
        return render(request, self.template_name, {
            "investor": investor
        })


@method_decorator([login_required], name='dispatch')
class CustomerPanelView(View):
    template_name = 'navigation/customer_panel.html'

    def get(self, request):
        return render(request, self.template_name, {})

