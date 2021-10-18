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
    path('profile/',CustomerProfileView.as_view(),name='customerprofile'),
    path('profile/order-<int:pk>/',CustomerOrderDetailView.as_view(),name="cutomerdetail"),

    path('admin-login/',AdminLoginView.as_view(),name="adminlogin"),
    path('admin-home/',AdminHomeView.as_view(),name="adminhome"),
    path('admin-order/<int:pk>/',AdminOrderDetailView.as_view(),name="admin-order"),
    path('admin-all-orders/',AdminOrderList.as_view(),name="adminorderlist"),
    path('admin-order-<int:pk>-change/',AdminOrderStatus.as_view(),name="adminorderstatus"),

    path("esewa-request/",EsewaRequest.as_view(),name="esewarequest"),
    path("esewa-verify/",EsewaVerify.as_view(),name="esewaverify"),
    path("admin-product/list/",AdminProductList.as_view(),name="adminproductlist"),
path("admin-product/add/",AdminProductAdd.as_view(),name="adminproductadd")









]