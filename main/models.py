from django.db import models
from account.models import Account
from django.db.models.signals import post_delete
from django.dispatch import receiver


def uploadLocation(instance, type):
	file_path = 'product/{type}/{title}-{brand}'.format(
		title=str(instance.title),
		brand=str(instance.brand),
		type=type
	)
	return file_path
		
class Product(models.Model):
	quantity				= models.IntegerField(null=False,blank=False)
	title					= models.CharField(null=False,blank=False,max_length=80)
	collection				= models.CharField(null=False,blank=False,max_length=80)
	brand					= models.CharField(null=False,blank=False,max_length=80)
	type					= models.CharField(null=False,blank=False,max_length=80)
	size					= models.CharField(null=False,blank=False,max_length=20)
	price					= models.DecimalField(max_digits=6, decimal_places=2)
	flag					= models.CharField(null=False,blank=False,max_length=80)
	image					= models.ImageField(upload_to=uploadLocation, null=False, blank=False)


	def __str__(self):
		return f'product: {self.title}'


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

