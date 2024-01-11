from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserBookAccountUpdateView, ReturnBookView, ProfileData

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileData, name='profile'),
    path('return_book/<int:id>/', ReturnBookView.as_view(), name='return_book'),
]
