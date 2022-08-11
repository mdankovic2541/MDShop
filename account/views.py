from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm


# @isAlreadyAuthenticated
def registerView(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password2')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('main:index')
		else:
			context = {
				'registration_form': form,
				'navbar': 'register'
			}
	else:
		form = RegistrationForm()
		context = {
			'navbar': 'register',
			'registration_form': form
		}
	return render(request, 'account/register.html', context)


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
