from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .forms import CheckoutForm, CheckoutAperoForm, CouponForm, RefundForm, PaymentForm, AvisForm, ContactForm, ProductForm, DeliveredForm
from .models import Product, OrderProduct, Order, Payment, Coupon, Refund, Info, Avis
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags



# Create your views here.
import random
import string
import stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid





class HomePageView(TemplateView):
    template_name = 'home.html'


class ProductListView(ListView):
    template_name = 'product-dejeuner.html'
    model = Product
    context_object_name = 'products'

    def get(self, *args, **kwargs):
        products = Product.objects.filter(menu='Dejeuner', visible=True)
        accessoire_product = Product.objects.filter(menu='Dejeuner',category='Accessoires')
        form = ProductForm(auto_id=False)
        user = self.request.user
        if user.is_authenticated:
            order, created = Order.objects.get_or_create(
                user=self.request.user, ordered=False, type_of_order='Dejeuner')

            context = {
                'order': order,
                'products': products,
                'accessoires': accessoire_product,
                'form': form,
                # 'couponform': CouponForm(),
                # 'DISPLAY_COUPON_FORM': True,
            }
            return render(self.request, 'product-dejeuner.html', context)
        else:
            context = {
                'products': products,
                
            }
            return render(self.request, 'product-dejeuner.html', context)


class ProductAperoView(ListView):
    template_name = 'product-apero.html'
    model = Product
    context_object_name = 'products'

    def get(self, *args, **kwargs):
        products = Product.objects.filter(menu='Apero', visible=True)
        form = ProductForm(auto_id=False)
        user = self.request.user
        if user.is_authenticated:
            order, created = Order.objects.get_or_create(
                user=self.request.user, ordered=False, type_of_order='Apero')
            
            context = {
                'order': order,
                'products': products,
                'form': form,
                # # 'couponform': CouponForm(),
                # 'DISPLAY_COUPON_FORM': False,
            }
            return render(self.request, 'product-apero.html', context)
        else:
            context = {
                'products': products
            }
            return render(self.request, 'product-apero.html', context)


# class ProductDetailView(DetailView):
#     template_name = 'product-detail.html'

#     def get_object(self):
#         slug_ = self.kwargs.get("slug")
#         return get_object_or_404(Product, slug=slug_)


