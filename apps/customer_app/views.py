from django.shortcuts import render, redirect, reverse
from .models import Category, Product, Image
import os

# Create your views here.
def index(request):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    # print(logged_user)
    categories = Category.objects.all()
    products = Product.objects.all().order_by('category')
    images = Image.objects.all()
    context = {
        'logged_user': logged_user,
        'categories': categories,
        'products': products,
        'images': images
    }
    return render(request, 'index.html', context)

def browse(request, category_name):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    # print(logged_user)
    category = Category.objects.get(name = category_name)
    products = Product.objects.filter(category = category)
    context = {
        'logged_user': logged_user,
        'products': products
    }
    return render(request, 'browse.html', context)

def user(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    else:
        logged_user = request.session['logged_user']
    return render(request, 'user-dashboard.html')
