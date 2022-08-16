from django.db import models
from account.models import Account

import json
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now

# Create your models here.


        
class Product(models.Model):
    quantity = models.IntegerField(null=False,blank=False)
    title = models.CharField(null=False,blank=False,max_length=80)
    collection = models.CharField(null=False,blank=False,max_length=80)
    brand = models.CharField(null=False,blank=False,max_length=80)
    type = models.CharField(null=False,blank=False,max_length=80)
    size = models.CharField(null=False,blank=False,max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    flag = models.CharField(null=False,blank=False,max_length=80)


    def __str__(self):
        return f'product: {self.title}'


class Comment(models.Model):  
    description = models.CharField(max_length=250)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='comments')
    createdAt = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    def __str__(self):
       return f'Comment:{self.description}'

