from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePageView, ProductListView, ProductDetailView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_product_from_cart, CheckoutView, DeliveryView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug>', ProductDetailView.as_view(), name='product-detail'),
    path('add_to_cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove_product_from_cart/<slug>', remove_single_product_from_cart,
         name='remove-single-product-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
