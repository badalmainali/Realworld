from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View

from .forms import NewUserForm, CheckoutForm, RegistrationForm
from django.contrib.auth import login
from django.contrib import messages #import messages
from django.views.generic import TemplateView,FormView,CreateView
from .models import *

# Create your views here.
def main(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def register(request):
    return render(request,'register.html')

class PetsView(TemplateView):
    template_name = 'pets.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        context['pets']=Pets.objects.all().order_by("-id")
        return context

class ProductDetailView(TemplateView):
    template_name = 'productdetail.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        url_slug=self.kwargs['slug']
        pets=Pets.objects.get(slug=url_slug)
        context['pets']=pets
        return context

class AddToCartView(TemplateView):
    template_name = 'addToCarts.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        #get pets id from url
        pets_id=self.kwargs['pro_id']

        #get pets
        pets_obj=Pets.objects.get(id=pets_id)

        #check carts existence by creating session
        cart_iid=self.request.session.get("cart_iid",None)  #sessions for everytime someone enter sites their previous cart is recorded

        if cart_iid:
            cart_obj=Cart.objects.get(id=cart_iid)
            this_product_in_cart=cart_obj.cartproduct_set.filter(pets=pets_obj)

            #if item already exist in cart we use this
            if this_product_in_cart.exists():
                cartproduct=this_product_in_cart.first()
                cartproduct.quantity += 1
                cartproduct.subtotal += pets_obj.selling_price
                cartproduct.save()
                cart_obj.total += pets_obj.selling_price
                cart_obj.save()
            else:
                cartproduct=CartProduct.objects.create(cart=cart_obj,pets=pets_obj,rate=pets_obj.selling_price,
                                                       quantity=1,subtotal=pets_obj.selling_price)
                cart_obj.total += pets_obj.selling_price
                cart_obj.save()
        else:
            cart_obj=Cart.objects.create(total=0)
            self.request.session['cart_iid']=cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, pets=pets_obj, rate=pets_obj.selling_price,
                                                     quantity=1, subtotal=pets_obj.selling_price)
            cart_obj.total += pets_obj.selling_price
            cart_obj.save()

        #check if pets already exists
        return context

class MyCartView(TemplateView):
    template_name = 'myCart.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_iid=self.request.session.get('cart_iid',None)
        if cart_iid:
            cart=Cart.objects.get(id=cart_iid)
        else:
            cart=None
        context['cart']=cart
        return context
class ManageCart(View):
    def get(self,request,*args,**kwargs):

        cp_id=self.kwargs["cp_id"]
        action=request.GET.get("action")
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart_obj=cp_obj.cart


        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()

        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()

            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
            if cp_obj == 0:
                cart_obj.total=0
                cart_obj.save()
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("mycart")

class EmptyCart(View):
    def get(self, request,*args,**kwargs):
        cart_iid=request.session.get("cart_iid",None)
        if cart_iid:
            cart=Cart.objects.get(id=cart_iid)
            cart.cartproduct_set.all().delete()
            cart.total=0
            cart.save()
        return redirect("mycart")

class Checkout(CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy("pets")

    # yo chai checkout garda afno cart dekhako same as mycart
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_iid=self.request.session.get("cart_iid",None)
        if cart_iid:
            cart_obj=Cart.objects.get(id=cart_iid)
        else:
            cart_obj=None

        context['cart']=cart_obj
        return context
    # making form valid for post request
    def form_valid(self,form):
        cart_iid=self.request.session.get("cart_iid")
        if cart_iid:
            cart_obj=Cart.objects.get(id=cart_iid)
            form.instance.cart=cart_obj
            form.instance.subtotal=cart_obj.total
            form.instance.discount=0
            form.instance.total=cart_obj.total
            form.instance.order_status="Order Received"
            del self.request.session['cart_iid']
        else:
            return redirect("pets")

        return super().form_valid(form)

# class AddToCartView(TemplateView):
#     template_name='new.html'
#
#     def get_context_data(self,**kwargs):
#
#         pets_idd=self.kwargs['p_id']
#
#         pets_ob=Pets.objects.get(id=pets_idd)
#
#         cart_session_id=self.request.session.get('cart_session_id',None)
#         this_item_in_cart=cart_session_id.cartproduct_set.filter(pets=pets_idd)
#
#         if this_item_in_cart.exists():
#             cartproduct=this_item_in_cart.first()
#
#         if cart_session_id:
#             cart_ob=Cart.objects.get(id=cart_session_id)
#         else:
#             cart_ob=Cart.objects.create(Total=0)

class RegistrationView(CreateView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy("/")