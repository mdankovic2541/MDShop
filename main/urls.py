from django.urls import path
from .views import (
    indexView,
    addProduct,
    kidswearView,
    menswearView,
    productDetail,
    usersView,
    womenswearView,
    productsView,

)


app_name = 'main'

urlpatterns = [
    path('', indexView, name='index'),
    path('add_product', addProduct, name='addProduct'),
    path('product_detail/<int:productId>',productDetail, name='productDetail'),
    path('menswear',menswearView, name='menswear'),
    path('womenswear',womenswearView, name='womenswear'),
    path('kidswear',kidswearView, name='kidswear'),
    path('users',usersView, name='users'),
    path('products',productsView, name='products'),
]