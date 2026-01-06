from django import forms
from .models import Product

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'price', 'old_price', 'image', 'description', 
            'condition', 'in_stock', 'is_featured', 
            'usage', 'laptop_type',  # Note: matches your model field 'laptop_type'
            'processor', 'ram', 'storage', 'storage_type', 'screen_size',
            'touchscreen', 'backlit_keyboard', 'fingerprint_sensor'
        ]
        
    def __init__(self, *args, **kwargs):
        super(ProductUploadForm, self).__init__(*args, **kwargs)
        
        # 1. Loop through all fields to add standard Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter {field.label}'
            })
            
        # 2. Special styling for Checkboxes (they need different classes)
        checkbox_fields = ['in_stock', 'is_featured', 'touchscreen', 'backlit_keyboard', 'fingerprint_sensor']
        for box in checkbox_fields:
            if box in self.fields:
                self.fields[box].widget.attrs.update({'class': 'form-check-input'})