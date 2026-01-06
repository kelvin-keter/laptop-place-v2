from django import forms
from .models import Product

# Custom widget to allow selecting multiple files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductUploadForm(forms.ModelForm):
    # Field for the cover image (Single)
    image = forms.ImageField(label="Main Cover Image", widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    # Field for the gallery (Multiple)
    gallery_images = MultipleFileField(label="Additional Gallery Photos (Select up to 5)", required=False)

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'price', 'old_price', 'image', 'description', 
            'condition', 'in_stock', 'is_featured', 
            'usage', 'laptop_type',  # Matches your model field
            'processor', 'ram', 'storage', 'storage_type', 'screen_size',
            'touchscreen', 'backlit_keyboard', 'fingerprint_sensor'
        ]
        
    def __init__(self, *args, **kwargs):
        super(ProductUploadForm, self).__init__(*args, **kwargs)
        
        # Standard Styling
        for field_name, field in self.fields.items():
            if field_name not in ['gallery_images', 'image']:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': f'Enter {field.label}'
                })
            
        # Checkbox Styling
        checkbox_fields = ['in_stock', 'is_featured', 'touchscreen', 'backlit_keyboard', 'fingerprint_sensor']
        for box in checkbox_fields:
            if box in self.fields:
                self.fields[box].widget.attrs.update({'class': 'form-check-input'})