from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, OrderProduct, Order
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
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Product, slug=slug_)


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product = OrderProduct.objects.create(product=product)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
        else:
            order.products.add(order_product)
    else:
        order = Order.objects.create(user=request.user)
        order.products.add(order_product)
    return redirect("product-detail", slug=slug)
