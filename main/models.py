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
	name					= models.CharField(max_length=256, blank=False, null=False, unique=True)

	def __str__(self):
		return self.name

	def getCount(self):
		return self.brands.count()


class Product(models.Model):
	class ClothesCollection(models.TextChoices):
		OUT_OF_COLLECTION = 'NO', _('Out of collection')
		SPRING = 'SP', _('Spring')
		SUMMER = 'SM', _('Summmer')
		AUTUMN = 'AT', _('Autumn')
		WINTER = 'WT', _('Winter')
	class ClothesFlag(models.TextChoices):
		NEW = 'N', _('NEW')
		POPULAR = 'P', _('POPULAR')
		NONE = 'X', _('NONE')
	class ClothesType(models.TextChoices):
		MALE = 'M', _('Male')
		FEMALE = 'F', _('Female')
		UNISEX = 'U', _('Unisex')
		KIDS = 'K', _('Kids')
	
	class ClothesSize(models.TextChoices):
		EXTRA_SMALL = 'XS', _('Extra small')
		SMALL = 'RS', _('Small')
		MEDIUM = 'RM', _('Medium')
		LARGE = 'RL', _('Large')
		EXTRA_LARGE = 'XL', _('Extra large')
		EXTRA_EXTRA_LARGE = '2L', _('Extra extra large')
	
	quantity				= models.IntegerField(null=False,blank=False)
	title					= models.CharField(null=False,blank=False,max_length=80)
	collection				= models.CharField(max_length=2, choices=ClothesCollection.choices, default=ClothesCollection.OUT_OF_COLLECTION, null=False, blank=False)
	year					= models.IntegerField(_('year'), validators=[MinValueValidator(1984), max_value_current_year], default=current_year)	
	brand					= models.ForeignKey(Brand, on_delete=models.CASCADE, null=False, blank=False, related_name='brands')
	isBranded				= models.BooleanField()
	size					= models.CharField(choices=ClothesSize.choices, max_length=2, default=ClothesSize.EXTRA_SMALL, null=False, blank=False)
	type					= models.CharField(max_length=1, choices=ClothesType.choices, default=ClothesType.UNISEX, null=False, blank=False)
	price					= models.DecimalField(max_digits=6, decimal_places=2)	
	flag					= models.CharField(max_length=1, choices=ClothesFlag.choices, default=ClothesFlag.NEW, null=False, blank=False)
	image					= models.ImageField(upload_to=uploadLocation, null=False, blank=False)


	def __str__(self):
		return f'product: {self.title}'

	def getCollection(self):
		return self.get_collection_display()

	def getFlag(self):
		return self.get_flag_display()

	def getType(self):
		return self.get_type_display()
	
	def getSize(self):
		return self.get_size_display()


@receiver(post_delete, sender=Product)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)


class Comment(models.Model):  
	description				= models.CharField(max_length=250)
	product					= models.ForeignKey(Product,on_delete=models.CASCADE, related_name='comments')
	createdAt				= models.DateTimeField(auto_now_add=True)
	account					= models.ForeignKey(Account,on_delete=models.CASCADE)

	def __str__(self):
	   return f'Comment:{self.description}'


class Cart(models.Model):
	user					= models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name='cart')
	product					= models.ManyToManyField(Product, related_name='products')

	def countProducts(self):
		if self.product:
			return self.product.count()
		else:
			return 0
	
	def getTotalPrice(self):
		price = 0
		for product in self.product.all():
			price += product.price
		return price

	def __str__(self):
		return f'{self.user}\'s cart'
	