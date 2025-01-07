from django.db import models
from django.contrib.auth.models import AbstractUser

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.title

# CustomUser Model (inherits from AbstractUser)
class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

# Cart Model
class Cart(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return f"Cart of {self.user.username}"

# CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def total_price(self):
        return self.quantity * self.product.price


from django.contrib import admin
from .models import Category, Product, CustomUser, Cart, CartItem

# Define admin classes to customize the display
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)


# models.py
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.user.email} on {self.date_ordered}"

    def total_cost(self):
        return sum(item.total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.quantity * self.product.price

from django.db import models
from django.contrib.auth import get_user_model

# Product model
# Review model
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating out of 5
    comment = models.TextField()
    

    def __str__(self):
        return f"Review by {self.user} for {self.product.title}"
