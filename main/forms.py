from django import forms
from .models import Product, Brand, current_year, year_choices

class CreateProductForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['brand'].disabled = True if self.initial.get('isBranded') == True else False
		self.fields['brand'].disabled = True if self.initial.get('isBranded') == True else False

	year = forms.TypedChoiceField(coerce=int, choices=year_choices, widget=forms.Select(attrs={
				'class': 'form-control',
			}), initial=current_year)
	brand = forms.ModelChoiceField(queryset= Brand.objects.all(),  widget=forms.Select(attrs={				
		    	'class': 'form-control',
		    	'name': 'Brand',
		    	'id': 'id_brand',
		    	'required': True,
	}), empty_label='Pick a Brand')
	class Meta:
		model = Product
		fields = ['title', 'collection', 'year', 'quantity', 'type', 'flag', 'brand', 'size', 'price', 'image']
		widgets = {
	    	'title': forms.TextInput(attrs={
		    	'class': 'form-control',
		    	'type': 'text',
		    	'name': 'Title',
		    	'id': 'id_title',
		    	'placeholder': 'Title',
		    	'maxlength': '80',
		    	'required': True,
		    	'autofocus': True,
		    }), 
			'collection': forms.Select(choices=Product.ClothesCollection, attrs={
		    	'class': 'form-control',
		    	'name': 'Collection',
		    	'id': 'id_collection',
		    	'required': True
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
			'type': forms.Select(choices=Product.ClothesType, attrs={
				'class': 'form-control',
		    	'name': 'Type',
		    	'id': 'id_type',
		    	'required': True
			}),
			'size': forms.Select(choices=Product.ClothesSize.choices, attrs={
				'class': 'form-control',
		    	'name': 'Size',
		    	'id': 'id_size',
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
			'flag': forms.Select(choices=Product.ClothesFlag, attrs={
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


class CreateBrandForm(forms.ModelForm):
	class Meta:
		model = Brand
		fields = ['name']
		widgets = {			
	    	'name': forms.TextInput(attrs={
		    	'class': 'form-control',
		    	'type': 'text',
		    	'name': 'Name',
		    	'id': 'id_name',
		    	'placeholder': 'Name',
		    	'maxlength': '80',
		    	'required': True,
		    	'autofocus': True,
		    }), 
		}