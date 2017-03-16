from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from ..admin_app.models import Product
from ..customer_app.models import Cart
import re, bcrypt

# Create your views here.
def login_registration(request):
    print("Log in and registration")
    if 'logged_user' not in request.session:
        print("Not logged in")
        return render(request, 'login_registration.html')
    else:
        print("Already logged in")
        return redirect('/admin')

def register(request):
    print("Register")
    if request.method == 'POST':
        form = request.POST
        errors = User.objects.validate_registration(form)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            if User.objects.register(form):
                messages.success(request, "You have successfully created an account")
            else:
                messages.error(request, "Something went wrong")
    return redirect('/login_registration')

def login(request):
    print("Log in")
    if request.method != 'POST':
        return redirect('/login_registration')
    user = User.objects.login(request.POST)
    if user:
        request.session['logged_user'] = user.id
        if 'product_id' in request.session:
            product = Product.objects.get(id = int(request.session['product_id']))
            if int(request.session['product_quantity']) <= product.inventory:
                user = User.objects.get(id = request.session['logged_user'])
                try:
                    item = Cart.objects.get(user = user, product = product)
                except:
                    item = None
                if item:
                    item.quantity += int(request.session['product_quantity'])
                    item.save()
                else:
                    item = Cart.objects.create(quantity = request.session['product_quantity'], user = user, product = product)
            del request.session['product_id']
            del request.session['product_quantity']
        if user.id == 1:
            return redirect('/admin')
        else:
            return redirect('/')
    else:
        messages.error(request, "Invalid login")
        return redirect('/login_registration')

def clear_user(request):
    User.objects.all().delete()
    print("delete all user")
    return redirect('/')
