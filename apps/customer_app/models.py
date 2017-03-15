from django.db import models
from ..admin_app.models import Category, Product, Image
from ..login_registration_app.models import User

# Create your models here.
class Cart(models.Model):
    quantity = models.PositiveSmallIntegerField(default=1)
    user = models.ForeignKey('login_registration_app.User', related_name='cartofuser')
    product = models.ForeignKey('admin_app.Product', related_name='productofcart')

class Order(models.Model):
    user = models.ForeignKey('login_registration_app.User', related_name='useroforder')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=30, default='Order in Process')
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    billing = models.ForeignKey('BillingAddress', related_name='billto')
    shipping = models.ForeignKey('ShippingAddress', related_name='shipto')

class OrderProduct(models.Model):
    order = models.ForeignKey('Order', related_name='orderofproduct')
    product = models.ForeignKey('admin_app.Product', related_name='productoforder')

class BillingAddress(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.PositiveSmallIntegerField()

class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.PositiveSmallIntegerField()
