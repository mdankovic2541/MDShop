from django.db import models

from account.models import Account

# Create your models here.

class Comment(models.Model):  
    description = models.CharField(null=True, blank=True,max_length=250)

    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    def __str__(self):
       return f'Comment:{self.description}'
        
class Product(models.Model):
    quantity = models.IntegerField(null=False,blank=False)
    title = models.CharField(null=False,blank=False,max_length=80)
    collection = models.CharField(null=False,blank=False,max_length=80)
    brand = models.CharField(null=False,blank=False,max_length=80)
    type = models.CharField(null=False,blank=False,max_length=80)
    size = models.CharField(null=False,blank=False,max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    flag = models.CharField(null=False,blank=False,max_length=80)

    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'product: {self.title}'

