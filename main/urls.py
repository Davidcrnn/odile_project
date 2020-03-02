from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView,
    ProductListView,
    ProductAperoView,
    ProductDetailView,
    add_to_cart,
    remove_from_cart,
    remove_from_cart_apero,
    OrderSummaryDejeunerView,
    OrderSummaryAperoView,
    remove_single_product_from_cart,
    remove_single_product_from_cart_apero,
    CheckoutView,
    CheckoutViewApero,
    PaymentView,
    PaymentAperoView,
    AddCouponView,
    RequestRefundView,
    add_single_item_to_cart,
    add_single_item_to_cart_apero,
    OrderDash,
    mentionsLegales,
    ConditionsGenerales,
    AvisCreate,
    ContactView,







)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('menu-dejeuner/', ProductListView.as_view(), name='products'),
    path('menu-apero/', ProductAperoView.as_view(), name='products-apero'),
    path('products/<slug>', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-single-item-to-cart/<slug>/',
         add_single_item_to_cart, name='add-single-item-to-cart'),
    path('add-single-item-to-cart-apero/<slug>/',
         add_single_item_to_cart_apero, name='add-single-item-to-cart-apero'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-from-cart-apero/<slug>/',
         remove_from_cart_apero, name='remove-from-cart-apero'),
    path('remove-single-product-from-cart/<slug>', remove_single_product_from_cart,
         name='remove-single-product-from-cart'),
    path('remove-single-product-from-cart-apero/<slug>', remove_single_product_from_cart_apero,
         name='remove-single-product-from-cart-apero'),
    path('panier-dejeuner/', OrderSummaryDejeunerView.as_view(),
         name='order-summary-dejeuner'),
    path('panier-apero/', OrderSummaryAperoView.as_view(),
         name='order-summary-apero'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout-apero/', CheckoutViewApero.as_view(), name='checkout-apero'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment-apero/', PaymentAperoView.as_view(), name='payment-apero'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('order/', OrderDash.as_view(), name='order'),
    path('mentions-legales/', mentionsLegales.as_view(), name='mentions'),
    path('conditions-generales/', ConditionsGenerales.as_view(), name='cgv'),
    path('votre-avis/', AvisCreate.as_view(), name='avis'),
    path('contact/', ContactView.as_view(), name='contact'),





]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