class OrderSummaryDejeunerView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order_dejeuner_qs = Order.objects.get(user=self.request.user, ordered=False,type_of_order='Dejeuner')
            
            form = ProductForm()
            context = {
                'order_dejeuner': order_dejeuner_qs,
                
                'form': form,
                # 'couponform': CouponForm(),
                # 'DISPLAY_COUPON_FORM': True,
            }
            return render(self.request, 'order-summary-dejeuner.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Vous n'avez rien dans votre panier")
            return redirect("/")

class OrderSummaryAperoView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order_apero_qs = Order.objects.get(user=self.request.user, ordered=False, type_of_order='Apero')
            context = {
                'order_apero': order_apero_qs,
                # 'couponform': CouponForm(),
                # 'DISPLAY_COUPON_FORM': True,
            }
            return render(self.request, 'order-summary-apero.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Vous n'avez rien dans votre panier")
            return redirect("/")

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_dejeuner_qs = Order.objects.filter(user=request.user, ordered=False, type_of_order ='Dejeuner')
    order_apero_qs = Order.objects.filter(user=request.user, ordered=False, type_of_order ='Apero')
    form = ProductForm(request.POST)
    response_data={}
    response ={}

    if form.is_valid() and request.method == 'POST':
        quantity = int(form.cleaned_data.get('quantity'))
        dessert = form.cleaned_data.get('dessert')
        boisson = form.cleaned_data.get('boisson')
        sandwich = form.cleaned_data.get('sandwich')
        alcool = form.cleaned_data.get('alcool')
        huitre = form.cleaned_data.get('huitre')
        order_product, created = OrderProduct.objects.get_or_create(
            product=product,
            user=request.user,
            ordered=False,
            dessert= dessert,
            boisson=boisson,
            sandwich=sandwich,
            alcool=alcool,
            huitre=huitre

        )

       
        if product.menu == 'Dejeuner':
            if order_dejeuner_qs.exists():
                order = order_dejeuner_qs[0]
                if order.products.filter(product__slug=product.slug, dessert= dessert,boisson=boisson, sandwich=sandwich).exists():
                    
                    order_product.quantity += quantity
                    order_product.save()
                    response_data = {
                        'quantity': order_product.quantity,
                        'total': order.get_total(),
                        'name': product.name,
                        'dessert':order_product.dessert,
                        'boisson':order_product.boisson,
                        'sandwich':order_product.sandwich,
                        'product_total': order_product.get_total_product_price(),
                        'cart_quantity': order.get_quantity(),
                        'product_name': order_product.product.name,
                        'order_product_id': order_product.id
                    }
                    return JsonResponse(response_data)
                else:    
                    print("ok")
                    order_product.quantity = quantity
                    order_product.dessert = dessert
                    order_product.boisson = boisson
                    order_product.sandwich = sandwich
                    order_product.save()
                    order.products.add(order_product)
                    response_data = {
                        'quantity': order_product.quantity,
                        'total': order.get_total(),
                        'name': product.name,
                        'dessert':order_product.dessert,
                        'boisson':order_product.boisson,
                        'sandwich':order_product.sandwich,
                        'product_total': order_product.get_total_product_price(),
                        'cart_quantity': order.get_quantity(),
                        'product_name': order_product.product.name,
                        'order_product_id': order_product.id
                    }
                   
                    
                    return JsonResponse(response_data)
            else:
                order = Order.objects.create(
                    user=request.user, type_of_order='Dejeuner')
                order_product.quantity = quantity
                order_product.dessert = dessert
                order_product.boisson = boisson
                order_product.sandwich = sandwich
                order_product.save()
                order.products.add(order_product)
                response_data = {
                        'quantity': order_product.quantity,
                        'total': order.get_total(),
                        'name': product.name,
                        'dessert':order_product.dessert,
                        'boisson':order_product.boisson,
                        'sandwich':order_product.sandwich,
                        'product_total': order_product.get_total_product_price(),
                        'cart_quantity': order.get_quantity(),
                        'product_name': order_product.product.name,
                        'order_product_id': order_product.id
                    }
            return JsonResponse(response_data)
        elif product.menu == 'Apero':
            if order_apero_qs.exists():
                order = order_apero_qs[0]
                if order.products.filter(product__slug=product.slug, alcool=alcool, huitre=huitre).exists():
                    order_product.quantity += quantity
                    order_product.save()
                    response = {
                        'quantity': order_product.quantity,
                        'total': order.get_total(),
                        'name': product.name,
                        'product_total': order_product.get_total_product_with_variant_price(),
                        'cart_quantity': order.get_quantity(),
                        'product_name': order_product.product.name,
                        'alcool': order_product.alcool,
                        'huitre': order_product.huitre,
                        'order_product_id': order_product.id
                    }
                    return JsonResponse(response)
                else:
                    order_product.quantity = quantity
                    order_product.alcool =alcool
                    order_product.huitre =huitre
                    order_product.save()
                    order.products.add(order_product)
                    response = {
                        'quantity': order_product.quantity,
                        'total': order.get_total(),
                        'name': product.name,
                        'product_total': order_product.get_total_product_with_variant_price(),
                        'cart_quantity': order.get_quantity(),
                        'product_name': order_product.product.name,
                        'alcool': order_product.alcool,
                        'huitre': order_product.huitre,
                        'order_product_id': order_product.id
                    }
                    return JsonResponse(response)
            else:
                order = Order.objects.create(
                    user=request.user, type_of_order='Apero')
                order_product.quantity = quantity
                order_product.alcool = alcool
                order_product.huitre=huitre
                order_product.save()
                order.products.add(order_product)
                response = {
                        'quantity': order_product.quantity,
                        'total': order.get_total(),
                        'name': product.name,
                        'product_total': order_product.get_total_product_with_variant_price(),
                        'cart_quantity': order.get_quantity(),
                        'product_name': order_product.product.name,
                        'alcool': order_product.alcool,
                        'huitre': order_product.huitre,
                        'order_product_id': order_product.id
                    }
                return JsonResponse(response)
        else: 
            messages.warning(request, 'Un problème vient de survenir')
    return redirect("home")

@login_required
def add_single_item_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_dejeuner_qs = Order.objects.filter(user=request.user, ordered=False, type_of_order ='Dejeuner')
    order_apero_qs = Order.objects.filter(user=request.user, ordered=False, type_of_order ='Apero')
    response_data = {}
    response= {}
    if product.menu == 'Dejeuner':
        order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
        sandwich=request.POST['sandwich'],
        boisson=request.POST['boisson'],
        dessert=request.POST['dessert'],
    )
        if order_dejeuner_qs.exists():
            order = order_dejeuner_qs[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product.quantity += 1
                order_product.save()
                response_data = {
                    'quantity': order_product.quantity,
                    'total': order_product.get_total_product_with_variant_price(),
                    'get_total': order.get_total(),
                }
                # messages.info(
                #     request, 'La quantité du produit a été ajouté au panier')
                # return redirect("order-summary-dejeuner")
                return JsonResponse(response_data)
            else:
                messages.info(request, 'Le produit a été ajouté au panier')
                order.products.add(order_product)
                return redirect("order-summary-dejeuner")
        else:
            order = Order.objects.create(user=request.user)
            order.products.add(order_product)
            messages.info(request, 'Le produit a été ajouté au panier')
    elif product.menu == 'Apero':
        order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
        alcool=request.POST['alcool'],
        huitre= request.POST['huitre'],
    )
        if order_apero_qs.exists():
            order = order_apero_qs[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product.quantity += 1
                order_product.save()
                response = {
                    'quantity': order_product.quantity,
                    'total': order_product.get_total_product_with_variant_price(),
                    'get_total': order.get_total(),
                }
                return JsonResponse(response)
            else:
                messages.info(request, 'Le produit a été ajouté au panier')
                order.products.add(order_product)
                return redirect("order-summary-apero")
        else:
            order = Order.objects.create(user=request.user)
            order.products.add(order_product)
            messages.info(request, 'Le produit a été ajouté au panier')
    else: 
        messages.warning(request, 'un problème vient de survenir')
    return redirect("home")



@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_dejeuner_qs = Order.objects.filter(user=request.user, ordered=False, type_of_order ='Dejeuner')
    order_apero_qs = Order.objects.filter(user=request.user, ordered=False, type_of_order ='Apero')
    if product.menu == 'Dejeuner':
        if order_dejeuner_qs.exists():
            order = order_dejeuner_qs[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product = OrderProduct.objects.filter(
                    product=product,
                    user=request.user,
                    ordered=False,
                    
                )[0]
                order.products.remove(order_product)
                order_product.delete()
                response_data = {
                    'sandwich': order_product.sandwich,
                    'dessert': order_product.dessert,
                    'boisson': order_product.boisson,
                    'order_id': order_product.id,
                    'quantity': order_product.quantity,
                    'total': order_product.get_total_product_with_variant_price(),
                    'get_total': order.get_total(),
                }
                return JsonResponse(response_data)
                # messages.info(request, 'Le produit a été supprimé du panier')
                # return redirect("order-summary-dejeuner")
            else:
                messages.info(request, "Le produit n'est pas dans votre panier-dejeuner")
                return redirect('order-summary-dejeuner')
        else:
            messages.info(request, "Vous n'avez pas de commande")
            return redirect('products')
    elif product.menu == 'Apero':
        if order_apero_qs.exists():
            order = order_apero_qs[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product = OrderProduct.objects.filter(
                    product=product,
                    user=request.user,
                    ordered=False
                )[0]
                order.products.remove(order_product)
                order_product.delete()
                response = {
                    'quantity': order_product.quantity,
                    'total': order_product.get_total_product_with_variant_price(),
                    'get_total': order.get_total(),
                }
                return JsonResponse(response)
            else:
                messages.info(request, "le produit n'est pas dans votre panier")
                return redirect('order-summary-apero')
        else:
            messages.warning(request, 'Votre panier est vide')
    return redirect('home')

@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_dejeuner_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        type_of_order='Dejeuner'
    )
    order_apero_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        type_of_order='Apero'
    )
    if product.menu == 'Dejeuner':
        if order_dejeuner_qs.exists():
            order = order_dejeuner_qs[0]
            # check if the order item is in the order
            if order.products.filter(product__slug=product.slug).exists():
                # order_product = OrderProduct.objects.filter(
                #     product=product,
                #     user=request.user,
                #     ordered=False
                # )[0]
                order_product, created = OrderProduct.objects.get_or_create(
                product=product,
                user=request.user,
                ordered=False,
                sandwich=request.POST['sandwich'],
                boisson=request.POST['boisson'],
                dessert=request.POST['dessert'],
                )
                
                if order_product.quantity > 1:
                    order_product.quantity -= 1
                    order_product.save()
                    response_data = {
                    'quantity': order_product.quantity,
                    'total': order_product.get_total_product_with_variant_price(),
                    'get_total': order.get_total(),
                    }
                    return JsonResponse(response_data)
                else:
                    order.products.remove(order_product)
                    response_data = {
                        'quantity': order_product.quantity,
                        'total': order_product.get_total_product_with_variant_price(),
                        'get_total': order.get_total(),
                    }
                    return JsonResponse(response_data)
                # messages.info(request, "This product quantity was updated.")
                # return redirect("order-summary-dejeuner")
            else:
                messages.info(request, "This product was not in your cart")
                return redirect("products")
        else:
            messages.info(request, "You do not have an active order")
            return redirect("home")
    elif product.menu == 'Apero':
        order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
        alcool=request.POST['alcool'],
        huitre= request.POST['huitre'],
        )
        if order_apero_qs.exists():
            order = order_apero_qs[0]
            # check if the order item is in the order
            if order.products.filter(product__slug=product.slug).exists():
                # order_product = OrderProduct.objects.filter(
                #     product=product,
                #     user=request.user,
                #     ordered=False
                # )[0]
                if order_product.quantity > 1:
                    order_product.quantity -= 1
                    order_product.save()
                    response = {
                    'quantity': order_product.quantity,
                    'total': order_product.get_total_product_with_variant_price(),
                    'get_total': order.get_total(),
                    }
                    return JsonResponse(response)
                else:
                    order.products.remove(order_product)
                    response = {
                    'quantity': order_product.quantity,
                    'total': order_product.get_total_product_with_variant_price(),
                    'get_total': order.get_total(),
                    }
                    return JsonResponse(response)
            else:
                messages.info(request, "This product was not in your cart")
                return redirect("products-apero")
        else:
            messages.info(request, "You do not have an active order")
            return redirect("home")
    else: 
        messages.warning(request, 'un problème vient de survenir')
    return redirect('home')






class CheckoutView(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False, type_of_order='Dejeuner')
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
                # 'couponform': CouponForm(),
                # 'DISPLAY_COUPON_FORM': True
            }
            address_qs = Info.objects.filter(
                user=self.request.user,
                default=True
            )
            if address_qs.exists():
                context.update(
                    {'default_address': address_qs.latest('id')})

        except ObjectDoesNotExist:
            messages.info(self.request, "Vous n'avez pas encore de produits dans votre panier")
            return redirect('checkout')

        return render(self.request, "checkout.html", context)

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        args = {}
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False, type_of_order='Dejeuner')
            if form.is_valid():
                default_address = form.cleaned_data.get('default_address')
                date_de_livraison = form.cleaned_data.get('date_de_livraison')
                delivery_option = form.cleaned_data.get('delivery_option')
                couvert = form.cleaned_data.get('couvert')
                loueur_bateau = form.cleaned_data.get('loueur_bateau')

                if default_address:
                    address_qs = Info.objects.filter(
                        user=self.request.user,
                        default=True,
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.information = shipping_address
                        order.delivery_option = delivery_option
                        order.date_de_livraison = datetime.datetime.strptime(date_de_livraison, '%d/%m/%Y %H:%M' )
                        order.couvert = couvert
                        order.loueur_bateau = loueur_bateau
                        order.save()
                        messages.info(
                            self.request, 'Il ne vous reste plus que le paiement - default')
                        return redirect('payment-dejeuner')
                    else:
                        messages.info(
                            self.request, "Pas de profil enregistré")
                        return redirect('checkout')
                else:
                    name = form.cleaned_data.get('name')
                    prenom = form.cleaned_data.get('prenom')
                    phone = form.cleaned_data.get('phone')
                    email = form.cleaned_data.get('email')
                    date_de_livraison = form.cleaned_data.get('date_de_livraison')
                    delivery_option = form.cleaned_data.get(
                        'delivery_option')

                    zone_delivery = form.cleaned_data.get('zone_delivery')
                    rang_delivery = form.cleaned_data.get('rang_delivery')
                    numero_delivery = form.cleaned_data.get('numero_delivery')
                    creneau_delivery = form.cleaned_data.get('creneau_delivery')
                    couvert = form.cleaned_data.get('couvert')
                    loueur_bateau = form.cleaned_data.get('loueur_bateau')
                    

                    if is_valid_form([name, prenom, phone, email]):
                        adresse_info = Info(
                            user=self.request.user,
                            name=name,
                            prenom=prenom,
                            phone=phone,
                            email=email,
                            zone_delivery=zone_delivery,
                            rang_delivery=rang_delivery,
                            numero_delivery=numero_delivery,
                            

                        )
                        adresse_info.save()

                        order.information = adresse_info
                        order.couvert= couvert
                        order.delivery_option = delivery_option
                        order.creneau_delivery= creneau_delivery
                        order.loueur_bateau = loueur_bateau

                        if order.delivery_option == 'livraison-sur-bateau':
                            order.date_de_livraison = datetime.datetime.strptime(date_de_livraison, '%d/%m/%Y' )
                        else:
                            order.date_de_livraison = datetime.datetime.strptime(date_de_livraison, '%d/%m/%Y %H:%M' )
                            
                        order.save()

                        save_address = form.cleaned_data.get(
                            'save_address')
                        if save_address:
                            adresse_info.default = True
                            adresse_info.save()

                        messages.info(
                            self.request, 'Il ne vous reste plus que le paiement')
                        return redirect('payment-dejeuner')
                    else:
                        messages.info(
                            self.request, "Vos informations personnelles ne sont pas complètes")
                        return redirect("checkout")
            else:
                args['form'] = form
                args['order'] = order
                print(form)
                messages.info(self.request, 'Une erreur est présente dans votre formulaire')
                return render(self.request, 'checkout.html', args)
        except ObjectDoesNotExist:
            messages.info(self.request, 'This order does not exist.')
            return redirect('order-summary-dejeuner')


class CheckoutViewApero(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False, type_of_order='Apero')
            form = CheckoutAperoForm()
            context = {
                'form': form,
                'order': order,
                # 'couponform': CouponForm(),
                # 'DISPLAY_COUPON_FORM': True
            }
            address_qs = Info.objects.filter(
                user=self.request.user,
                default=True
            )
            if address_qs.exists():
                context.update(
                    {'default_address': address_qs.latest('id')})

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect('checkout-apero')

        return render(self.request, "checkout-apero.html", context)
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        form = CheckoutAperoForm(self.request.POST or None)
        args= {}
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False, type_of_order='Apero')
            if form.is_valid():
                default_address = form.cleaned_data.get('default_address')
                date_de_livraison = form.cleaned_data.get('date_de_livraison')
                couvert = form.cleaned_data.get('couvert')
                

                if default_address:
                    address_qs = Info.objects.filter(
                        user=self.request.user,
                        default=True,
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.information = shipping_address
                        order.date_de_livraison = datetime.datetime.strptime(date_de_livraison, '%d/%m/%Y %H:%M' )
                        order.couvert = couvert
                        order.save()
                        messages.info(
                            self.request, 'Il ne vous reste plus que le paiement - default')
                        return redirect('payment-apero')
                    else:
                        messages.info(
                            self.request, "Pas de profil enregistré")
                        return redirect('checkout-apero')
                else:
                    name = form.cleaned_data.get('name')
                    prenom = form.cleaned_data.get('prenom')
                    phone = form.cleaned_data.get('phone')
                    email = form.cleaned_data.get('email')
                    date_de_livraison = form.cleaned_data.get('date_de_livraison')
                    couvert = form.cleaned_data.get('couvert')
                    
                    

                    if is_valid_form([name, prenom, phone, email]):
                        adresse_info = Info(
                            user=self.request.user,
                            name=name,
                            prenom=prenom,
                            phone=phone,
                            email=email,

                        )
                        adresse_info.save()

                        order.information = adresse_info
                        # order.date_de_livraison = date_de_livraison
                        order.date_de_livraison = datetime.datetime.strptime(date_de_livraison, '%d/%m/%Y %H:%M' )
                        order.couvert = couvert
                       
                        
                        order.save()

                        save_address = form.cleaned_data.get(
                            'save_address')
                        if save_address:
                            adresse_info.default = True
                            adresse_info.save()

                        messages.info(
                            self.request, 'Il ne vous reste plus que le paiement')
                        return redirect('payment-apero')
                    else:
                        messages.info(
                            self.request, "Vos informations personnelles ne sont pas complètes")
                        return redirect("checkout-apero")

            else:
                args['form'] = form
                messages.info(self.request, "Le formulaire n'est pas valide")
                return render(self.request, 'checkout-apero.html', args)
        except ObjectDoesNotExist:
            messages.info(self.request, "Vous n'avez pas de commande pour le moment")
            return redirect('order-summary-apero')


class PaymentView(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False,type_of_order='Dejeuner')
        if order.information:
            context = {
                'order': order,
                # 'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, 'payment-dejeuner.html', context)
        else:
            messages.warning(
                self.request, "Vous devez remplir le formulaire avant d'accèder au paiement ")
            return redirect("checkout")
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False, type_of_order='Dejeuner')
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total())
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                currency='eur',
                # replace by token in prod 'tok_visa'
                source=token,
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
            
            context = {
                'user': order.information.full_name,
                'user_email': order.information.email, 
                'user_phone': order.information.phone, 
                'date_delivery': order.date_de_livraison,
                'ref': order.ref_code,
                'total': order.payment.amount,
                'product': order.products.all(),
                
            }
            subject = "Déjeuner sur l'eau: Votre commande a bien été prise en compte !"
            html_message = render_to_string('email-order-confirmation.html', context)
            text_message = strip_tags(html_message)
            from_email = 'david.crenin@gmail.com'
            to = order.information.email
            send_mail(subject, text_message, from_email, [to], html_message=html_message, fail_silently=False)

            messages.info(
                self.request, "Votre commande a été bien été prise en compte")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("payment-dejeuner")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Veuillez réessayer un peu plus tard ! Le service est saturé pour le moment")
            return redirect("payment-dejeuner")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.warning(self.request, "Les données ne sont pas corrects")
            return redirect("payment-dejeuner")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Un problème technique est survenu !")
            return redirect("payment-dejeuner")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Problème de réseau")
            return redirect("payment-dejeuner")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("payment-dejeuner")

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("payment-dejeuner")


