from socket import fromshare
from django import forms
from .models import Product, Comment, year_choices, current_year

class CreateProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'quantity', 'collection', 'year', 'brand', 'type', 'size', 'price', 'flag', 'image']
		year = forms.TypedChoiceField(coerce=int, choices=year_choices)
		widgets = {
			'year': forms.NumberInput(attrs={
				'class': 'form-control',
			}),
	    	'title': forms.TextInput(attrs={
		    	'class': 'form-control',
		    	'type': 'text',
		    	'name': 'Title',
		    	'id': 'id_title',
		    	'placeholder': 'Title',
		    	'maxlength': '80',
		    	'required': True,
		    	'autofocus': True
		    }), 
	    	'quantity': forms.NumberInput(attrs={
		    	'class': 'form-control',
		    	'type': 'number',
		    	'name': 'Quantity',
		    	'id': 'id_quantity',
		    	'min': '0',
		    	'value':'0',
		    	'required': True
		    }),
			'collection': forms.Select(choices=Product.Collection, attrs={
		    	'class': 'form-control',
		    	'name': 'Collection',
		    	'id': 'id_collection',
		    	'required': True
		    }),
			'type': forms.Select(choices=Product.ClothesType, attrs={
				'class': 'form-control',
		    	'name': 'Type',
		    	'id': 'id_type',
		    	'required': True
			}),
	    	'brand': forms.TextInput(attrs={
		    	'class': 'form-control',
		    	'type': 'text',
		    	'name': 'Brand',
		    	'id': 'id_brand',
		    	'placeholder': 'Brand',
		    	'maxlength': '80',
		    	'required': True
		    }),  
	    	# 'type': forms.TextInput(attrs={
		    # 	'class': 'form-control',
		    # 	'type': 'text',
		    # 	'name': 'Type',
		    # 	'id': 'id_type',
		    # 	'placeholder': 'Type',
		    # 	'maxlength': '80',
		    # 	'required': True
		    # }), 
	    	'size': forms.TextInput(attrs={
		    	'class': 'form-control',
		    	'type': 'text',
		    	'name': 'Size',
		    	'id': 'id_size',
		    	'placeholder': 'Size',
		    	'maxlength': '80',
		    	'required': True
		    }),         
	    	'price': forms.NumberInput(attrs={
		    	'class': 'form-control',
		    	'type': 'number',
		    	'name': 'Price',
		    	'id': 'id_price',
		    	'min': '0',
		    	'value':'0',
		    	'required': True
		    }), 
			'flag': forms.Select(choices=Product.Flag, attrs={
		    	'class': 'form-control',
		    	'name': 'Flag',
		    	'id': 'id_flag',
		    	'required': True
		    }),
			'image': forms.FileInput(attrs={
				'class': 'form-control',
				'type': 'file',
				'name': 'image',
				'id': 'id_image',
				'accept': 'image/*',
				'required': True
			})
		}


class EditProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'quantity', 'collection', 'year', 'brand','type','size','price','flag', 'image']
		
		def save(self, commit=True):
			product = self.instance
			product.title = self.cleaned_data['title']
			product.quantity = self.cleaned_data['quantity']
			product.collection = self.cleaned_data['collection']
			product.brand = self.cleaned_data['brand']
			product.type = self.cleaned_data['type']
			product.size = self.cleaned_data['size']
			product.price = self.cleaned_data['price']
			product.flag = self.cleaned_data['flag']
			if self.cleaned_data['image']:
				product.image = self.cleaned_data['image']
			
			if commit:
				product.save()
			return product
