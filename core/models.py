from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Unique ID for the URL (e.g. hp-laptops)")

    class Meta:
        # FIX: Changes "Categories" to "Brands" in the Admin Panel
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

class Product(models.Model):
    # --- DROPDOWN CHOICES ---
    CONDITION_CHOICES = [
        ('New', 'Brand New'),
        ('Refurbished', 'Ex-UK Refurbished'),
        ('Used', 'Used - Good Condition'),
    ]
    
    RAM_CHOICES = [
        ('4GB', '4GB'),
        ('8GB', '8GB'),
        ('16GB', '16GB'),
        ('32GB', '32GB'),
        ('64GB', '64GB'),
    ]
    
    STORAGE_TYPE_CHOICES = [
        ('SSD', 'SSD (Fast)'),
        ('HDD', 'HDD (Large Storage)'),
        ('NVMe', 'NVMe (Super Fast)'),
    ]

    # --- NEW: USAGE & TYPE CHOICES ---
    USAGE_CHOICES = [
        ('Everyday', 'Everyday Laptops'),
        ('Business', 'Business/Enterprise Laptops'),
        ('Premium', 'Premium Laptops'),
        ('Gaming', 'Gaming Laptops'),
        ('Student', 'Student Laptops'),
    ]

    TYPE_CHOICES = [
        ('Standard', 'Standard Laptop'),
        ('X360', 'X360 / Convertible'),
        ('Detachable', 'Detachable'),
        ('Slim', 'Ultrabook / Slim'),
    ]

    # --- BASIC INFO ---
    # FIX: Added verbose_name="Brand" so the form label says "Brand"
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Brand")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # --- PRICING (KES) ---
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Current Price in KES")
    old_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, help_text="Previous Price (to show discount)")
    
    # --- COMMERCIAL INFO ---
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, default='Refurbished')
    
    # --- NEW: CLASSIFICATION FIELDS ---
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, default='Everyday', help_text="Best use case (e.g. Student, Gaming)")
    laptop_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Standard', help_text="Physical style (e.g. X360, Slim)")
    
    # --- TECHNICAL SPECS ---
    processor = models.CharField(max_length=200, default='Intel Core i5', help_text="e.g. Intel Core i5 6th Gen")
    ram = models.CharField(max_length=10, choices=RAM_CHOICES, default='8GB')
    storage = models.CharField(max_length=50, default='256GB', help_text="e.g. 256GB")
    storage_type = models.CharField(max_length=10, choices=STORAGE_TYPE_CHOICES, default='SSD')
    screen_size = models.CharField(max_length=50, default='14 inch', help_text="e.g. 14 inch FHD")
    
    # --- KEY FEATURES ---
    touchscreen = models.BooleanField(default=False)
    backlit_keyboard = models.BooleanField(default=False)
    fingerprint_sensor = models.BooleanField(default=False)
    
    # --- MEDIA & STATUS ---
    image = models.ImageField(upload_to='products/')
    is_featured = models.BooleanField(default=False, help_text="Tick this to show on the Homepage")
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return int(discount)
        return 0

# --- CUSTOMER REVIEWS MODEL ---
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Customer Name")
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s review on {self.product.name}"
    
    def stars_range(self):
        return range(self.rating)

# --- NEW: PRODUCT GALLERY (FOR MULTIPLE PHOTOS) ---
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery/')
    
    def __str__(self):
        return f"Gallery Image for {self.product.name}"