class PaymentAperoView(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False, type_of_order='Apero')
        if order.information:

            context = {
                'order': order,
                # 'DISPLAY_COUPON_FORM': False
            }

            return render(self.request, 'payment-apero.html', context)
        else:
            messages.warning(
                self.request, "Vous devez remplir le formulaire avant d'accèder au paiement ")
            return redirect("checkout-apero")
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False, type_of_order='Apero')
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total())
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                currency='eur',
                # replace by token in prod 'tok_visa'
                source=token,
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
            
            context = {
                'user': order.information.full_name,
                'user_email': order.information.email, 
                'user_phone': order.information.phone, 
                'date_delivery': order.date_de_livraison,
                'ref': order.ref_code,
                'total': order.payment.amount,
                'product': order.products.all(),
                
            }

            subject = "Déjeuner sur l'eau: Votre commande a bien été prise en compte !"
            html_message = render_to_string('email-order-confirmation.html', context)
            text_message = strip_tags(html_message)
            from_email = 'david.crenin@gmail.com'
            to = order.information.email
            send_mail(subject, text_message, from_email, [to], html_message=html_message, fail_silently=False)

            messages.info(
                self.request, "Votre commande a été bien été prise en compte")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("payment-apero")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Veuillez réessayer un peu plus tard ! Le service est saturé pour le moment")
            return redirect("payment-apero")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.warning(self.request, "Les données ne sont pas corrects")
            return redirect("payment-apero")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Un problème technique est survenu !")
            return redirect("payment-apero")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Problème de réseau")
            return redirect("payment-apero")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("payment-apero")

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("payment-apero")

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

                messages.info(self.request, 'Votre demande de remboursement a bien été prise en compte !')
                return redirect('home')

            except ObjectDoesNotExist:
                messages.info(self.request, "La référence commande communiquée n'est pas valable")
                return redirect('request-refund')



