from django.contrib import admin
from .models import CustomerUser

@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display=['user']

# Register your models here.
