from django.contrib import admin
from .models import UserBookAccount, UserAddress, PurchaseModel
# Register your models here.

admin.site.register(UserBookAccount)
admin.site.register(UserAddress)
admin.site.register(PurchaseModel)
