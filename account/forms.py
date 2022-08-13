from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import authenticate
from .models import Account


class RegistrationForm(UserCreationForm):
	first_name					= forms.CharField(widget=forms.TextInput(attrs={'name': 'first_name', 'class':'form-control form-control-lg', 'placeholder':'First Name', 'autofocus':'true'}), label='')
	last_name					= forms.CharField(widget=forms.TextInput(attrs={'name': 'last_name', 'class':'form-control form-control-lg', 'placeholder':'Last Name'}), label='')
	email						= forms.EmailField(widget=forms.EmailInput(attrs={'name': 'email', 'class':'form-control form-control-lg', 'placeholder':'Electronic mail'}), label='')
	username					= forms.CharField(max_length=16, widget=forms.TextInput(attrs={'name': 'username', 'class':'form-control form-control-lg', 'placeholder':'Username'}), label='')
	password1					= forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password1', 'class':'form-control form-control-lg', 'placeholder':'Password'}))
	password2					= forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password2', 'class':'form-control form-control-lg', 'placeholder':'Repeat password'}))
	street_name = forms.CharField(widget=
	forms.TextInput(attrs={'name':'street_name','class':'form-control form-control-lg', 'placeholder':'Street Name'}))
	street_number = forms.CharField(widget=
	forms.TextInput(attrs={'name':'street_number','class':'form-control form-control-lg', 'placeholder':'Street Number'}))
	city =  forms.CharField(widget=
	forms.TextInput(attrs={'name':'city','class':'form-control form-control-lg', 'placeholder':'City Name'}))
	postal_code =  forms.CharField(widget=
	forms.TextInput(attrs={'name':'postal_code','class':'form-control form-control-lg', 'placeholder':'Postal Code'}))
	country =  forms.CharField(widget=
	forms.TextInput(attrs={'name':'country','class':'form-control form-control-lg', 'placeholder':'Country Name'}))
	
	class Meta:
		model = Account
		fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2','street_name','street_number','city','postal_code','country')


class LoginForm(forms.ModelForm):
	email						= forms.EmailField(widget=forms.EmailInput(attrs={'name': 'email', 'class':'form-control form-control-lg', 'placeholder':'Email', 'autofocus':'true'}))
	password					= forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password1', 'class':'form-control form-control-lg', 'placeholder':'Password'}))

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError('Invalid login.')


class UserPasswordResetForm(PasswordResetForm):

	def __init__(self, *args, **kwargs):
		super(UserPasswordResetForm, self).__init__(*args, **kwargs)

	email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'name': 'email', 'class':'form-control form-control-lg', 'placeholder':'Electronic mail', 'autofocus':'true'}))


class EditAccountForm(forms.ModelForm):    
	class Meta:
		model = Account
		fields = ['first_name', 'last_name', 'email', 'username','street_name','street_number','city','postal_code','country']

	def save(self, commit=True):
		account = self.instance
		account.first_name = self.cleaned_data['first_name']
		account.last_name = self.cleaned_data['last_name']
		account.email = self.cleaned_data['email']
		account.username = self.cleaned_data['username']		
		account.street_name = self.cleaned_data['street_name']
		account.street_number = self.cleaned_data['street_number']
		account.city = self.cleaned_data['city']
		account.postal_code = self.cleaned_data['postal_code']
		account.country = self.cleaned_data['country']


        # if self.cleaned_data['image']:
        #     account.image = self.cleaned_data['image']

		if commit:
			account.save()
		return account