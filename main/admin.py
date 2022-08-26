from django.contrib import admin
from .models import Cart, Comment, Product, Brand
# Register your models here.

admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Brand)
admin.site.register(Cart)