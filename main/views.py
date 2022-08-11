from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import Http404
from account.models import Account
from main.forms import CreateProductForm
from .models import Product

# Create your views here.

def indexView(request):
    context = {}
    products = Product.objects.all()
    accounts = Account.objects.all()
    context = {
        'products' : products,
        'accounts' : accounts,

    }

    return render(request,"main/index.html",context)


def addProduct(request):
    form = CreateProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save()
        form = CreateProductForm()
        return redirect('main:index')
    context = {
        'form': form,
        
    }
    return render(request, 'main/addProduct.html', context)

def usersView(request):
    context = {}
    accounts = Account.objects.all()
    context = {
        'accounts' : accounts,

    }
    return render(request,"main/users.html",context)


def productsView(request):
    context = {}
    products = Product.objects.all()
    context = {
        'products' : products,

    }
    return render(request,"main/products.html",context)



def productDetail(request,productId):
    context = {}
    try:
        product = get_object_or_404(Product, id=productId)
    except Http404: 
        return redirect('main:index')

    context = {
        'product' : product,

    }
    
    return render(request, 'main/productDetail.html', context)


def menswearView(request):
    context = {}
    products = Product.objects.filter(type='MEN').all()
    context = {
        'products' : products,
        'nav':'Men',

    }

    return render(request,"main/men.html",context)

    
def womenswearView(request):
    context = {}
    products = Product.objects.filter(type='WOMEN').all()
    context = {
        'products' : products,
        'nav':'Women',

    }

    return render(request,"main/women.html",context)

def kidswearView(request):
    context = {}
    products = Product.objects.filter(type='KIDS').all()
    context = {
        'products' : products,
        'nav':'Kids',

    }

    return render(request,"main/kids.html",context)
