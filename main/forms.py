from socket import fromshare
from django import forms
from .models import Product

class CreateProductForm(forms.ModelForm):    
    class Meta:
        model = Product
        fields = ['title',
                'quantity',
              'collection',
              'brand',
              'type',
              'size',
              'price',
              'flag'
            ]
        widgets = {
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
            'collection': forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'name': 'Collection',
                    'id': 'id_collection',
                    'placeholder': 'Collection',
                    'maxlength': '80',
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
            'type': forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'name': 'Type',
                    'id': 'id_type',
                    'placeholder': 'Type',
                    'maxlength': '80',
                    'required': True
                    }), 
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
            'flag': forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'name': 'Flag',
                    'id': 'id_flag',
                    'placeholder': 'Flag',
                    'maxlength': '80',
                    'required': True
                    }),     
            
        }
