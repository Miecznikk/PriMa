from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    path('investments/', views.AllInvestments.as_view(), name='investment_list'),
    path('investments/<int:id>', views.InvestmentDetail.as_view(), name='investment_detail'),
    path('investments/apartment/<int:id>', views.ApartmentDetail.as_view(), name='apartment_detail'),
    path('investments/search', views.SearchView.as_view(), name='search'),
    path('investments/my_investments', views.MyInvestmentsView.as_view(), name='my_investments'),
    path('investments/delete_investment/<int:id>', views.DeleteInvestmentView.as_view(), name='delete_investment'),
    path('investments/add_investment', views.AddInvestmentView.as_view(), name='add_investment'),
    path('investments/my_apartments/<int:investment>', views.MyApartmentsView.as_view(), name='my_apartments'),
    path('investments/my_apartments/mass_delete', views.MassDeleteApartmentsView.as_view(),
         name='mass_delete_apartments'),
    path('investments/my_apartments/<int:investment>/add/', views.AddApartmentView.as_view(), name='add_apartment'),
    path('investments/my_apartments/<int:apartment>/edit', views.EditApartmentView.as_view(), name='edit_apartment'),
    path('investments/my_apartments/<int:apartment>/edit/images', views.EditApartmentImages.as_view(),
         name='edit_apartment_images'),
    path('investments/my_apartments/<int:apartment>/edit/images/delete/<int:image>',
         views.DeleteApartmentImage.as_view(), name='delete_apartment_image'),
    path('investments/my_investments/<int:id>/edit', views.EditInvestmentView.as_view(), name='edit_investment'),
    path('investments/saved_search', views.MySearchResultsView.as_view(), name='saved_search'),
    path('investments/saved_search/<int:id>', views.SearchResultDetailView.as_view(), name='saved_search_detail'),
    path('investments/delete_saved_search/<int:id>', views.DeleteSearchResult.as_view(), name='delete_saved_search')
]
