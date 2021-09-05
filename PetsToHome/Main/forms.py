from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order,Customer


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
		fields=["ordered_by","shipping_address","mobile","email"]

class RegistrationForm(forms.ModelForm):
	username=forms.CharField(widget=forms.TextInput())
	password=forms.CharField(widget=forms.PasswordInput())
	email=forms.CharField(widget=forms.TextInput())
	class Meta:
		model=Customer
		fields=["username","password","email","full_name","address"]