from django.contrib import admin
from .models import Category, Product

# --- NEW: CUSTOM BRANDING ---
admin.site.site_header = "Laptop Place Kenya Admin"
admin.site.site_title = "Laptop Place Manager"
admin.site.index_title = "Inventory Dashboard"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 1. LIST VIEW
    # Added 'touchscreen' so you can see features at a glance
    list_display = ('name', 'price', 'condition', 'ram', 'category', 'is_featured', 'in_stock')
    
    # 2. FILTERS
    # Added 'touchscreen' and 'storage_type' to the sidebar filters
    list_filter = ('category', 'condition', 'in_stock', 'is_featured', 'ram', 'touchscreen', 'storage_type')
    
    # 3. SEARCH
    search_fields = ('name', 'description', 'processor')
    
    # 4. QUICK EDIT
    list_editable = ('price', 'in_stock', 'is_featured', 'condition')
    
    # 5. FORM LAYOUT (Kept your excellent grouping!)
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