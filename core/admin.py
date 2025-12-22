from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 1. LIST VIEW: What you see in the main table
    # I added 'ram' and 'condition' so you can quickly see specs
    list_display = ('name', 'price', 'condition', 'ram', 'category', 'is_featured', 'in_stock')
    
    # 2. FILTERS: Sidebar options to narrow down results
    list_filter = ('category', 'condition', 'ram', 'in_stock', 'is_featured')
    
    # 3. SEARCH: Search by name, description, or processor
    search_fields = ('name', 'description', 'processor')
    
    # 4. QUICK EDIT: Preserved your ability to edit these directly in the list
    list_editable = ('price', 'in_stock', 'is_featured')
    
    # 5. FORM LAYOUT: Grouping the fields nicely
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'image', 'description')
        }),
        ('Pricing & Status', {
            'fields': ('price', 'old_price', 'in_stock', 'is_featured', 'condition')
        }),
        ('Technical Specifications', {
            'fields': ('processor', 'ram', 'storage', 'storage_type', 'screen_size')
        }),
        ('Special Features', {
            'fields': ('touchscreen', 'backlit_keyboard', 'fingerprint_sensor')
        }),
    )