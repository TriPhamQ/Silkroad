from django.shortcuts import render, redirect, reverse
from .models import User, Category, Product, Image, Cart, Order, OrderProduct, BillingAddress, ShippingAddress
import os, math

# Create your views here.
def index(request):
    # Use this next line to clear cart while test
    # Cart.objects.all().delete()
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    try:
        user = User.objects.get(id = logged_user)
    except:
        user = None
    if user:
        cart = Cart.objects.filter(user = user)
        cart_item = 0
        for item in range (0, cart.count()):
            cart_item += cart[item].quantity
        categories = Category.objects.all()
        products = Product.objects.filter(ongoing = True).order_by('category')
        images = Image.objects.all()
        context = {
            'logged_user': logged_user,
            'cart': cart,
            'cart_item': cart_item,
            'categories': categories,
            'products': products,
            'images': images
        }
    else:
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
    category = Category.objects.get(name = category_name)
    products = Product.objects.filter(category = category)
    page_size = 15
    product_start = (int(current_page)-1)*page_size
    product_end = (int(current_page))*page_size
    max_pages = math.ceil(len(products)/page_size)
    products_out = Product.objects.filter(category = category).filter(ongoing = True)[product_start:product_end]
    try:
        user = User.objects.get(id = logged_user)
    except:
        user = None
    if user:
        cart = Cart.objects.filter(user = user)
        cart_item = 0
        for item in range (0, cart.count()):
            cart_item += cart[item].quantity
        context = {
            'cart_item': cart_item,
            'logged_user': logged_user,
            'products': products_out
        }
    else:
        context = {
            'logged_user': logged_user,
            'products': products_out
        }
    return render(request, 'browse.html', context)

def product_page(request, product_id):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    try:
        user = User.objects.get(id = logged_user)
    except:
        user = None
    product = Product.objects.get(id = product_id)
    if user:
        cart = Cart.objects.filter(user = user)
        cart_item = 0
        for item in range (0, cart.count()):
            cart_item += cart[item].quantity
        categories = Category.objects.all()
        products = Product.objects.filter(ongoing = True).order_by('category')
        images = Image.objects.all()
        context = {
            'product': product,
            'logged_user': logged_user,
            'cart': cart,
            'cart_item': cart_item,
            'categories': categories,
            'products': products,
            'images': images
        }
    else:
        categories = Category.objects.all()
        products = Product.objects.filter(ongoing = True).order_by('category')
        images = Image.objects.all()
        context = {
            'product': product,
            'logged_user': logged_user,
            'categories': categories,
            'products': products,
            'images': images
        }
    return render(request, 'product-page.html', context)

def add_to_cart(request, product_id):
    if 'logged_user' not in request.session:
        form = request.POST
        request.session['product_id'] = product_id
        request.session['product_quantity'] = form['product_quantity']
        return redirect('/login_registration')
    else:
        logged_user = request.session['logged_user']
        product = Product.objects.get(id = product_id)
        if product.ongoing == True:
            form = request.POST
            if int(form['product_quantity']) <= product.inventory:
                user = User.objects.get(id = logged_user)
                try:
                    item = Cart.objects.get(user = user, product = product)
                except:
                    item = None
                if item:
                    item.quantity += int(form['product_quantity'])
                    item.save()
                else:
                    item = Cart.objects.create(quantity = form['product_quantity'], user = user, product = product)
        return redirect('/product/' + product_id)

def shopping_cart(request):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    try:
        user = User.objects.get(id = logged_user)
    except:
        user = None
    if user:
        cart = Cart.objects.filter(user = user)
        cart_item = 0
        raw_total = 0
        error = []
        for item in range (0, cart.count()):
            cart_item += cart[item].quantity
            raw_total += cart[item].quantity * cart[item].product.price
            if cart[item].quantity > cart[item].product.inventory:
                error.append(""+cart[item].product.name+" only has "+str(cart[item].product.inventory)+" left in stock but you selected "+str(cart[item].quantity)+", please change quantity")
        tax = round(float(raw_total)*0.075, 2)
        if raw_total > 0:
            shipping = 5.99
        else:
            shipping = 0.00
        total = round(tax + float(raw_total) + float(shipping), 2)
        context = {
            'error': error,
            'cart_item': cart_item,
            'cart': cart,
            'raw_total': raw_total,
            'tax': tax,
            'shipping': shipping,
            'total': total
        }
        return render(request, 'shopping-cart.html', context)
    else:
        return redirect('/')

