from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Product, OrderProduct, Order, Payment, Coupon, Refund
# Create your views here.
import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


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
            return redirect("products")
        else:
            messages.info(request, 'Le produit a été ajouté au panier')
            order.products.add(order_product)
            return redirect("products")
    else:
        order = Order.objects.create(user=request.user)
        order.products.add(order_product)
        messages.info(request, 'Le produit a été ajouté au panier')
    return redirect("products")


@login_required
def add_single_item_to_cart(request, slug):
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
            return redirect("products")
        else:
            messages.info(request, "Le produit n'est pas dans votre panier")
            return redirect('products')
    else:
        messages.info(request, "Vous n'avez pas de commande")
        return redirect('products')
    return redirect('products')


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
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
                'couponform': CouponForm(),
                'DISPLAY_COUPON_FORM': True
            }
        except ObjectDoesNotExist:
            return redirect('checkout')

        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        if form.is_valid():
            print('Form valid')
            messages.success(self.request, 'Prochaine étape')
            return redirect('payment')
        messages.warning(self.request, "Failed checkout")
        return redirect("order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.information:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, 'payment.html', context)
        else:
            messages.warning(
                self.request, "Vous devez remplir le formulaire avant d'accèder au paiement ")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total())

        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                currency='eur',
                source='tok_visa',  # replace by token in prod
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = amount
            payment.save()

            order_items = order.products.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            messages.success(self.request, "Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.warning(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "Ce code promo n'existe pas")
        return redirect('checkout')


class AddCouponView(View):

    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user,
                    ordered=False
                )
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, 'Le code coupon est accepté')
                return redirect('checkout')
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect('checkout')


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, 'Your request was received')
                return redirect('request-refund')

            except ObjectDoesNotExist:
                messages.info(self.request, 'This order does not exist.')
                return redirect('request-refund')
