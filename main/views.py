from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View
from .forms import CheckoutForm, DeliveryForm
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


class OrderSummaryView(LoginRequiredMixin, View):
    template_name = 'order-summary.html'

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(
                request, 'La quantité du produit a été ajouté au panier')
            return redirect("order-summary")
        else:
            messages.info(request, 'Le produit a été ajouté au panier')
            order.products.add(order_product)
            return redirect("order-summary")
    else:
        order = Order.objects.create(user=request.user)
        order.products.add(order_product)
        messages.info(request, 'Le produit a été ajouté au panier')
    return redirect("order-summary")


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            messages.info(request, 'Le produit a été supprimé du panier')
            return redirect("order-summary")
        else:
            messages.info(request, "Le produit n'est pas dans votre panier")
            return redirect('product-detail', slug=slug)
    else:
        messages.info(request, "Vous n'avez pas de commande")
        return redirect('product-detail', slug=slug)
    return redirect('product-detail', slug=slug)


@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, "This product quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This product was not in your cart")
            return redirect("product-detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product-detail", slug=slug)


class CheckoutView(View):

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        if form.is_valid():
            print('Form valid')
            messages.success(self.request, 'Prochaine étape')
            return redirect('delivery')
        messages.warning(self.request, "Failed checkout")
        return redirect("order-summary")


class DeliveryView(View):

    def get(self, *args, **kwargs):
        form = DeliveryForm()
        context = {
            'form': form
        }
        return render(self.request, "delivery.html", context)

    def post(self, *args, **kwargs):
        form = DeliveryForm(self.request.POST or None)
        print(self.request.POST)
        if form.is_valid():
            print('Form valid')
            messages.success(self.request, 'Plus que le paiment')
            return redirect('delivery')
        messages.warning(self.request, "Failed delivery")
        return redirect("checkout")
