from multiprocessing import context
from re import A
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse

from main.models import Cart, Receipt
from .models import Account, Address
from .forms import AddressForm, EditAccountForm, EditAddressForm, RegistrationForm, LoginForm
from main.helpers import isAjax
import json


def registerView(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		address = AddressForm(request.POST)
		if form.is_valid():
			user = form.save()
			address = address.save(commit=False)
			address.user = user
			address.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password2')
			account = authenticate(email=email, password=raw_password)
			try:
				cart = Cart.objects.get(user=account)
			except Cart.DoesNotExist:
				cart = Cart.objects.create(user=account)
			account.cart = cart 
			login(request, account)
			return redirect('main:index')
		else:
			context = {
				'form': form,
				'address': address,
				'navbar': 'register'
			}
	else:
		form = RegistrationForm()
		address = AddressForm()
		context = {
			'navbar': 'register',
			'address': address,
			'form': form
		}
	return render(request, 'account/register.html', context)


def profileView(request):
	context = {}
	user = get_object_or_404(Account, id=request.user.id)
	if not user.is_authenticated:
		return redirect('main:index')
	receipts = Receipt.objects.filter(account=user).all()
	context['receipts'] = receipts
	context['user'] = user
	return render(request,"account/profile.html",context)






def loginView(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect('main:index')
	if request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				try:
					cart = Cart.objects.get(user=user)
				except Cart.DoesNotExist:
					cart = Cart.objects.create(user=user)
				user.cart = cart 
				login(request, user)
				nxt = request.GET.get('next', False)
				if nxt:
					return HttpResponseRedirect(nxt)
				else:
					return redirect('main:index')
	else:
		form = LoginForm()
	context['login_form'] = form
	context['navbar'] = 'login'
	return render(request, 'account/login.html', context)


def logoutView(request):
	logout(request)
	return redirect('main:index')


def editAccountView(request,accountId):
	context = {}
	account = get_object_or_404(Account, id=accountId)
	try:
		address = get_object_or_404(Address, user=account)
	except:
		address = Address.objects.create(user=account)
	if request.POST:
		form = EditAccountForm(request.POST or None, instance=account)
		address = EditAddressForm(request.POST)
		if form.is_valid():
			user = form.save()
			address = address.save(commit=False)
			address.user = user
			address.save()
	if not request.user.is_superuser:
		form = EditAccountForm(
			initial = {
				'first_name' : account.first_name,
				'last_name': account.last_name,
				'email': account.email,
				'username': account.username,
			}
		)
	else:
		form = EditAccountForm(
			initial = {
				'first_name' : account.first_name ,
				'last_name': account.last_name,
				'email': account.email,
				'username': account.username,
				'is_admin': account.is_admin,
				'is_active': account.is_active,
				'is_superuser': account.is_superuser,
				'is_staff': account.is_staff,
			}
		)
	address = EditAddressForm(
		initial = {
			'street_name': address.street_name,
			'street_number': address.street_number,
			'city': address.city,
			'postal_code': address.postal_code,
			'country': address.country
		}
	)
	admin_check = ['is_admin', 'is_active', 'is_superuser', 'is_staff']
	context = {
		'form': form,
		'address': address,
		'account': account,
		'admin_check': admin_check,
	}

	return render(request, 'account/editAccount.html', context)


# def deleteAccountView(request,accountId):
# 	try:
# 		account = get_object_or_404(Account, id=accountId)
# 		if not request.user.is_superuser:
# 			return redirect('main:index')
# 	except Account.DoesNotExist:
# 		return HttpResponse("Account not found",status = 404)
# 	except Exception:
# 		return HttpResponse("Internal Error",status= 500)
# 	account.delete()
	
# 	return redirect('main:users')


def deleteAccountView (request):
	if request.method == "POST" and isAjax(request):
		userId = request.POST.get('id', None)
		try:
			user = get_object_or_404(Account, id=userId)
			user.delete()
			return HttpResponse(json.dumps({ "good": True }), content_type="application/json")
		except Account.DoesNotExist:
			return HttpResponse(json.dumps({ "good": False }), content_type="application/json")