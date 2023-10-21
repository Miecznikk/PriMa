from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    path('investments/', views.AllInvestments.as_view(), name='all_investments'),
    path('investments/<int:id>', views.InvestmentDetail.as_view(), name='investment_detail'),
    path('investments/apartment/<int:id>', views.ApartmentDetail.as_view(), name='apartment_detail'),
    path('investments/search', views.TmpSearchView.as_view(), name='search'),
    path('investments/my_investments', views.MyInvestmentsView.as_view(), name='my_investments'),
    path('investments/delete_investment/<int:id>', views.DeleteInvestmentView.as_view(), name='delete_investment'),
    path('investments/add_investment', views.AddInvestmentView.as_view(), name='add_investment'),
    path('investments/my_apartments/<int:investment>', views.MyApartmentsView.as_view(), name='my_apartments'),
    path('investments/my_apartments/mass_delete', views.MassDeleteApartmentsView.as_view(), name='mass_delete_apartments'),
]
