from audioop import add
import json
from math import prod
import math
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import Http404
from django.http import HttpResponse, JsonResponse
from account.models import Account, Address
from main.forms import CreateProductForm, EditProductForm, CreateBrandForm
from .models import Brand, Cart, Product, Comment, Receipt
from main.helpers import isAjax

# Create your views here.

def indexView(request):
	context = {}
	products = Product.objects.all()
	if request.user.is_authenticated:
		cart = get_object_or_404(Cart, user=request.user)
		context['cart'] = cart
	context['products'] = products
	return render(request,"main/index.html",context)


def addProductView(request, brandId=None):
	context = {}
	isBranded = False
	if not request.user.is_superuser:
		return redirect('main:index')
	if brandId:
		brand = get_object_or_404(Brand, id=brandId)
		isBranded = True		
		form = CreateProductForm(request.POST or None, request.FILES or None, initial = { 'brand': brand, 'isBranded': True })
	else:
		form = CreateProductForm(request.POST or None, request.FILES or None, initial = { 'isBranded': False })
	if form.is_valid():
		obj = form.save(commit=False)
		obj.isBranded = True if brandId else False
		obj.save()
		productId = obj.id
		form = CreateProductForm()
		return redirect('main:productDetail', productId=productId)
	context = {
		'form': form,
		'isBranded': isBranded,
	}
	return render(request, 'main/addProduct.html', context)


def usersView(request):
	if not request.user.is_superuser:
		return redirect('main:index')
	
	return render(request,"main/users.html",{})

def usersJsonView(request):
	users = Account.objects.all()
	total = users.count()	
	_start = request.GET.get('start')
	_length = request.GET.get('length')
	if _start and _length:
		start = int(_start)
		length = int(_length)
		page = math.ceil(start / length) + 1
		per_page = length
		users = users[start:start + length]
	data = [user.to_dict_json() for user in users]
	response = {
		'data': data,
		'page': page,  # [opcional]
		'per_page': per_page,  # [opcional]
		'recordsTotal': total,
		'recordsFiltered': total,
	}
	return JsonResponse(response)


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

# def deleteCommentView(request,commentId):
# 	try:
# 		comment = get_object_or_404(Comment, id=commentId)
# 	except Comment.DoesNotExist:
# 		return HttpResponse("Comment not found",status = 404)
# 	except Exception:
# 		print(Exception)
# 		return HttpResponse("Internal Error",status= 500)
# 	comment.delete()
	
# 	return redirect('main:index')



def deleteCommentView (request):
	if request.method == "POST" and isAjax(request):
		commentId = request.POST.get('id', None)
		try:
			comment = get_object_or_404(Comment, id=commentId)
			comment.delete()
			return HttpResponse(json.dumps({ "good": True }), content_type="application/json")
		except Account.DoesNotExist:
			return HttpResponse(json.dumps({ "good": False }), content_type="application/json")



def productsView(request):
	if not request.user.is_superuser:
		return redirect('main:index')
	
	return render(request,"main/products.html",{})


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
			'front_image': product.front_image,
			'back_image': product.back_image,
		}
	)
	context = {
		'form': form,
		'product': product,
	}
	return render(request, 'main/editProduct.html', context)



# def deleteProductView(request,productId):
# 	try:
# 		product = get_object_or_404(Product, id=productId)
# 		if not request.user.is_superuser:
# 			return redirect('main:index')
# 	except Product.DoesNotExist:
# 		return HttpResponse("Product not found",status = 404)
# 	except Exception:
# 		return HttpResponse("Internal Error",status= 500)
# 	product.delete()
	
# 	return redirect('main:products')
	

def deleteProductView (request):
	if request.method == "POST" and isAjax(request):
		productId = request.POST.get('id', None)
		try:
			product = get_object_or_404(Product, id=productId)
			product.delete()
			return HttpResponse(json.dumps({ "good": True }), content_type="application/json")
		except Account.DoesNotExist:
			return HttpResponse(json.dumps({ "good": False }), content_type="application/json")



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


def productsJsonView(request):
	products = Product.objects.all()
	total = products.count()	
	_start = request.GET.get('start')
	_length = request.GET.get('length')
	if _start and _length:
		start = int(_start)
		length = int(_length)
		page = math.ceil(start / length) + 1
		per_page = length
		products = products[start:start + length]
	data = [product.to_dict_json() for product in products]
	response = {
		'data': data,
		'page': page,  
		'per_page': per_page,  
		'recordsTotal': total,
		'recordsFiltered': total,
	}
	return JsonResponse(response)


