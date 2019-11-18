from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePageView, ProductListView, ProductDetailView, add_to_cart

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug>', ProductDetailView.as_view(), name='product-detail'),
    path('add_to_cart/<slug>/', add_to_cart, name='add-to-cart')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
