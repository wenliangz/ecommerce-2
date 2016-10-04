
## 1. URL best practice: keep app-related URLs inside the app.
- use include in main url.py and create a app-specific url.py in the app. e.g.

The main url.py
```
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # Examples:
    url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),
    url(r'^about/$', 'ecommerce2.views.about', name='about'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^products/', include('products.urls')),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
    
The products url.py:
```
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from .views import ProductDetailView,ProductListView

urlpatterns = [
    # Examples:
    # url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^(?P<pk>\d+)',ProductDetailView.as_view(),name='product_detail'),
    url(r'^$',ProductListView.as_view(),name='products'),
    # url(r'^(?P<id>\d+)','products.views.product_detail_view_func',name='product_detail_function')

]
```

# ======= Detail and List View  ==============


##2. Function based view vs Class-based view(CBV):
- CBV has a lot of default settings built-in (inherited from parents,DetailView, here) as well as error handling. It tends to save you time of writing repetitive codes. 
- However, in CBV, you have to remember a lot of built-in defaults(attributes and methods) such as template_name, get_object(),get_context_data() , in order to use or override them correctly. e.g.
    - content variable for an object in detail view: object (or modelname); in list view is: object_list (or modelname_list)
    - template name and path in detail view is: appname/modelname_detail.html; in list view is: appname/modelname_list.html
    
```
from django.views.generic.detail import DetailView
from django.shortcuts import render,get_object_or_404
from django.http import Http404

from .models import Product
# Create your views here.

class ProductDetailView(DetailView):
    model = Product
    # template_name = '<appname>/<modelname>_detail.html'   # this is the default for the template in CBV


def product_detail_view_func(request,id):
    # product_instance = Product.objects.get(id=id)
    # below is a better way to get the instance and do the exception handling
    product_instance = get_object_or_404(Product,id=id)
    try:
        prodict_instance = Product.object.get(id=id)
    except Product.DoesNotExist:
        raise Http404
    except:
        raise Http404
    
    template = "products/product_detail.html"
    context ={
        'object':product_instance
    }
    return render(request, template, context)
```
- URL setting
    - Note the default argument for object id in CBV is pk instead of id.  
```
urlpatterns = [
    # Examples:
    # url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^cbv/(?P<pk>\d+)',ProductDetailView.as_view(),name='product_detail'),
    url(r'^(?P<id>\d+)','products.views.product_detail_view_func',name='product_detail_function')

]
```
- Tips for url: 
    - in the main url, after slash "/", don't put $, which indicating the end of url
    - when writing aboslute path, if it begins with slash "/", it will append the address to the main url. If no "/", it will append to the current url

##3. Override method in Class-based view(CBV):
- In the function-based view, everything is very obvious as we provide everything to the function ourselves, such as template name, context. In the classed-base view, they are inherited from parents. When you need to customize, you need to override the method or attributes. For example, context data in CBV is return by the method called, get_context_data(self). To customize the context data, we just need to write our own method get_context_data(self) to override. Normally, we want to add our own data to the existing parent data, so we usually do a supercall of the parent class to get the context and append our own data before return it. e.g.

```
class ProductDetailView(DetailView):
    model = Product
    # template_name = '<appname>/<modelname>_detail.html'   # this is the default for the template in CBV


class ProductListView(ListView):
    model = Product
    # template_name = '<appname>/<modelname>_detail.html'   # this is the default for the template in CBV
    def get_context_data(self, **kwargs):  # to override the parent method
        context = super(ProductListView,self).get_context_data(**kwargs)  # supercall to get the context from parent
        context['now'] = timezone.now() # add our customize data to the context
        return context
```

- Default context variables available for template to use all the times. These variables are coming from the context_processors. Such as 
  {{user}}
  
  
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            # this context_processors will provide default context variables for template to use for rendering
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

- Tips for varible use in the template:
    - the variable within the template tag, no need for {{ }}
    - the method call in the template tag, no need (). Just use the dot notation like the attribute
    
 
##3. Getting link for each of model instance:
- hard-coded with object.id: 
```
<a href = '/products/{{object.id}}'> {{object.title}}</a>
```
- a better way is to use url template tag and url name with object.id passed
```
<a href = '{% url "product_detail" pk=object.pk}'> {{object.title}}</a>
```
- the best and more dynamic way is to define a model instance method, get_absolute_url method, in the model. and get the url for each instance by using reverse method.
in the model:
```
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(decimal_places=2,max_digits=20)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'pk':self.pk})
```
in the template:
```
<a href = '{{object.get_absolute_url}}'> {{object.title}}</a>  # note no () is needed to call method here
 ```

##3. Model managers for getting customized queryset
- user case: if the product status is not active, we should not show them on the product list.
- to do this: create a custom model manager and queryset in the model:

```
from django.db import models
from django.core.urlresolvers import reverse

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

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'pk':self.pk})  

```
##3. Use a separate model for Product variations with one-to-many relationship
- add product variations in admin view (TODO: build userview to add variation based on primary key for product (choice dropdown menu in the form))
- refer to related variation data in the template: {{ object.variation_set.all }} . 
    - you can iterate it over.
    - you can make a selection choice on the page
    ```
    <select class="'form-control">
    {% for vari_obj in object.variation_set.all %}
    <option value = '{{ vari_obj }}'>{{ vari_obj }}</option>
    {% endfor %}
    </select>
    ```
## 4. Use post Save signal for creating default variations for each product
this allow us to make things happen outside of context of views or admin. when the model save, it will send signal for us to do various things.
- three signals that will be sent out when yous save a record in a model: sender, instance, created
- we create a function that take the three signals as arguments and do what we want to do post save
- use the post_save.connect(product_post_save_receiver,sender=Product) to connect the function and the model
```
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
```
## 5. clean up product detail template with html and bootstrap div class

## 6. Create model for productImage uploads
- one-to-many relationship: product as the Foreignkey. 
- unicode return the related product title
- image field only works if python pillow package installed ( you can filefield, but there are some differences)
- define a function,which take an instance and filename, and return a dynamic and customized upload location (slugify version)





# =======   ==============