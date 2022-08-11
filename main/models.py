from django.db import models

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

