from django.contrib import admin
from .models import Product, OrderProduct, Order
# Register your models here.

admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)

admin.site.index_title = "Tableau de bord"
admin.site.site_header = "Dejeuner sur l'eau"
