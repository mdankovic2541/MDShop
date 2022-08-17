from multiprocessing import context
from telnetlib import STATUS

from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import Http404
from django.http import HttpResponse, JsonResponse
from account.models import Account
from main.forms import CreateProductForm, EditProductForm
from .models import Product, Comment
from main.helpers import isAjax

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
	if not request.user.is_superuser:
		return redirect('main:index')
	form = CreateProductForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save()
		productId = obj.id
		form = CreateProductForm()
		return redirect('main:productDetail', productId=productId)
	context = {
		'form': form,
	}
	return render(request, 'main/addProduct.html', context)

def usersView(request):
	if not request.user.is_superuser:
		return redirect('main:index')
	context = {}
	accounts = Account.objects.all()
	context = {
		'accounts' : accounts,

	}
	return render(request,"main/users.html",context)


def createCommentView(request, productId):
	product = get_object_or_404(Product, id=productId)
	if product and isAjax(request):
		description = request.POST.get('description', None)
		if description:
			comment = product.comments.create(description=description,product=product.id, account=request.user)
			comment.save()
			response = {
				'description': comment.description,
				'account': comment.account.username,
				
			}
			return JsonResponse(response)
	else:
		return redirect('main:index')

def deleteCommentView(request,commentId):
	try:
		comment = get_object_or_404(Comment, id=commentId)
	except Comment.DoesNotExist:
		return HttpResponse("Comment not found",status = 404)
	except Exception:
		print(Exception)
		return HttpResponse("Internal Error",status= 500)
	comment.delete()
	
	return redirect('main:index')
	

def productsView(request):
	if not request.user.is_superuser:
		return redirect('main:index')
	context = {}
	products = Product.objects.all()
	context = {
		'products' : products,

	}
	return render(request,"main/products.html",context)


def editProductView(request,productId):
	context = {}
	product = get_object_or_404(Product, id=productId)	
	if not request.user.is_superuser:
		return redirect('main:index')
	if request.POST:
		form = EditProductForm(request.POST or None, request.FILES or None, instance=product)
		if form.is_valid():
			obj = form.save()
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
			'flag': product.flag,
			'image': product.image,
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
		comments = product.comments.all()
	except Http404: 
		return redirect('main:index')
	
	context = {
		'product' : product,
		'comments' : comments

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
