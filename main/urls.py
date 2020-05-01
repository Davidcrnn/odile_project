from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    HomePageView,

    ProductListView,
    ProductAperoView,
    #     ProductDetailView,
    add_to_cart,
    remove_from_cart,
    remove_single_product_from_cart,
    add_single_item_to_cart,

    OrderSummaryDejeunerView,
    OrderSummaryAperoView,
    CheckoutView,
    CheckoutViewApero,
    PaymentView,
    PaymentAperoView,

    RequestRefundView,
    OrderDash,
    mentionsLegales,
    ConditionsGenerales,
    AvisCreate,
    ContactView,
    ProfileView,
    is_delivered,
    GeneratePdf,
    delivery,

    #     AddCouponView,


)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('menu-dejeuner/', ProductListView.as_view(), name='products'),
    path('menu-apero/', ProductAperoView.as_view(), name='products-apero'),
    #     path('products/<slug>', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-single-item-to-cart/<slug>/',
         add_single_item_to_cart, name='add-single-item-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-product-from-cart/<slug>', remove_single_product_from_cart,
         name='remove-single-product-from-cart'),
    path('panier-dejeuner/', OrderSummaryDejeunerView.as_view(),
         name='order-summary-dejeuner'),
    path('panier-apero/', OrderSummaryAperoView.as_view(),
         name='order-summary-apero'),
    path('livraison-dejeuner/', CheckoutView.as_view(), name='checkout'),
    path('livraison-apero/', CheckoutViewApero.as_view(), name='checkout-apero'),
    path('paiement-dejeuner/', PaymentView.as_view(), name='payment-dejeuner'),
    path('paiement-apero/', PaymentAperoView.as_view(), name='payment-apero'),
    #     path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('demande-remboursement/',
         RequestRefundView.as_view(), name='request-refund'),
    path('tableau-de-bord/', OrderDash.as_view(), name='order'),
    path('mentions-legales/', mentionsLegales.as_view(), name='mentions'),
    path('conditions-generales/', ConditionsGenerales.as_view(), name='cgv'),
    path('votre-avis/', AvisCreate.as_view(), name='avis'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('profil/', ProfileView.as_view(), name='profil'),
    path('is_delivered/<ref_code>/', is_delivered, name='is_delivered'),
    path('pdf/<ref_code>', GeneratePdf, name='pdf'),
    path('livraison', delivery, name='livraison'),



]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
