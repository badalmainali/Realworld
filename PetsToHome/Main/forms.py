from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order,Customer,Pets


# Create your forms here.

class NewUserForm(UserCreationForm):

	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class CheckoutForm(forms.ModelForm):
	class Meta:
		model=Order
		fields=["ordered_by","shipping_address","mobile","email","payment_method"]

class RegistrationForm(forms.ModelForm):
	username=forms.CharField(widget=forms.TextInput())
	password=forms.CharField(widget=forms.PasswordInput())
	email=forms.CharField(widget=forms.TextInput())
	class Meta:
		model=Customer
		fields=["username","password","email","full_name","address"]

	#username validation
	def clean_username(self):
		uname=self.cleaned_data.get("username")
		if User.objects.filter(username=uname).exists():

			raise forms.ValidationError(" x User already exists. x")
		return uname

class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput())
	password=forms.CharField(widget=forms.PasswordInput())

class AdminLoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput())
	password=forms.CharField(widget=forms.PasswordInput())

class ProductForm(forms.ModelForm):
	class Meta:
		model=Pets
		fields=["title","slug","category","image","marked_price","selling_price","description","return_policy"]

