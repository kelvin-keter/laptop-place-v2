from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Review

# --- CUSTOM BRANDING ---
admin.site.site_header = "Laptop Place Kenya Admin"
admin.site.site_title = "Laptop Place Manager"
admin.site.index_title = "Inventory Dashboard"

# --- HELPER ACTIONS ---
@admin.action(description='Duplicate selected products')
def duplicate_products(modeladmin, request, queryset):
    """
    Copies the selected products so you don't have to re-type everything
    for similar laptops.
    """
    for product in queryset:
        product.pk = None  # Resetting the ID creates a new copy
        product.name = f"{product.name} (Copy)" # Add (Copy) to name
        product.is_featured = False # Reset featured status
        product.save()

# --- INLINES ---
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0  # Don't show empty rows by default, keeps it clean
    readonly_fields = ('created_at',)
    can_delete = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Total Laptops'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # --- LOAD CUSTOM THEME CSS ---
    class Media:
        css = {
            'all': ('css/admin_theme.css',)
        }

    # 1. LIST VIEW (What you see on the dashboard)
    list_display = ('image_preview', 'name', 'price_display', 'category', 'condition', 'in_stock', 'is_featured')
    list_display_links = ('image_preview', 'name') # Click image or name to edit
    list_per_page = 20
    
    # 2. FILTERS (Side bar)
    list_filter = ('category', 'condition', 'in_stock', 'is_featured', 'usage')
    search_fields = ('name', 'description', 'processor')
    
    # 3. ACTIONS (The "Duplicate" magic)
    actions = [duplicate_products]
    
    # 4. QUICK EDIT (Change these without opening the product)
    list_editable = ('price', 'in_stock', 'is_featured')
    
    # 5. FORM LAYOUT (Grouping fields logically)
    save_on_top = True
    
    fieldsets = (
        ('Product Identity', {
            'fields': (
                ('category', 'name'), # Side by side
                'image',
            )
        }),
        ('Sales & Pricing', {
            'fields': (
                ('price', 'old_price'), 
                ('in_stock', 'condition'),
                ('is_featured', 'usage')
            ),
            'classes': ('collapse', 'open'), # Collapsible but open by default
        }),
        ('Core Specs (Critical)', {
            'fields': (
                ('processor', 'ram'),
                ('storage', 'storage_type'),
                'screen_size'
            )
        }),
        ('Detailed Features', {
            'classes': ('collapse',), # Collapsed by default to save space
            'fields': ('type', 'touchscreen', 'backlit_keyboard', 'fingerprint_sensor', 'description')
        }),
    )

    inlines = [ReviewInline]

    # --- CUSTOM HELPERS ---
    
    def image_preview(self, obj):
        """Shows a small thumbnail in the admin list"""
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image"

    def price_display(self, obj):
        return f"KES {obj.price:,}"
    price_display.short_description = "Price"
    price_display.admin_order_field = 'price'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'comment')