from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'


class ProductListView(ListView):
    template_name = 'product-list.html'
    model = Product
    context_object_name = 'products'


class ProductDetailView(DetailView):
    template_name = 'product-detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Product, id=id_)
