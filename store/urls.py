"""
URL configuration for BookNest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import forgot_password

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    # path('signup_view/', views.signup_view, name='signup_view'),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login1/',views.login1, name="login1"),
    path('home/',views.home,name = "home"),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('category/<int:id>/', views.category_products, name='category_products'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),  # Cart page
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category'),

    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),

    path('add_product/', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category'),

    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('remove_category/<int:category_id>/', views.remove_category, name='remove_category'),
    path('remove_product/<int:product_id>/', views.remove_product, name='remove_product'),
    path('remove_user/<int:user_id>/', views.remove_user, name='remove_user'),

    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

    path('forgot-password/', forgot_password, name='forgot_password'),
    
    path('user/<int:user_id>/details/', views.user_details_view, name='view_user_details'),
    
    path('login/', views.login1, name='login2'),
    path('admin-page/', views.admin_page, name='admin_page'),  # Add this
    path('', views.index, name='index'),
    path('admin-login/', views.adminlogin, name='adminlogin'),
    path('orders/', views.orders_view, name='orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
]
