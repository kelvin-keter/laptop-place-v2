from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_featured', 'in_stock')
    list_filter = ('category', 'is_featured', 'in_stock')
    search_fields = ('name', 'description')
    list_editable = ('price', 'in_stock', 'is_featured')