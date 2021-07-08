from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Customer,Cart,Category,Order,Pets,CartProduct])