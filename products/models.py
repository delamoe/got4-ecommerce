from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.IntegerField(help_text='Available quantity in stock')
    available = models.BooleanField(default=True, help_text='Is the product currently available for purchase?')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True, help_text='A short description of the image.')

    def __str__(self):
        return f"Image for {self.product.name} - {self.alt_text or 'No Alt Text'}"
