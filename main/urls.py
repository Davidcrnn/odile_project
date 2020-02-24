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
    OrderSummaryView,
    remove_single_product_from_cart,
    CheckoutView,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    add_single_item_to_cart,
    OrderDash,
    mentionsLegales,
    ConditionsGenerales,




)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('menu-apero/', ProductAperoView.as_view(), name='products-apero'),
    path('products/<slug>', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-single-item-to-cart/<slug>/',
         add_single_item_to_cart, name='add-single-item-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-product-from-cart/<slug>', remove_single_product_from_cart,
         name='remove-single-product-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # path('delivery/', DeliveryView.as_view(), name='delivery'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('order/', OrderDash.as_view(), name='order'),
    path('mentions-legales/', mentionsLegales.as_view(), name='mentions'),
    path('conditions-generales/', ConditionsGenerales.as_view(), name='cgv'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
