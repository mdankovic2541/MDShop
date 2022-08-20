import json
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager




class AwesomeAccountManager(BaseUserManager):
	def create_user(self, email, username, password):
		if not email:
			raise ValueError("Users must have an email address.")
		if not username:
			raise ValueError("Users must have a username.")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	first_name					= models.CharField(verbose_name='First name', max_length=60)
	last_name					= models.CharField(verbose_name='Last name', max_length=60)
	email						= models.EmailField(verbose_name='E-mail', max_length=60, unique=True)
	username					= models.CharField(max_length=16, unique=True)
	street_name = models.CharField(max_length=60)
	street_number = models.CharField(max_length=20)
	city =  models.CharField(max_length=50)
	postal_code =  models.CharField(max_length=50)
	country =  models.CharField(max_length=50)
	date_joined					= models.DateField(verbose_name='Date joined', auto_now_add=True)
	last_login					= models.DateField(verbose_name='Last login', auto_now_add=True)
	is_admin					= models.BooleanField(default=False)
	is_active					= models.BooleanField(default=True)
	is_staff					= models.BooleanField(default=False)
	is_superuser				= models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = AwesomeAccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True