class OrderDash(View):
   

    def get(self, *args, **kwargs):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        orders_dej = Order.objects.filter(type_of_order='Dejeuner', ordered=True, is_delivered=False).order_by('-date_de_livraison')
        orders_dej_today = Order.objects.filter(type_of_order='Dejeuner', ordered=True, is_delivered=False, date_de_livraison__date=datetime.datetime.now()).order_by('-date_de_livraison')
        orders_dej_tomorrow = Order.objects.filter(type_of_order='Dejeuner', ordered=True, is_delivered=False, date_de_livraison__date=tomorrow.date()).order_by('-date_de_livraison')

        orders_apero = Order.objects.filter(type_of_order='Apero', ordered=True, is_delivered=False).order_by('-date_de_livraison')
        orders_apero_today = Order.objects.filter(type_of_order='Apero', ordered=True, is_delivered=False, date_de_livraison__date=datetime.datetime.now()).order_by('-date_de_livraison')
        orders_apero_tomorrow = Order.objects.filter(type_of_order='Apero', ordered=True, is_delivered=False, date_de_livraison__date=tomorrow.date()).order_by('-date_de_livraison')

        orders_all = Order.objects.filter(ordered=True, is_delivered=False).order_by('-date_de_livraison')
        orders_all_today = Order.objects.filter(ordered=True, is_delivered=False, date_de_livraison__date=datetime.datetime.now()).order_by('-date_de_livraison')
        orders_all_tomorrow = Order.objects.filter(ordered=True, is_delivered=False, date_de_livraison__date=tomorrow.date()).order_by('-date_de_livraison')
      
        form = DeliveredForm(auto_id=False)
        context = {
            "orders_dej": orders_dej,
            "orders_dej_today": orders_dej_today,
            "orders_dej_tomorrow": orders_dej_tomorrow,

            "orders_apero": orders_apero,
            "orders_apero_today": orders_apero_today,
            "orders_apero_tomorrow": orders_apero_tomorrow,

            "orders_all": orders_all,
            "orders_all_today": orders_all_today,
            "orders_all_tomorrow": orders_all_tomorrow,
            
            "form": form,
            "today": datetime.datetime.now(),

        }
        return render(self.request, 'order-list.html', context)

    # def post(self,*args,**kwargs):
    #     orders_dej = Order.objects.filter(type_of_order='Dejeuner', ordered=True, is_delivered=False)
    #     form = DeliveredForm(self.request.POST)
    #     data = {}
    #     if form.is_valid():
    #         is_delivered = form.cleaned_data['is_delivered']
    #         try:
    #             if is_delivered:
    #                 order = orders_dej[0]
    #                 order.is_delivered = True
    #                 order.save()
    #             messages.info(self.request, 'LIVRER')
    #             return redirect('order')
    #         except ObjectDoesNotExist:
    #             messages.info(self.request, "La commande n'existe pas")
    #             return redirect('order')

