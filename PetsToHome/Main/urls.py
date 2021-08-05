from django.urls import path
from . import views
from .views import *

urlpatterns=[
    path('',views.main,name="main"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('register',views.register,name="register"),
    path('pets',views.PetsView.as_view(),name="pets"),
    path("pets/<slug:slug>/",ProductDetailView.as_view(),name="productdetail"),


]