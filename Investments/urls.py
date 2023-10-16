from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    path('investments/', views.AllInvestments.as_view(), name='all_investments'),
    path('investments/<int:id>', views.InvestmentDetail.as_view(), name='investment_detail')
]
