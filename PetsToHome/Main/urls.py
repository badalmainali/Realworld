from django.urls import path
from . import views
from .views import *

urlpatterns=[
    path('',views.main,name="main"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),

    path('pets',views.PetsView.as_view(),name="pets"),
    path("pets/<slug:slug>/",ProductDetailView.as_view(),name="productdetail"),

    path('addToCart<int:pro_id>/',AddToCartView.as_view(),name="addToCart"),
    path('my-cart/',MyCartView.as_view(),name="mycart"),
    path('manage-cart/<int:cp_id>/',ManageCart.as_view(),name="ManageCart"),
    path('empty-cart/',EmptyCart.as_view(),name="emptycart"),
    path('checkout/',Checkout.as_view(),name="checkout"),
    path('register/',RegistrationView.as_view(),name="register"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('login/',LoginView.as_view(),name="login"),





]