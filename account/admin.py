from django.contrib import admin
from .models import Account, Address
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
	list_display = ('email', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser')
	search_fields = ('email', 'username')
	list_filter = ('is_active', 'is_admin', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
	readonly_fields = ('username', 'email', 'date_joined', 'last_login', 'address')
	
	filter_horizontal = ()
	fieldsets = ()


class AddressAdmin(admin.ModelAdmin):
	list_display = ('street_name', 'street_number', 'city', 'postal_code', 'country')
	search_fields = ('street_name', 'street_number', 'city', 'postal_code', 'country')
	list_filter = ()
	readonly_fields = ()

	filter_horizontal = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(Address, AddressAdmin)