from django.urls import path
from .views import (
    addBrandView,
    brandsView,
    cartManagmentView,
    cartView,
    createCommentView,
    deleteBrandView,
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
    brandedClothesView
)


app_name = 'main'

urlpatterns = [
    path('', indexView, name='index'),
    path('add_product', addProductView , name='addProduct'),
    path('<int:brandId>/add_product', addProductView , name='addProduct'),

    path('product_detail/<int:productId>',productDetailView, name='productDetail'),
    path('edit_product/<int:productId>',editProductView, name='editProduct'),
    path('delete_product',deleteProductView, name='deleteProduct'),
    path('create_comment/<int:productId>',createCommentView, name='createComment'),
    path('delete_comment/<int:commentId>',deleteCommentView, name='deleteComment'),
    path('menswear',menswearView, name='menswear'),
    path('womenswear',womenswearView, name='womenswear'),
    path('kidswear',kidswearView, name='kidswear'),
    path('users',usersView, name='users'),
    path('products',productsView, name='products'),
    path('brands',brandsView, name='brands'),
    path('products/<int:brandId>', brandedClothesView, name='productsOfBrand'),
    
    path('delete_brand',deleteBrandView,name='deleteBrand'),
    path('create_brand', addBrandView, name='addBrand'),
    path('cart_managment', cartManagmentView, name='manageCart'),
    path('cart', cartView, name='cart'),
]