def check_out(request):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    try:
        user = User.objects.get(id = logged_user)
    except:
        user = None
    if user:
        cart = Cart.objects.filter(user = user)
        cart_item = 0
        raw_total = 0
        error = []
        for item in range (0, cart.count()):
            cart_item += cart[item].quantity
            raw_total += cart[item].quantity * cart[item].product.price
            if cart[item].quantity > cart[item].product.inventory:
                error.append(""+cart[item].product.name+" only has "+str(cart[item].product.inventory)+" left in stock but you selected "+str(cart[item].quantity)+", please change quantity")
        tax = round(float(raw_total)*0.075, 2)
        if raw_total > 0:
            shipping = 5.99
        else:
            shipping = 0.00
        total = round(tax + float(raw_total) + float(shipping), 2)
        print(error)
        context = {
            'error': error,
            'cart_item': cart_item,
            'cart': cart,
            'raw_total': raw_total,
            'tax': tax,
            'shipping': shipping,
            'total': total
        }
        return render(request, 'check-out.html', context)
    else:
        return redirect('/')

def change_quantity(request, product_id):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    try:
        user = User.objects.get(id = logged_user)
    except:
        user = None
    if user:
        cart = Cart.objects.filter(user = user)
        cart_item = 0
        raw_total = 0
        form = request.POST
        item_to_change = cart.get(product_id = product_id)
        item_to_change.quantity = form['product_quantity']
        item_to_change.save()
        cart = Cart.objects.filter(user = user)
        error = []
        for item in range (0, cart.count()):
            cart_item += cart[item].quantity
            raw_total += cart[item].quantity * cart[item].product.price
            if cart[item].quantity > cart[item].product.inventory:
                error.append(""+cart[item].product.name+" only has "+str(cart[item].product.inventory)+" left in stock, please change quantity")
        tax = round(float(raw_total)*0.075, 2)
        if raw_total > 0:
            shipping = 5.99
        else:
            shipping = 0.00
        total = round(tax + float(raw_total) + float(shipping), 2)
        print(error)
        context = {
            'error': error,
            'cart_item': cart_item,
            'cart': cart,
            'raw_total': raw_total,
            'tax': tax,
            'shipping': shipping,
            'total': total
        }
        return redirect('/shopping-cart')
    else:
        return redirect('/')

def remove_cart_item(request, product_id):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    try:
        user = User.objects.get(id = logged_user)
    except:
        user = None
    if user:
        Cart.objects.get(user = user, product_id = product_id).delete()
        cart_item = 0
        raw_total = 0
        form = request.POST
        cart = Cart.objects.filter(user = user)
        error = []
        for item in range (0, cart.count()):
            cart_item += cart[item].quantity
            raw_total += cart[item].quantity * cart[item].product.price
            if cart[item].quantity > cart[item].product.inventory:
                error.append(""+cart[item].product.name+" only has "+str(cart[item].product.inventory)+" left in stock, please change quantity")
        tax = round(float(raw_total)*0.075, 2)
        if raw_total > 0:
            shipping = 5.99
        else:
            shipping = 0.00
        total = round(tax + float(raw_total) + float(shipping), 2)
        print(error)
        context = {
            'error': error,
            'cart_item': cart_item,
            'cart': cart,
            'raw_total': raw_total,
            'tax': tax,
            'shipping': shipping,
            'total': total
        }
        return redirect('/shopping-cart')
    else:
        return redirect('/')

def user(request):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    try:
        user = User.objects.get(id = logged_user)
    except:
        user = None
    if user:
        cart = Cart.objects.filter(user = user)
        cart_item = 0
        for item in range (0, cart.count()):
            cart_item += cart[item].quantity
        context = {
            'logged_user': logged_user,
            'cart_item': cart_item,
            'cart': cart
        }
        return render(request, 'user-dashboard.html', context)
    else:
        return redirect('/')
