from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.utils import timezone

from .models import Product
# Create your views here.

class ProductDetailView(DetailView):
    model = Product
    # template_name = '<appname>/<modelname>_detail.html'   # this is the default for the template in CBV


class ProductListView(ListView):
    model = Product
    # template_name = '<appname>/<modelname>_detail.html'   # this is the default for the template in CBV
    def get_context_data(self, **kwargs):
        context = super(ProductListView,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context



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