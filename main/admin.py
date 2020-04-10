from django.contrib import admin
from .models import Product, OrderProduct, Order, Payment, Coupon, Refund, Info, Avis
# Register your models here.


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'type_of_order',
        'ordered',
        'is_delivered',
        'received',
        'refund_requested',
        'refund_granted',
        'payment',
        'coupon'
    ]

    list_display_links = [
        'user',
        'payment',
        'coupon'
    ]
    list_filter = [
        'ordered',
        'is_delivered',
        'received',
        'refund_requested',
        'refund_granted'

    ]

    search_fields = [
        'user__email',
        'ref_code'
    ]

    actions = [make_refund_accepted]


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount']


class InfoAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'code_postal',
        'pays',
        'phone',
        'email',
    ]


admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Coupon)
admin.site.register(Avis)
admin.site.register(Info, InfoAdmin)
admin.site.register(Refund)


admin.site.index_title = "Tableau de bord"
admin.site.site_header = "Dejeuner sur l'eau"
