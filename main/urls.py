from django.urls import path
from .views import (
    createCommentView,
    deleteCommentView,
    editProductView,
    indexView,
    addProductView,
    kidswearView,
    menswearView,
    productDetailView,
    usersView,
    womenswearView,
    productsView,
    deleteProductView,

)


app_name = 'main'

urlpatterns = [
    path('', indexView, name='index'),
    path('add_product', addProductView , name='addProduct'),
    path('product_detail/<int:productId>',productDetailView, name='productDetail'),
    path('edit_product/<int:productId>',editProductView, name='editProduct'),
    path('delete_product/<int:productId>',deleteProductView, name='deleteProduct'),
    path('create_comment/<int:productId>',createCommentView, name='createComment'),
    path('delete_comment/<int:commentId>',deleteCommentView, name='deleteComment'),
    path('menswear',menswearView, name='menswear'),
    path('womenswear',womenswearView, name='womenswear'),
    path('kidswear',kidswearView, name='kidswear'),
    path('users',usersView, name='users'),
    path('products',productsView, name='products'),
]