# ============  Product App  ===========
## ---------------- URL --------------------
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
from .views import ProductDetailView,ProductListView,VariationListView

urlpatterns = [
    # Examples:
    # url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^(?P<pk>\d+)/$',ProductDetailView.as_view(),name='product_detail'),
    url(r'^(?P<pk>\d+)/inventory/$',VariationListView.as_view(),name='product_inventory'),
    url(r'^$',ProductListView.as_view(),name='products'),
    # url(r'^(?P<id>\d+)','products.views.product_detail_view_func',name='product_detail_function')

]
```

## 2. Dynamic URL
- Using regular expression and python Named Group for the url pattern, we can capture the keyword in the url into a variable, which can be passed to the view function for more dynamic views
    ```
    from django.conf import settings
    from django.conf.urls import include, url
    from django.conf.urls.static import static
    from django.contrib import admin
    from .views import ProductDetailView,ProductListView,VariationListView
    
urlpatterns = [
    url(r'^(?P<pk>\d+)/$',ProductDetailView.as_view(),name='product_detail'),
    url(r'^(?P<pk>\d+)/inventory/$',VariationListView.as_view(),name='product_inventory'),
    url(r'^$',ProductListView.as_view(),name='products'),

]
    ```

## 3. Notes and Tips for URL: 
- in the main url, after slash "/", don't put $, which indicating the end of url
- The url pattern will be searched in the order from the beginning to the end of the list of the urlpatterns. Once found, the research will stop! So in the app url, if you want the url to match exactly the regular expression, put '$' in the end, so that it wouldn't match any other string attached after url. 
- when writing aboslute path, if it begins with slash "/", it will append the address to the main url. If no "/", it will append to the current url

##------------ Detail and List View ----------------


##2. Function based view vs Class-based view(CBV):
- CBV has a lot of default settings built-in (inherited from parents,DetailView, here) as well as error handling. It tends to save you time of writing repetitive codes. 
- However, in CBV, you have to remember a lot of built-in defaults(attributes and methods) such as template_name, get_object(),get_context_data() , in order to use or override them correctly. e.g.
    - content variable for an object in detail view: object (or modelname); in list view is: object_list (or modelname_list)
    - template name and path in detail view is: appname/modelname_detail.html; in list view is: appname/modelname_list.html
    - Note the default argument for object id in CBV is "pk" instead of "id", although you can override it or use slug field. In the functional view, it is much easier to change it. 
    
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
- show related data of product variations on the product detail view. 
    - refer to related variation data in the template: {{ object.variation_set.all }} . 
    - you can iterate it over to make a selection choice on the page. 
    - to make a portal table, just like in filemaker? 
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
## 5. clean up product detail view in the template with html and bootstrap div class

## 6. Create model for productImage uploads
- one-to-many relationship: product as the Foreignkey. 
- unicode return the related product title
- image field only works if python pillow package installed ( you can filefield, but there are some differences)
- define a function,which take an instance and filename, and return a dynamic and customized upload location (slugify version)
- notice the difference of static file storage and static url:
```
{{ img.image.file }}
{{ img.image.url }}
```
## 7. Add Search Query in the product list view (use bootstrap)
- Search query put the following string into the url: url/?queykeyword=value. for example:
```
http://127.0.0.1:8000/products/?q=mp3
```
- To make the search work, override the instance method of ListView: get_queryset(). Use Q function to search multiple fields. Note that different field types(e.g. text and decimal), you will have to do separate Q search and combine them.
```
class ProductListView(ListView):
    model = Product
    # template_name = '<appname>/<modelname>_detail.html'   # this is the default for the template in CBV
    def get_context_data(self, **kwargs):
        context = super(ProductListView,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self,*args,**kwargs):
        qs = super(ProductListView,self).get_queryset(*args,**kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains = query) |
                Q(description__icontains=query)
                  )
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs
```
- create a simple search bar with
    - the form of method=GET. 
    - the url for action will the same url as the current page, {% url "product" %}
    - the name attribute for the input tag will be 'q' 
    ```
    <form class="navbar-form navbar-left" method="GET" role = 'search' action="{% url 'products' %}">
    <div class="form-group">
    <input type="text" class="form-control" placeholder="Search" name="q">
    </div>
    <button type="submit" class="btn btn-default">Submit</button>
    </form>
    ```

## 8. Create list view of related objects
- The goal is to click the product and go to the view of a list of variations of that product. 
- To do that, We can pass keyword args, product primary key(pk), of the product from url to view function to get a queryset of related data(product variations) 
- url:
```
url(r'^(?P<pk>\d+)/inventory',VariationListView.as_view(),name='product_inventory'),
```
- view:
```
class VariationListView(ListView):
    model = Variation
    queryset = Variation.objects.all()
    # template_name = '<appname>/<modelname>_detail.html'   # this is the default for the template in CBV
    def get_queryset(self,*args,**kwargs):
        product_pk = self.kwargs.get('pk')
        if product_pk:
            product = get_object_or_404(Product,pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset
```


##------------------- Add Form to the view for Adding/Editing objects ----------------

- Single ModelFrom: use to add/edit one object on a view (detail view)
- FormSet: when we need add/edit multiple objects on a view( e.g. VariationsListView)
 
## 1. Add FormSet to the VariationListView for editing multiple objects
- Create a model FormSet for Variation model, in form.py. Use extra number for adding new items. If just editing/updating existing items, set it to zero.
```
from django import forms
from django.forms.models import modelformset_factory

from .models import Variation

class VariationInventoryForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = [
            'title'
            'price',
            'sale_price',
            'inventory',
            'active',
        ]

VariationInventoryFormSet = modelformset_factory(Variation,form=VariationInventoryForm,extra=2)
```
- Add the model formset instance (take a queryset as argument) to the context of the VarationListView
 ```
 
 ```
- Render formset in the VariationListView
    - simple render of formset: `{{ formset.as_p }}`
    - understand managementForm: The management form is available as an attribute of the formset itself. When rendering a formset in a template, you can include all the management data by rendering {{ my_formset.management_form }} (substituting the name of your formset as appropriate).
    ```
        <form method="POST" action=""> {% csrf_token %}
        {{ formset.management_form }}
        {% for form in formset %}
            {{form.instance.product.title  }}
            {{ form.instance.title }}
            {{ form.as_p }}
        {% endfor %}

    <input type = 'submit' value ='update' class="btn" />
    </form>
    ```

- define and override instance method, post(), for handling post events after submitting the formset(updating existing items and saving new items).
```
class VariationListView(ListView):
    model = Variation
    queryset = Variation.objects.all()
    # template_name = '<appname>/<modelname>_detail.html'   # this is the default for the template in CBV
    def get_context_data(self, *args,**kwargs):
        context = super(VariationListView,self).get_context_data(*args,*kwargs)
        context['formset'] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def get_queryset(self,*args,**kwargs):
        product_pk = self.kwargs.get('pk')
        if product_pk:
            product = get_object_or_404(Product,pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self,request, *args,**kwargs):
        formset = VariationInventoryFormSet(request.POST,request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                product_pk = self.kwargs.get('pk')
                product = get_object_or_404(Product,pk=product_pk)
                new_item.product = product
                new_item.save()
            messages.success(request, 'your inventory and pricing has been udpated')
        return redirect('products')
```

## ---------------------- Improve the Product View ----------------------------------

## 1. Set priviliages for the view:  Login required Mixin
One of the big advantage of CBV is to use custom mixins. We can seperate common instance methods from different views and wrapped into a class, called mixins, from which CBV can inherit from. For example, using Login required Mixin can allow loggin as staff for adding/editing items, but not available for not loggin or non-staff member.
- Create a mixins.py file and define different mixin classes, from which the CBVs can inherit.
- Login required Mixin
```
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

class StaffRequiredMixin:
    @classmethod
    def as_view(self,*args,**kwargs):
        view = super(StaffRequiredMixin,self).as_view(*args,**kwargs)
        return login_required(view)

    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_staff:
            return super(StaffRequiredMixin,self).dispatch(request,*args,**kwargs)
        else:
            raise Http404


class LoginRequiredMixin:
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(LoginRequiredMixin, self).as_view(*args, **kwargs)
        return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
```

## 2. Django message and Bootstrap alert implementation after updating
- import django contribute app
- Bootstrap alert

## 3. Social Share and font awesome
 - Facebook
```
<a href="https://www.facebook.com/sharer/sharer.php?u={{request.build_absolute_url}}"> 
<i class="fa fa-facebook-square fa-3x></i>
</a>
```
## 4. jQuery Ajax for updating values on the page when selecting product variation 
- To test if jQuery is working. Add the following the end of the body tag in the base.html:
```
<script>
    $(document).ready(function(){
        alert('hello')
    })
</script>
```
- jQuery implementation: Add a jquery block in the base.html in order to make jQuery work in all the html documents.
```
<script>
    $(document).ready(function(){
        {% block jquery %}
        {% endblock %}
    })
</script>

```
- jQuery Script: In the product_detail.html, we want to write the script in the jQuery block. The goal is to select the variations and change the price on page. First, we need to define elements id we need to refer to, the options for varation and price. 
    - $() is the html element selector in jQuery. The format is very like the CSS selector. e.g. $("#div"), $("h3")
    - 

## 4. Related products in the product detail view
- define custom model manager and queryset
```
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    def all(self,*args,**kwargs):
        return self.get_queryset().active()

    def get_related(self,instance):
        products_one = self.get_queryset().filter(categories__in = instance.categories.all())
        products_two = self.get_queryset().filter(default = instance.default)
        qs = (products_one | products_two).exclude(id=instance.id).distinct()
        return qs

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(decimal_places=2,max_digits=20)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category',blank = True)
    default = models.ForeignKey('Category',related_name='default_category',null=True,blank=True)

    objects = ProductManager()
```

- Distinct and Random QuerySets for related products
```
import random
class ProductDetailView(DetailView):
    model = Product
    # template_name = '<appname>/<modelname>_detail.html'   # this is the default for the template in CBV
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        instance = self.get_object()
        context['related'] = sorted(Product.objects.get_related(instance)[:6],key = lambda x: random.random())
        return context
```
## 6. cycle tag in the template with div tag to create thumbnailview(boxview)
cycle tag: Produces one of its arguments each time this tag is encountered. The first argument is produced on the first encounter, the second argument on the second encounter, and so forth. Once all arguments are exhausted, the tag cycles to the first argument and produces it again.
```
{% block content %}
 <div class="row">
{%  for product in object_list %}
    <div class="col-xs-4">
    <div class="thumnail text-center">
    <h4><a href=" {{ product.get_absolute_url }}">{{ product.title }}</a></h4>
        {% if product.get_image_url %}
        <a href ='{{ product.get_absolute_url }}'><img id="img" class="img-responsive" src="{{ product.get_image_url }}"/></a><br/>
        {% endif %}
    </div>
    </div>
    {% cycle '' '' '</div><div class="row"">' %}
{% endfor %}
</div>
{% endblock content %}
```
## 7. Template tag Include with Variable
 
 

## --------------------- Product Category Model and View ---------------------

## 1. Relationship between Product and Category Model
- Create category model: the name and the description of any categories 
- Add two fields in the product model:
    - categories: many-to-many with product
    - default: one-to-many with product
- Add and manage categories in the admin
- Show the default category in the product detail view

## 2. Category List and Detail Views
- Create a separate url file, urls_categories.py, in the product folder. 
- 
 
## ----------- Feature Product Model and View ----------------


# =================== Carts App (Order App)===================
## 1. Many-to-Many relationship through intermediate model:
```
Product Variations -------------<- CartItem ->----------- Cart(Order)
```
## 2. Add,Remove,Update Cart data on CarView
- Create Cart CBV from base view by overriding get()method
    - modifying GET request by modifying url
    - GET request through 'Add to Cart' html form in product detail view
- Add SingleObjectMxin and override get_object() method
- Django sessions: Django sessions allow to store and retrieve data per site visitor basis, even when users are not logged in
- Format Cart and Remove items
- Update Cartitems quantity in cart

## 3. LineItem total 
- update lineitem total in CartItem using model pre-save signal, refreshing the page
- update subtotal in Cart using model pre-save signal, refreshing the page

## 4. Ajax   ( Compared to FileMaker Script Trigger)
- Ajax: Asynchronous Javascript And Xml. We can do data passing without refeshing the page. 
```
selector.function(function handler)
```
    - selector: 
    - event: change(), click()
    - event handler: function(){ }
- Ajax for updating linetiem total and cart subtotal 
- jQuery Flash Message
- Post delete signal for empty Cart
- Ajax for updating Cart Count
