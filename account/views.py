from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse

from .models import Account
from .forms import EditAccountForm, RegistrationForm, LoginForm


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


def editAccountView(request,accountId):
    context = {}
    account = get_object_or_404(Account, id=accountId)
    if request.POST:
        form = EditAccountForm(request.POST or None, instance=account)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Product updated!'
    form = EditAccountForm(
        initial = {
            'first_name' : account.first_name ,
			'last_name': account.last_name,
			'email': account.email,
			'username': account.username,
			'street_name':account.street_name,
			'street_number':account.street_number,
			'city':account.city,
			'postal_code':account.postal_code,
			'country':account.country
        }
    )
    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'account/editAccount.html', context)


def deleteAccountView(request,accountId):
    try:
        account = get_object_or_404(Account, id=accountId)
        if not request.user.is_superuser:
            return redirect('main:index')
    except Account.DoesNotExist:
        return HttpResponse("Account not found",status = 404)
    except Exception:
        return HttpResponse("Internal Error",status= 500)
    account.delete()
    
    return redirect('main:users')