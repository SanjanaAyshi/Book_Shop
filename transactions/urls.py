from django.urls import path
from .views import addMoney, BuyBookView

urlpatterns = [
    path("deposit/", addMoney, name="addMoney"),
    path("buyBook/<int:id>", BuyBookView.as_view(), name="BuyBook"),
]