def menswearView(request):
	context = {}
	products = Product.objects.filter(Q(type__contains='M') | Q(type__contains='U')).all()
	brands = list(set(Brand.objects.filter(Q(brands__type__contains='M') | Q(brands__type__contains='U')).all()))
	sizes = list(set(Product.objects.values_list('size',flat=True)))
	context = {
		'products' : products,
		'nav':'Men',
		'brands': brands,
		'sizes' : sizes,
		

	}

	return render(request,"main/men.html",context)

	
def womenswearView(request):
	context = {}
	products = Product.objects.filter(Q(type__contains='F') | Q(type__contains='U')).all()
	context = {
		'products' : products,
		'nav':'Women',

	}

	return render(request,"main/women.html",context)

def kidswearView(request):
	context = {}
	products = Product.objects.filter(Q(type__contains='K')).all()
	context = {
		'products' : products,
		'nav':'Kids',

	}

	return render(request,"main/kids.html",context)


def addBrandView(request):
	if not request.user.is_superuser:
		return redirect('main:index')
	form = CreateBrandForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = CreateBrandForm()		
		return redirect('main:brands')
	context = {
		'form': form,
	}
	return render(request, 'main/addBrand.html', context)



def deleteBrandView (request):
	if request.method == "POST" and isAjax(request):
		brandId = request.POST.get('id', None)
		try:
			brand = get_object_or_404(Brand, id=brandId)
			brand.delete()
			return HttpResponse(json.dumps({ "good": True }), content_type="application/json")
		except Account.DoesNotExist:
			return HttpResponse(json.dumps({ "good": False }), content_type="application/json")


# TODO: Refactor others to work with DataTables
def brandsView(request):
	if not request.user.is_superuser:
		return redirect('main:index')
	return render(request, "main/brands.html", {})


def brandsJsonView(request):
	brands = Brand.objects.all()
	total = brands.count()	
	_start = request.GET.get('start')
	_length = request.GET.get('length')
	if _start and _length:
		start = int(_start)
		length = int(_length)
		page = math.ceil(start / length) + 1
		per_page = length
		brands = brands[start:start + length]
	data = [brand.to_dict_json() for brand in brands]
	response = {
		'data': data,
		'page': page,  # [opcional]
		'per_page': per_page,  # [opcional]
		'recordsTotal': total,
		'recordsFiltered': total,
	}
	return JsonResponse(response)
# TODO: End todo.


def brandedClothesView(request, brandId):
	if not request.user.is_superuser:
		return redirect('main:index')
	brand = get_object_or_404(Brand, id=brandId)
	products = Product.objects.filter(brand=brand).all()
	context = {
		'brand': brand,
		'products': products,
	}
	return render(request, 'main/clothesWithBrand.html', context)


def cartManagmentView(request):
	if request.method == "POST" and isAjax(request):
		productId = request.POST.get('id', None)
		user = Account.objects.get(id=request.user.id)
		product = Product.objects.get(id=productId)
		cart = get_object_or_404(Cart, user=user)
		if product in cart.product.all():
			cart.product.remove(product)
		else:
			cart.product.add(product)
		cart.save()
		return HttpResponse(json.dumps({ "good": True }), content_type="application/json")
	else:
		return redirect('main:index')


def cartView(request):
	cart = get_object_or_404(Cart, user=request.user)
	context = {
		'cart': cart,
	}
	return render(request, 'main/cart.html', context)


def checkoutView(request):
	return render(request, 'main/checkout.html', {})


def checkoutFinalView(request):
	if request.method == "POST":
		cartId = request.POST.get('id', None)
		receiptNumber =  request.POST.get('receiptNumber', None)
		cart = get_object_or_404(Cart, id=cartId)
		for product in cart.product.all():
			product.quantity -= 1
			product.save()
		cart.save()
		receipt = Receipt.objects.create(cart=cart, account=request.user, receiptNumber=receiptNumber)
		receipt.save()
		return JsonResponse({"good" : "True"})

def receiptView(request):
	context = {}	
	receipts = Receipt.objects.filter(account=request.user).all()
