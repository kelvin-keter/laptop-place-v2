from django.contrib import admin
from .models import Category, Product, Review

# --- CUSTOM BRANDING ---
admin.site.site_header = "Laptop Place Kenya Admin"
admin.site.site_title = "Laptop Place Manager"
admin.site.index_title = "Inventory Dashboard"

# This allows you to edit reviews directly inside the Product page
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1  # Number of empty review slots to show
    readonly_fields = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 1. LIST VIEW
    list_display = ('name', 'price', 'condition', 'ram', 'category', 'is_featured', 'in_stock')
    
    # 2. FILTERS
    list_filter = ('category', 'condition', 'in_stock', 'is_featured', 'ram', 'touchscreen', 'storage_type')
    
    # 3. SEARCH
    search_fields = ('name', 'description', 'processor')
    
    # 4. QUICK EDIT
    list_editable = ('price', 'in_stock', 'is_featured', 'condition')
    
    # 5. FORM LAYOUT
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

    # 6. ADD REVIEWS TO PRODUCT PAGE
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'product')
    search_fields = ('name', 'comment')
    readonly_fields = ('created_at',)