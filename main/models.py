from typing import Collection
from django.db import models
from account.models import Account
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

def uploadLocation(instance, type):
	file_path = 'product/{type}/{title}-{brand}'.format(
		title=str(instance.title),
		brand=str(instance.brand),
		type=type
	)
	return file_path


def current_year():
	return datetime.date.today().year
		

def max_value_current_year(value):
	return MaxValueValidator(current_year())(value)


def year_choices():
	return [(r,r) for r in range(1984, datetime.date.today().year+1)]

class Brand(models.Model):
	brand					= models.CharField

class Product(models.Model):
	class Collection(models.TextChoices):
		SPRING = 'SP', _('Spring')
		SUMMER = 'SM', _('Summmer')
		AUTUMN = 'AT', _('Autumn')
		WINTER = 'WT', _('Winter')

	quantity				= models.IntegerField(null=False,blank=False)
	title					= models.CharField(null=False,blank=False,max_length=80)
	collection				= models.CharField(max_length=2, choices=Collection.choices, null=False, blank=False)
	year					= models.IntegerField(_('year'), validators=[MinValueValidator(1984), max_value_current_year], default=current_year)
	brand					= models.CharField(null=False,blank=False,max_length=80)
	type					= models.CharField(null=False,blank=False,max_length=80)
	size					= models.CharField(null=False,blank=False,max_length=20)
	price					= models.DecimalField(max_digits=6, decimal_places=2)
	flag					= models.CharField(null=False,blank=False,max_length=80)
	image					= models.ImageField(upload_to=uploadLocation, null=False, blank=False)

	def __str__(self):
		return f'product: {self.title}'

	def getCollection(self):
		return self.get_collection_display()


@receiver(post_delete, sender=Product)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)

class Comment(models.Model):  
	description = models.CharField(max_length=250)
	product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='comments')
	createdAt = models.DateTimeField(auto_now_add=True)
	account = models.ForeignKey(Account,on_delete=models.CASCADE)

	def __str__(self):
	   return f'Comment:{self.description}'

