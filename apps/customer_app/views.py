from django.shortcuts import render, redirect, reverse
from .models import Category, Product, Image, Cart, Order, OrderProduct, BillingAddress, ShippingAddress
import os, math

# Create your views here.
def index(request):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    # print(logged_user)
    categories = Category.objects.all()
    products = Product.objects.filter(ongoing = True).order_by('category')
    images = Image.objects.all()
    context = {
        'logged_user': logged_user,
        'categories': categories,
        'products': products,
        'images': images
    }
    return render(request, 'index.html', context)

def browse(request, category_name, current_page):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    # print(logged_user)
    category = Category.objects.get(name = category_name)
    products = Product.objects.filter(category = category)
    page_size = 15
    product_start = (int(current_page)-1)*page_size
    product_end = (int(current_page))*page_size
    max_pages = math.ceil(len(products)/page_size)
    products_out = Product.objects.filter(category = category).filter(ongoing = True)[product_start:product_end]
    context = {
        'logged_user': logged_user,
        'products': products_out
    }
    return render(request, 'browse.html', context)

def user(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    else:
        logged_user = request.session['logged_user']
    return render(request, 'user-dashboard.html')
