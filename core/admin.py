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
    # --- LOAD CUSTOM THEME CSS ---
    class Media:
        css = {
            'all': ('css/admin_theme.css',)
        }

    # 1. LIST VIEW
    list_display = ('name', 'price', 'condition', 'ram', 'category', 'is_featured', 'in_stock')
    list_per_page = 20  # Show 20 items per page instead of 100 for cleaner look
    
    # 2. FILTERS (Added ordering for better UX)
    list_filter = ('category', 'condition', 'in_stock', 'is_featured', 'ram', 'touchscreen')
    ordering = ('-id',)  # Newest items first
    
    # 3. SEARCH
    search_fields = ('name', 'description', 'processor')
    
    # 4. QUICK EDIT
    list_editable = ('price', 'in_stock', 'is_featured', 'condition')
    
    # 5. FORM LAYOUT
    save_on_top = True  # Puts a "Save" button at the top of the page too
    
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