from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages #import messages
from django.views.generic import TemplateView
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


