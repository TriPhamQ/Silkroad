from django.shortcuts import render, redirect, reverse
from .models import Category, Product, Image
import os

# Create your views here.
def index(request):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    print(logged_user)
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

def user(request):
    return render(request, 'user-dashboard.html')
