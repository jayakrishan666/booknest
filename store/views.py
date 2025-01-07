from django.shortcuts import render
from .models import Product

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def index(request):
    products = Product.objects.all()  # Retrieve all products from the database
    return render(request, 'index.html', {'products': products})

def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products': products})




from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import CustomUser
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # Get the category by ID
    products = Product.objects.filter(category=category)  # Get products related to that category
    return render(request, 'category_products.html', {'category': category, 'products': products})

import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        # Username validation: only alphabets and between 4-20 characters
        if not re.match(r'^[a-zA-Z]{4,20}$', username):
            messages.error(request, 'Username must be 4-20 characters long and contain only letters.')
            return redirect('signup')

        # Password validation: check length and complexity
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('signup')
        if not re.search(r'[A-Z]', password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return redirect('signup')
        if not re.search(r'[a-z]', password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            return redirect('signup')
        if not re.search(r'[0-9]', password):
            messages.error(request, 'Password must contain at least one digit.')
            return redirect('signup')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>).')
            return redirect('signup')
        if username.lower() in password.lower():
            messages.error(request, 'Password must not contain the username.')
            return redirect('signup')

        # Confirm password check
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        # Check if the username or email is already taken
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')
        
        # Create and save the new user
        user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'signup.html')






from django.contrib import messages, auth
from django.contrib.auth import authenticate, login

def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
            
    
    return render(request, 'login.html')
    

def index(request):
    categories = Category.objects.all()  # Get all categories
    products = Product.objects.all()  # Get all products, or adjust as needed
    return render(request, 'index.html', {'categories': categories, 'products': products})

def home(request):
    categories = Category.objects.all()  # Get all categories
    products = Product.objects.all()  # Get all products, or adjust as needed
    return render(request, 'home.html', {'categories': categories, 'products': products})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_cost = sum(item.total_price() for item in cart_items)

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total_cost": total_cost,
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1  # Increase quantity if the product is already in the cart
    cart_item.save()

    return redirect('cart_view')  # Redirect to the Cart page after adding to cart


from django.views.decorators.http import require_POST

@require_POST
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get("quantity", 1))
    cart_item.quantity = quantity
    cart_item.save()
    return redirect("cart_view")

@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("cart_view")


from django.shortcuts import render, redirect
from .models import Category, Product, CustomUser
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    categories = Category.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'admin_page.html', {'categories': categories, 'users': users})

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('admin_dashboard')

@login_required
def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        category_id = request.POST.get('category_id')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        category = Category.objects.get(id=category_id)
        Product.objects.create(title=title, author=author, price=price, category=category, quantity=quantity, image=image)
        return redirect('admin_dashboard')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Product, CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Product  # Assuming models are named `Category` and `Product`
from django.views.decorators.http import require_POST


@login_required
def admin_dashboard(request):
    categories = Category.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'admin_page.html', {'categories': categories, 'users': users})

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        messages.success(request, 'Category added successfully!')
        return redirect('admin_dashboard')

@login_required
def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        category_id = request.POST.get('category_id')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        category = Category.objects.get(id=category_id)
        Product.objects.create(title=title, author=author, price=price, category=category, quantity=quantity, image=image)
        messages.success(request, 'Product added successfully!')
        return redirect('admin_dashboard')

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, "Category added successfully!")
        else:
            messages.error(request, "Category name cannot be empty.")
        return redirect('admin_dashboard')  # Redirect to your admin dashboard URL
    return render(request, 'admin_page.html')  # Render the dashboard page with categories



from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.contrib.auth.models import User
from store.models import CustomUser 
from django.contrib.auth.models import User

# Admin Dashboard View
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Product, Category

def admin_dashboard(request):
    User = get_user_model()  # Dynamically get the user model (CustomUser or default User)
    users = User.objects.all()  # Get all users from the appropriate model
    products = Product.objects.all()  # Get all products
    categories = Category.objects.all()  # Get all categories

    return render(request, 'admin_page.html', {
        'products': products,
        'categories': categories,
        'users': users,
    })

# Add Category View
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('admin_dashboard')
    return render(request, 'add_category.html')

# Add Product View
def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        category_id = request.POST.get('category_id')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')

        if title and author and price and category_id and quantity:
            category = Category.objects.get(id=category_id)
            Product.objects.create(
                title=title,
                author=author,
                price=price,
                category=category,
                quantity=quantity,
                image=image
            )
            return redirect('admin_dashboard')
    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})

