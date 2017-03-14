from django.db import models

# Manager for models    =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =
class ProductManager(models.Manager):
    def add_product(self, form):
        print(form)
        if len(form['product_name']) and len(form['product_price']) and len(form['product_inventory']):
            if form['product_category'] == 'default' and len(form['product_new_category']):
                print("here")
                try:
                    category = Category.objects.get(name = form['product_new_category'])
                except:
                    category = Category.objects.create(name = form['product_new_category'])
            else:
                print("not here")
                category = Category.objects.get(name = form['product_category'])
            new_product = Product.objects.create(
                name = form['product_name'],
                description = form['product_description'],
                price = form['product_price'],
                inventory = form['product_inventory'],
                ongoing = True,
                category = category
            )
            return new_product
        return

# Create your models here   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =   =
class Category(models.Model):
    name = models.CharField(max_length=30)

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=9.99)
    inventory = models.PositiveSmallIntegerField(default=0)
    ongoing = models.BooleanField(default=True)
    category = models.ForeignKey('Category', related_name='categoryofproduct')
    objects = ProductManager()

class Image(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='img', default='img/placeholder_image.jpg')
    main = models.BooleanField(default=False)
    product = models.ForeignKey('Product', related_name='imageofproduct')
