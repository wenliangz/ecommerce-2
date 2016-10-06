from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.text import slugify


# Create your models here.

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    def all(self,*args,**kwargs):
        return self.get_queryset().active()


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(decimal_places=2,max_digits=20)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category',blank = True)
    default = models.ForeignKey('Category',related_name='default_category',null=True,blank=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'pk':self.pk})

class Variation(models.Model):
    product =  models.ForeignKey(Product)
    title = models.CharField(max_length = 120)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20,null= True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null = True, blank=True) # negative refer to unlimited amount

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()  # return url of the related product by foreign key

def product_save_receiver(sender, instance, created, *args,**kwargs):
    print(sender)
    print(instance)
    print(created)
    product = instance
    variations = product.variation_set.all()
    if variations.count() ==0:
        new_var = Variation()
        new_var.product =product
        new_var.title = 'Default'
        new_var.price = product.price
        new_var.save()

post_save.connect(product_save_receiver,sender=Product)


post_save.connect(product_save_receiver,sender = Product)

def image_upload_to(instance, filename):
    title = instance.product.title
    slug =slugify(title)
    file_extension = filename.split('.')[1]
    new_filename =  '%s.%s'%(instance.id,file_extension)
    return 'products/%s/%s'%(slug,new_filename)

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return self.product.title  # return the related product title by foreign key

class Category(models.Model):
    title = models.CharField(max_length=120,unique =True)
    slug = models.SlugField(unique = True)
    description = models.TextField(null=True,blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now = False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail',kwargs = {'slug':self.slug})

