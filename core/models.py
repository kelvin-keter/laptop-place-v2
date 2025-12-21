from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Unique ID for the URL (e.g. gaming-laptops)")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Pricing (KES)
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Current Price in KES")
    old_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, help_text="Previous Price (to show discount)")
    
    # Media
    image = models.ImageField(upload_to='products/')
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Tick this to show on the Homepage")
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    # Helper to calculate discount percentage
    def get_discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return int(discount)
        return 0
    