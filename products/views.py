from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'products/product_list.html'
    context_object_name = 'product_list'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