# Edit Product View
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Category

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)  # Get the existing product to edit

    if request.method == 'POST':
        # Update the product fields with the submitted form data
        product.title = request.POST.get('title', product.title)
        product.author = request.POST.get('author', product.author)
        product.price = request.POST.get('price', product.price)
        product.quantity = request.POST.get('quantity', product.quantity)

        # Update category if selected
        category_id = request.POST.get('category_id')
        if category_id:
            product.category = Category.objects.get(id=category_id)

        # Update the image if a new image is uploaded
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        # Save the updated product
        product.save()

        # Redirect to the product edit page after saving
        return redirect('edit_product', product_id=product.id)  # Make sure to pass the product_id

    # Get the list of categories to show in the form
    categories = Category.objects.all()

    return render(request, 'edit_product.html', {'product': product, 'categories': categories})


from django.contrib.auth.models import User
# Edit Category View
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_category.html', {'category': category})

# Edit User View
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_user.html', {'user': user})

from django.shortcuts import get_object_or_404, redirect
from .models import Category

def remove_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect('admin_dashboard')  # Redirect back to the admin dashboard after deletion

from django.shortcuts import get_object_or_404, redirect
from .models import Product

def remove_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('admin_dashboard')  # Redirect back to the admin dashboard after deletion

from .models import CustomUser  # Ensure you're importing the correct model

def remove_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)  # Use CustomUser instead of User
    user.delete()
    return redirect('admin_dashboard')
  # Redirect back to the admin dashboard after deletion





# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cart, Order, OrderItem

def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_cost = sum(item.total_price() for item in cart_items)
    
    if request.method == "POST":
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        
        # Create the order
        order = Order.objects.create(
            user=request.user,
            address=address,
            phone_number=phone_number
        )
        
        # Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
            
            # Update product quantity in stock
            item.product.quantity -= item.quantity 
            item.product.save()
        
        # Clear the cart after order is placed
        cart_items.delete()

        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_cost': total_cost
    })

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
import re  # For regex validation

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check if the username and email are valid
        try:
            user = CustomUser.objects.get(username=username, email=email)
            
            # Password validation logic
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
            elif len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
            elif not re.search(r'[A-Z]', new_password):
                messages.error(request, "Password must include at least one uppercase letter.")
            elif not re.search(r'[a-z]', new_password):
                messages.error(request, "Password must include at least one lowercase letter.")
            elif not re.search(r'\d', new_password):
                messages.error(request, "Password must include at least one number.")
            elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                messages.error(request, "Password must include at least one special character.")
            else:
                # Update the password
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successful. Please log in.")
                return redirect('login1')
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid username or email.")

    return render(request, 'forgot_password.html')


from django.shortcuts import render, get_object_or_404
from .models import CustomUser, Cart, Order

def user_details_view(request, user_id):
    # Fetch the user by ID
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Fetch the user's cart
    cart = get_object_or_404(Cart, user=user)
    
    # Fetch the user's orders
    orders = Order.objects.filter(user=user)
    
    context = {
        'user': user,
        'cart': cart,  # Pass the cart instance instead of cart items
        'orders': orders,
    }
    
    return render(request, 'user_details.html', context)





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login2(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check for admin credentials
            if username == "admin" and password == "admin":
                return redirect("admin_page")  # Replace with the name of your admin page URL
            else:
                return redirect("index")  # Redirect to the default page
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")


def admin_page(request):
    return render(request, "admin_page.html")

def adminlogin(request):
    return render(request, 'adminlogin.html')

from django.shortcuts import render
from .models import Order

def orders_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated
    
    # Fetch all orders for the logged-in user
    user_orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    context = {
        'orders': user_orders
    }
    return render(request, 'orders.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order

def cancel_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.is_confirmed:
        messages.error(request, "Order cannot be canceled as it is already confirmed.")
    else:
        order.delete()
        messages.success(request, "Order has been successfully canceled.")
    
    return redirect('orders')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm

@login_required
def edit_profile(request):
    user = request.user  # The logged-in user
    if request.method == 'POST':
        # If the form is submitted, we update the user details
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        # You can add more fields here if needed
        user.save()
        messages.success(request, "Your details have been updated successfully.")
        return redirect('edit_profile')  # Redirect to the same page after saving

    # Display the form with the current user data
    return render(request, 'edit_profile.html', {'user': user})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Fetch the reviews for the product
    reviews = Review.objects.filter(product=product)
    
    if request.method == 'POST' and request.user.is_authenticated:
        # Handle review submission
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            # Save the new review
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            return redirect('product_detail', product_id=product.id)
        else:
            return HttpResponse("Invalid form submission", status=400)
    
    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'product_detail.html', context)
