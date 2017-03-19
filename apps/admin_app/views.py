from django.shortcuts import render, redirect, reverse
from .models import Category, Product, Image
from ..customer_app.models import Cart, Order, OrderProduct, BillingAddress, ShippingAddress
from ..login_registration_app.models import User
import os

# App root
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
def admin(request):
    if 'logged_user' not in request.session:
        return redirect('/login_registration')
    else:
        if request.session['logged_user'] == 1:
            return render(request, 'admin-dashboard.html')
        else:
            return redirect('/')
def signout(request):
    request.session.pop('logged_user', None)
    return redirect('/')

def products(request):
    if 'logged_user' not in request.session:
        return redirect('/login_registration')
    else:
        if request.session['logged_user'] == 1:
            categories = Category.objects.all()
            products = Product.objects.all().order_by('category')
            images = Image.objects.all()
            context = {
                'categories': categories,
                'products': products,
                'images': images
            }
            # print(context)
            return render(request, 'products.html', context)
        else:
            return redirect('/')

def orders(request):
    if 'logged_user' not in request.session:
        return redirect('/login_registration')
    else:
        if request.session['logged_user'] == 1:
            orders = Order.objects.all()
            context = {
                'orders': orders
            }
            return render(request, 'orders.html', context)
        else:
            return redirect('/')

def order_status_update(request):
    if 'logged_user' not in request.session:
        return redirect('/login_registration')
    else:
        if request.session['logged_user'] == 1:
            order = Order.objects.get(id = request.GET['order_id'])
            order.status = request.GET['status']
            order.save()
            orders = Order.objects.all()
            context = {
                'orders': orders
            }
            return render(request, 'orders.html', context)
        else:
            return redirect('/')

def add_product(request):
    print("Image File HERE:", request.FILES)
    form = request.POST
    product = Product.objects.add_product(form)
    print("ROOT IS HERE", APP_ROOT)
    target = os.path.join(APP_ROOT, 'media/img')
    # default_image = os.path.join(APP_ROOT, 'static/img/placeholder_image.jpg')
    if not os.path.isdir(target):
        os.mkdir(target)
    print("Is there product?:", product)
    if product:
        print("in product image")
        if request.FILES.getlist("image_file_main"):
            for main_img in request.FILES.getlist("image_file_main"):
                Image.objects.create(
                    name = main_img.name,
                    image = main_img,
                    product = product,
                    main = True
                )
        else:
            Image.objects.create(
                name = "default_image",
                product = product,
                main = True
            )
        for extra_img in request.FILES.getlist("image_file"):
            Image.objects.create(
                name = extra_img.name,
                image = extra_img,
                product = product
            )
    return redirect(reverse('products'))

def stop_sale_product(request, product_id):
    product = Product.objects.get(id = product_id)
    product.ongoing = False
    product.save()
    return redirect(reverse('products'))

def restart_sale_product(request, product_id):
    product = Product.objects.get(id = product_id)
    product.ongoing = True
    product.save()
    return redirect(reverse('products'))

def edit_product(request, product_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    else:
        if request.session['logged_user'] == 1:
            product = Product.objects.get(id = product_id)
            categories = Category.objects.all()
            context = {
                'categories': categories,
                'product': product
            }
            return render(request, 'edit-product.html', context)
        else:
            return redirect('/')

def submit_edited_product(request, product_id):
    print("New Main Image File HERE:", request.FILES)
    form = request.POST
    product = Product.objects.get(id = product_id)
    if len(form['product_name']):
        product.name = form['product_name']
    if len(form['product_description']):
        product.description = form['product_description']
    if form['product_category'] == 'default' and len(form['product_new_category']):
        print("here")
        try:
            category = Category.objects.get(name = form['product_new_category'])
        except:
            category = Category.objects.create(name = form['product_new_category'])
        product.category = category
    elif form['product_category'] != 'default':
        category = Category.objects.get(name = form['product_category'])
        product.category = category
    else:
        pass
    if len(form['product_price']):
        product.price = form['product_price']
    if len(form['product_inventory']):
        product.inventory = form['product_inventory']
    product.save()
    if request.FILES.getlist("image_file_main"):
        image = Image.objects.filter(product = product).filter(main = True)
        image.delete()
        for main_img in request.FILES.getlist("image_file_main"):
            Image.objects.create(
                name = main_img.name,
                image = main_img,
                product = product,
                main = True
            )
    for extra_img in request.FILES.getlist("image_file"):
        Image.objects.create(
            name = extra_img.name,
            image = extra_img,
            product = product
        )
    return redirect(reverse('products'))

def clear_db(request):
    Product.objects.all().delete()
    Category.objects.all().delete()
    Image.objects.all().delete()
    return redirect(reverse('products'))