def is_delivered(request, ref_code):
    form = DeliveredForm(request.POST)
    orders_dej = Order.objects.get(ref_code=ref_code)
    data ={}
    if form.is_valid():
        is_delivered = form.cleaned_data['is_delivered']
        try:
            if is_delivered:
                order = orders_dej
                order.is_delivered = True
                order.save()
                
            # messages.info(request, 'LIVRER')
            # return redirect('order')
            return JsonResponse(data)
        except ObjectDoesNotExist:
            messages.info(request, "La commande n'existe pas")
            return redirect('order')






class mentionsLegales(TemplateView):
    template_name = 'mentions-legales.html'


class ConditionsGenerales(TemplateView):
    template_name = 'cgv.html'


class AvisCreate(View):
    def get(self, *args, **kwargs):
        form = AvisForm()

        context = {
            'form': form,

        }
        return render(self.request, "avis.html", context)

    def post(self, *args):
        
        avis = Avis.objects.create()
        form = AvisForm(self.request.POST or None)
        args = {}
        if form.is_valid():
            email = form.cleaned_data.get('email')
            objet = form.cleaned_data.get('objet')
            message = form.cleaned_data.get('message')
            avis.email = email
            avis.objet = objet
            avis.message = message
            avis.save()
            messages.info(self.request, 'Votre avis a bien été enregistré')
            return redirect('home')
        else:
            args['form'] = form
            messages.info(self.request, 'Le formulaire nest pas valide')
            return render(self.request, 'avis.html', args)


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'contact.html', context)

    def post(self, request):
        form = ContactForm(self.request.POST or None)
        args = {}
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            send_mail(subject, message, from_email, [
                      'david.crenin@gmail.com'], fail_silently=False)
            messages.warning(
                request, 'Votre message a été envoyé !')
            return redirect('home')
        else:
            form = ContactForm(self.request.POST or None)
            args['form'] = form
            return render(self.request, 'contact.html', args)


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = self.request.user
        order = Order.objects.filter(user=user, ordered=True).order_by('-date_de_creation')
        
        context = {
            'user': user,
            'order': order,
            
        }

        return render(self.request, 'profile.html', context)


