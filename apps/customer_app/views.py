from django.shortcuts import render, redirect, reverse
from .models import User, Category, Product, Image, Cart, Order, OrderProduct, BillingAddress, ShippingAddress
import os, math, stripe

# Stripe
stripe.api_key = "sk_test_rcBDHXKJDHEK0uSNnRiLsorp"

# Create your views here.
def index(request):
    # Use this next line to clear cart while test
    # Cart.objects.all().delete()
    # Order.objects.all().delete()
    # OrderProduct.objects.all().delete()
    # BillingAddress.objects.all().delete()
    # ShippingAddress.objects.all().delete()
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
    categories = Category.objects.all()
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
            'categories': categories,
            'cart_item': cart_item,
            'logged_user': logged_user,
            'products': products_out
        }
    else:
        context = {
            'categories': categories,
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
            if cart[item].product.ongoing == False:
                error.append(""+cart[item].product.name+" sale has been discontinued, please remove from your cart")
            if cart[item].quantity > cart[item].product.inventory:
                if cart[item].product.ongoing == True:
                    error.append(""+cart[item].product.name+" only has "+str(cart[item].product.inventory)+" left in stock but you selected "+str(cart[item].quantity)+", please change quantity")
        tax = round(float(raw_total)*0.075, 2)
        if raw_total > 0:
            shipping = 5.99
        else:
            shipping = 0.00
        total = round(tax + float(raw_total) + float(shipping), 2)
        stripe_total = round((tax + float(raw_total) + float(shipping))*100, 2)
        context = {
            'error': error,
            'cart_item': cart_item,
            'cart': cart,
            'raw_total': raw_total,
            'tax': tax,
            'shipping': shipping,
            'total': total,
            'stripe_total': stripe_total
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
        if cart.count() >= 1:
            cart_item = 0
            raw_total = 0
            error = []
            for item in range (0, cart.count()):
                cart_item += cart[item].quantity
                raw_total += cart[item].quantity * cart[item].product.price
                if cart[item].product.ongoing == False:
                    error.append(""+cart[item].product.name+" sale has been discontinued, please remove from your cart")
                if cart[item].quantity > cart[item].product.inventory:
                    if cart[item].product.ongoing == True:
                        error.append(""+cart[item].product.name+" only has "+str(cart[item].product.inventory)+" left in stock but you selected "+str(cart[item].quantity)+", please change quantity")
            tax = round(float(raw_total)*0.075, 2)
            if raw_total > 0:
                shipping = 5.99
            else:
                shipping = 0.00
            total = round(tax + float(raw_total) + float(shipping), 2)
            stripe_total = round((tax + float(raw_total) + float(shipping))*100, 2)
            context = {
                'error': error,
                'cart_item': cart_item,
                'cart': cart,
                'raw_total': raw_total,
                'tax': tax,
                'shipping': shipping,
                'total': total,
                'stripe_total': stripe_total
            }
            return render(request, 'check-out.html', context)
        else:
            return redirect('/')
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

def place_order(request):
    if 'logged_user' not in request.session:
        logged_user = 0
    else:
        logged_user = request.session['logged_user']
    try:
        user = User.objects.get(id = logged_user)
    except:
        user = None
    if user:
        form = request.POST
        token = request.POST['stripeToken']
        cart = Cart.objects.filter(user = user)
        cart_item = 0
        raw_total = 0
        error = []
        for item in range (0, cart.count()):
            cart_item += cart[item].quantity
            raw_total += cart[item].quantity * cart[item].product.price
            if cart[item].product.ongoing == False:
                error.append(""+cart[item].product.name+" sale has been discontinued, please remove from your cart")
            if cart[item].quantity > cart[item].product.inventory:
                if cart[item].product.ongoing == True:
                    error.append(""+cart[item].product.name+" only has "+str(cart[item].product.inventory)+" left in stock but you selected "+str(cart[item].quantity)+", please change quantity")
        tax = round(float(raw_total)*0.075, 2)
        if raw_total > 0:
            shipping = 5.99
        else:
            shipping = 0.00
        total = round(tax + float(raw_total) + float(shipping), 2)
        stripe_total = round((tax + float(raw_total) + float(shipping))*100, 2)
        if len(error) < 1:
            print("Creating order")
            charge = stripe.Charge.create(
                amount = int(stripe_total),
                currency = "usd",
                description = "Charged "+str(stripe)+" to "+str(User.objects.get(id = user.id)),
                source = token,
            )
            if charge:
                billing_address = BillingAddress.objects.create(
                    first_name = form['bill_first_name'],
                    last_name = form['bill_last_name'],
                    address = form['bill_address'],
                    city = form['bill_city'],
                    state = form['bill_state'],
                    zipcode = form['bill_zip']
                )
                shipping_address = ShippingAddress.objects.create(
                    first_name = form['ship_first_name'],
                    last_name = form['ship_last_name'],
                    address = form['ship_address'],
                    city = form['ship_city'],
                    state = form['ship_state'],
                    zipcode = form['ship_zip']
                )
                order = Order.objects.create(
                    user = user,
                    total = total,
                    tax = tax,
                    shipping_cost = shipping,
                    billing = billing_address,
                    shipping = shipping_address,
                    stripe_id = charge['id']
                )
                for item in range (0, cart.count()):
                    OrderProduct.objects.create(
                        quantity = cart[item].quantity,
                        order = order,
                        product = cart[item].product
                    )
                    change_inventory = cart[item].product
                    change_inventory.inventory -= cart[item].quantity
                    change_inventory.save()
                cart.delete()
            return redirect('/check-out')
        else:
            print("Error")
            return redirect('/check-out')
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
        orders = Order.objects.filter(user = user)
        context = {
            'logged_user': logged_user,
            'cart_item': cart_item,
            'cart': cart,
            'orders': orders
        }
        return render(request, 'user-dashboard.html', context)
    else:
        return redirect('/')

def view_order(request, order_id):
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
        order = Order.objects.get(id = order_id)
        context = {
            'logged_user': logged_user,
            'cart_item': cart_item,
            'cart': cart,
            'order': order
        }
        return render(request, 'view-order.html', context)
    else:
        return redirect('/')

def cancel_order(request, order_id):
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
        order_to_cancel = Order.objects.get(id = order_id)
        if order_to_cancel:
            stripe.api_key = "sk_test_rcBDHXKJDHEK0uSNnRiLsorp"
            restock_items = OrderProduct.objects.filter(order = order_to_cancel)
            for item in restock_items:
                item.product.inventory += item.quantity
                item.product.save()
            stripe.Refund.create(
                charge = order_to_cancel.stripe_id
            )
            order_to_cancel.status = "Cancelled"
            order_to_cancel.save()
        orders = Order.objects.filter(user = user)
        context = {
            'logged_user': logged_user,
            'cart_item': cart_item,
            'cart': cart,
            'orders': orders
        }
        return render(request, 'user-dashboard.html', context)
    else:
        return redirect('/')
