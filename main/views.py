from multiprocessing import context
from telnetlib import STATUS
from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import Http404
from django.http import HttpResponse
from account.models import Account
from main.forms import CreateProductForm, EditProductForm
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


def addProductView(request):
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


def editProductView(request,productId):
    context = {}
    product = get_object_or_404(Product, id=productId)
    if request.POST:
        form = EditProductForm(request.POST or None, instance=product)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Product updated!'
            product = obj
    form = EditProductForm(
        initial = {
            'title': product.title,
            'quantity':product.quantity,
            'collection':product.collection,
            'brand': product.brand,
            'type': product.type,
            'size': product.size,
            'price' : product.price,
            'flag': product.flag
        }
    )
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'main/editProduct.html', context)


def deleteProductView(request,productId):
    try:
        product = get_object_or_404(Product, id=productId)
        if not request.user.is_superuser:
            return redirect('main:index')
    except Product.DoesNotExist:
        return HttpResponse("Product not found",status = 404)
    except Exception:
        return HttpResponse("Internal Error",status= 500)
    product.delete()
    
    return redirect('main:products')
    



def productDetailView(request,productId):
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