def custom_error_404_view(request, exception):
    return render(request, '404.html', status = 404)

def custom_error_500_view(request):
    return render(request, '500.html', status=500)

def delivery(request):
    return render(request, 'livraison.html')








# def get_coupon(request, code):
#     try:
#         coupon = Coupon.objects.get(code=code)
#         return coupon
#     except ObjectDoesNotExist:
#         messages.info(request, "Ce code promo n'existe pas")
#         return redirect('checkout')


# class AddCouponView(View):

#     def post(self, *args, **kwargs):
#         form = CouponForm(self.request.POST or None)
#         if form.is_valid():
#             try:
#                 code = form.cleaned_data.get('code')
#                 order = Order.objects.get(
#                     user=self.request.user,
#                     ordered=False
#                 )
#                 order.coupon = get_coupon(self.request, code)
#                 order.save()
#                 messages.info(self.request, 'Le code coupon est accepté')
#                 return redirect('checkout')
#             except ObjectDoesNotExist:
#                 messages.info(self.request, "You do not have an active order")
#                 return redirect('checkout')



# PDF VIEW

from django.template.loader import get_template

#import render_to_pdf from util.py 
from .utils import render_to_pdf 


def GeneratePdf(request, ref_code):
    template = get_template('invoice.html')
    order = Order.objects.get(ref_code=ref_code)
    print(order.information.phone)
    context = {
        "name": order.information.name,
        "prenom": order.information.prenom,
        "phone": order.information.phone,
        "email": order.information.email,
        "ref_code": order.ref_code,
        'products': order.products.all(),
        "total": order.get_total(),
        "amount": 1399.99,
        "today": "Today",
    }
    html = template.render(context)
    pdf = render_to_pdf('invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Commande_%s.pdf" %(order.ref_code)
        content = "inline; filename=%s" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

