from django import template
from main.models import Order

register = template.Library()


@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            total = qs[0].products.count()
            return total

    return 0
