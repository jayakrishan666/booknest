from django.contrib import admin
from .models import Product, Category, Cart, CartItem, CustomUser
from django.contrib.auth.admin import UserAdmin
from .models import Order, OrderItem

# Define admin classes for Product and Category
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'category')
    search_fields = ('title', 'author')
    list_filter = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Inline class for CartItem to display items in the CartAdmin
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'total_price')  # Specify fields to display
    readonly_fields = ('total_price',)  # Make total_price readonly

# CartAdmin with CartItem inline to display items within each cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [CartItemInline]  # Display CartItems in the Cart view

# Admin class for CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']

# Admin class for OrderItem
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

# Admin class for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number', 'date_ordered', 'is_confirmed')



from django.contrib import admin
from .models import Product, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('title', 'category', 'price')  # Add 'created_at' here

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating')
    search_fields = ['product__title', 'user__email']


admin.site.register(Review, ReviewAdmin)


# Register models and their respective admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CartItem)
