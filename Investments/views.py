from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from Users.models import InvestorUser
from .decorators import investor_required
from Investments.models import Investment, Apartment, ApartmentImage
from .forms import ApartmentSearchForm, InvestmentDeletionForm, InvestmentAddForm, ApartmentAddForm, ApartmentImageForm


class AllInvestments(View):
    template_name = 'investments/investments_list.html'

    def get(self, request):
        if request.GET.get("investor"):
            investments = Investment.objects.filter(investor__id=request.GET.get("investor"))
            investor = InvestorUser.objects.get(id=request.GET.get("investor"))
        else:
            investments = Investment.objects.all()
            investor = None
        return render(request, self.template_name, {
            'investments': investments,
            "investor": investor
        })


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
        investor = InvestorUser.objects.get(id=apartment.investment.investor.id)
        return render(request, self.template_name, {
            "apartment": apartment,
            "investor": investor
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

            apartments = apartments.filter(area__gte=min_area, area__lte=max_area,
                                           price__gte=min_price, price__lte=max_price,
                                           floor__gte=min_floor, floor__lte=max_floor,
                                           rooms__gte=min_rooms, rooms__lte=max_rooms)

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


@method_decorator([login_required, investor_required], name='dispatch')
class MyInvestmentsView(View):
    template_name = 'investments/my_investments.html'

    def get(self, request):
        investments = Investment.objects.filter(investor=request.user.investoruser)
        return render(request, self.template_name, {
            "investments": investments
        })


@method_decorator([login_required, investor_required], name='dispatch')
class DeleteInvestmentView(View):
    template_name = 'investments/delete_investment.html'

    def get(self, request, id):
        form = InvestmentDeletionForm()
        investment = get_object_or_404(Investment, id=id, investor=request.user.investoruser)
        return render(request, self.template_name, {
            "investment": investment,
            "form": form
        })

    def post(self, request, id):
        form = InvestmentDeletionForm(request.POST)
        investment = get_object_or_404(Investment, id=id, investor=request.user.investoruser)

        if form.is_valid():
            if form.cleaned_data['confirmation_field'] == investment.name:
                investment.delete()
                return redirect('investments:my_investments')
            else:
                form.add_error('confirmation_field', "Incorrect confirmation input")

        return render(request, self.template_name, {
            "investment": investment,
            "form": form
        })


@method_decorator([login_required, investor_required], name='dispatch')
class AddInvestmentView(View):
    template_name = 'investments/add_investment.html'

    def get(self, request):
        form = InvestmentAddForm()
        return render(request, self.template_name, {
            "form": form
        })

    def post(self, request):
        form = InvestmentAddForm(request.POST, request.FILES)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.investor = get_object_or_404(InvestorUser, id=request.user.investoruser.id)
            investment.save()
            return redirect('investments:my_investments')
        return render(request, self.template_name, {"form": form})


@method_decorator([login_required, investor_required], name='dispatch')
class MyApartmentsView(View):
    template_name = 'investments/my_apartments.html'

    def get(self, request, investment):
        investment = get_object_or_404(Investment, id=investment, investor=request.user.investoruser)
        apartments = Apartment.objects.filter(investment=investment)
        return render(request, self.template_name, {
            "apartments": apartments,
            "investment": investment
        })


@method_decorator([login_required, investor_required], name='dispatch')
class MassDeleteApartmentsView(View):
    def post(self, request):
        apartments = Apartment.objects.filter(id__in=request.POST.getlist('apartment_ids'))
        apartments.delete()
        return redirect('investments:my_investments')


@method_decorator([login_required, investor_required], name='dispatch')
class AddApartmentView(View):
    template_name = 'investments/add_apartment.html'

    def get(self, request, investment):
        apartment_form = ApartmentAddForm()
        apartment_images_form = ApartmentImageForm()
        apartment_images_form.fields['images'].widget.attrs['class'] = 'form-control mb-4'

        return render(request, self.template_name, {
            "apartment_form": apartment_form,
            "apartment_images_form": apartment_images_form
        })

    def post(self, request, investment):
        apartment_form = ApartmentAddForm(request.POST)
        apartment_images_form = ApartmentImageForm(request.POST, request.FILES)
        apartment_images_form.fields['images'].widget.attrs['class'] = 'form-control mb-4'
        investment = get_object_or_404(Investment, id=investment, investor=request.user.investoruser)

        if apartment_form.is_valid():
            apartment = apartment_form.save(commit=False)
            apartment.investment = investment
            apartment.save()
            for image in request.FILES.getlist('images'):
                ApartmentImage.objects.create(image=image, apartment=apartment)
            return redirect('investments:my_apartments', investment=investment.id)

        return render(request, self.template_name, {
            "apartment_form": apartment_form,
            "apartment_images_form": apartment_images_form
        })


@method_decorator([login_required, investor_required], name='dispatch')
class EditApartmentView(View):
    template_name = 'investments/apartment_edit.html'

    def get(self, request, apartment):
        editing_apartment = get_object_or_404(Apartment, id=apartment, investment__investor=request.user.investoruser)
        initial_values = {
            "building_number": editing_apartment.building_number,
            "apartment_number": editing_apartment.apartment_number,
            "area": editing_apartment.area,
            "rooms": editing_apartment.rooms,
            "price": editing_apartment.price,
            "floor": editing_apartment.floor,
            "has_balcony": editing_apartment.has_balcony,
            "has_garden": editing_apartment.has_garden,
            "has_garage": editing_apartment.has_garage,
            "has_basement": editing_apartment.has_basement,
            "has_AC": editing_apartment.has_AC,
            "two_floor_apartment": editing_apartment.two_floor_apartment
        }
        apartment_form = ApartmentAddForm(initial=initial_values)
        return render(request, self.template_name, {
            "apartment_form": apartment_form,
            "apartment": editing_apartment
        })

    def post(self, request, apartment):
        apartment_obj = get_object_or_404(Apartment, id=apartment, investment__investor=request.user.investoruser)
        apartment_form = ApartmentAddForm(request.POST, instance=apartment_obj)
        if apartment_form.is_valid():
            apartment_form.save()
            return redirect('investments:my_apartments', apartment_obj.investment.id)
        return render(request, self.template_name, {
            "apartment_form": apartment_form,
            "apartment": apartment_obj
        })


@method_decorator([login_required, investor_required], name='dispatch')
class EditApartmentImages(View):
    template_name = 'investments/edit_apartment_images.html'

    def get(self, request, apartment):
        apartment = get_object_or_404(Apartment, id=apartment, investment__investor=request.user.investoruser)
        apartment_images = ApartmentImage.objects.filter(apartment=apartment)
        apartment_images_form = ApartmentImageForm()
        apartment_images_form.fields['images'].widget.attrs['class'] = 'form-control mb-4'
        return render(request, self.template_name, {
            "apartment": apartment,
            "apartment_images": apartment_images,
            "apartment_images_form": apartment_images_form
        })

    def post(self, request, apartment):
        apartment = get_object_or_404(Apartment, id=apartment, investment__investor=request.user.investoruser)
        apartment_images_form = ApartmentImageForm(request.POST, request.FILES)
        apartment_images_form.fields['images'].widget.attrs['class'] = 'form-control mb-4'
        for image in request.FILES.getlist('images'):
            ApartmentImage.objects.create(image=image, apartment=apartment)
        return redirect('investments:edit_apartment_images', apartment.id)


@method_decorator([login_required, investor_required], name='dispatch')
class DeleteApartmentImage(View):

    def post(self, request, apartment, image):
        deletion_image = get_object_or_404(ApartmentImage, id=image,
                                           apartment__investment__investor=request.user.investoruser)
        deletion_image.delete()
        return redirect('investments:edit_apartment_images', apartment=apartment)


@method_decorator([login_required, investor_required], name='dispatch')
class EditInvestmentView(View):
    template_name = 'investments/edit_investment.html'

    def get(self, request, id):
        investment = get_object_or_404(Investment, id=id, investor=request.user.investoruser)
        initial_data = {
            "name": investment.name,
            "image": investment.image,
            "street": investment.street,
            "city": investment.city
        }
        form = InvestmentAddForm(initial=initial_data, instance=investment)
        return render(request, self.template_name, {
            "investment": investment,
            "form": form
        })

    def post(self, request, id):
        investment = get_object_or_404(Investment, id=id, investor=request.user.investoruser)
        form = InvestmentAddForm(request.POST, request.FILES, instance=investment)
        if form.is_valid():
            investment = form.save()
            return redirect('investments:my_investments')
        return render(request, self.template_name, {
            "investment": investment,
            "form": form
        })
