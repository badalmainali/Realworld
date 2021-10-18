from django.shortcuts import render,redirect
from django.urls import reverse_lazy, reverse
from django.views import View

from .forms import NewUserForm, CheckoutForm, RegistrationForm, LoginForm, AdminLoginForm, ProductForm
from django.contrib.auth import login
from django.contrib import messages #import messages
from django.views.generic import TemplateView,FormView,CreateView,DetailView,ListView
from django.contrib.auth import authenticate,login,logout
from .models import *

# Create your views here.
class PetsMixin(object):
    def dispatch(self,request,*args,**kwargs):

        cart_iid=self.request.session.get("cart_iid",None)
        if cart_iid:
            cart_obj=Cart.objects.get(id=cart_iid)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer=request.user.customer
                cart_obj.save()
        return super().dispatch(request,*args,**kwargs)


def main(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def register(request):
    return render(request,'register.html')

class PetsView(PetsMixin,TemplateView):
    template_name = 'pets.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        context['pets']=Pets.objects.all().order_by("-id")
        return context



class ProductDetailView(PetsMixin,TemplateView):
    template_name = 'productdetail.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        url_slug=self.kwargs['slug']
        pets=Pets.objects.get(slug=url_slug)
        context['pets']=pets
        return context

class AddToCartView(PetsMixin,TemplateView):
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

class MyCartView(PetsMixin,TemplateView):
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
class ManageCart(PetsMixin,View):
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

class EmptyCart(PetsMixin,View):
    def get(self, request,*args,**kwargs):
        cart_iid=request.session.get("cart_iid",None)
        if cart_iid:
            cart=Cart.objects.get(id=cart_iid)
            cart.cartproduct_set.all().delete()
            cart.total=0
            cart.save()
        return redirect("mycart")

class Checkout(PetsMixin,CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy("pets")

    def dispatch(self, request, *args, **kwargs):
        user=request.user
        if user.is_authenticated and user.customer:
            pass
        else:
            return redirect('/login/?next=/checkout/')
        return super().dispatch(request,*args,**kwargs)

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
            pm=form.cleaned_data.get("payment_method")
            order=form.save()
            if pm == "Esewa":
                return redirect(reverse("esewarequest")+"?o_id=" + str(order.id))
            else:
                pass
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
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        email=form.cleaned_data.get("email")
        user=User.objects.create_user(username,email,password)
        form.instance.user=user
        login(self.request,user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url=self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("main")

class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        uname=form.cleaned_data.get("username")
        pword=form.cleaned_data.get("password")
        usr=authenticate(username=uname,password=pword)
        if usr is not None and usr.customer:
            login(self.request,usr)
        else:
            return render(self.request,self.template_name,{"form":LoginForm, "error":"Credentials didn't match"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url=self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class CustomerProfileView(TemplateView):
    template_name = 'customerprofile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("login/?next=/profile/")
        return super().dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        customer=self.request.user.customer
        context['customer']=customer
        orders=Order.objects.filter(cart__customer=customer)
        context['orders']=orders
        return context

class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model=Order
    context_object_name = "ord_obj"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("login/?next=/profile/")
        return super().dispatch(request,*args,**kwargs)

#admin pages
class AdminLoginView(FormView):
    template_name = "adminn/adminlogin.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": AdminLoginForm, "error": "Credentials didn't match"})
        return super().form_valid(form)

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("admin-login")
        return super().dispatch(request,*args,**kwargs)

class AdminHomeView(AdminRequiredMixin,TemplateView):
    template_name = "adminn/adminhome.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["pendingorders"]=Order.objects.filter(order_status="Order Received").order_by("-id")
        return context

class AdminOrderDetailView(AdminRequiredMixin,DetailView):
    template_name = "adminn/adminorderdetail.html"
    model=Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["allstatus"]=ORDER_STATUS
        return context

class AdminOrderList(AdminRequiredMixin, ListView):
    template_name = "adminn/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorder"

class AdminOrderStatus(AdminRequiredMixin, View):
    def post(self,request,*args,**kwargs):
        order_id=self.kwargs["pk"]

        order_obj=Order.objects.get(id=order_id)
        new_status=request.POST.get("status")
        order_obj.order_status=new_status
        order_obj.save()
        return redirect(reverse_lazy("admin-order",kwargs={"pk":order_id}))

#payments
class EsewaRequest(View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get("o_id")
        order=Order.objects.get(id=o_id)
        context={
            "order":order

        }

        return render(request,"esewarequest.html",context)

class EsewaVerify(View):
    def get(self,request,*args,**kwargs):
        import xml.etree.ElementTree as ET
        oid=request.GET.get("oid")
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")

        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'EPAYTEST',
            'rid': refId,
            'pid': oid,
        }
        resp = request.post(url, d)
        root = ET.fromstring(resp.content)
        status=root[0].text.strip()
        order_id = oid.split("_")[1]
        order_obj=Order.objects.get(id=order_id)
        if status=="Success":
            order_obj.payment_completed=True
            order_obj.save()

            return redirect("main")
        else:

            return redirect("/esewa-request/?o_id="+order_id)

class AdminProductList(AdminRequiredMixin, ListView):
    template_name = "adminn/adminproductlist.html"
    queryset =Pets.objects.all().order_by("-id")
    context_object_name ="allproducts"

class AdminProductAdd(AdminRequiredMixin,CreateView):
    template_name ="adminn/adminproductadd.html"
    form_class = ProductForm
    success_url = reverse_lazy("adminproductlist")