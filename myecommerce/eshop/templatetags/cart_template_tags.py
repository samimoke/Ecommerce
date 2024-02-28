from django import template
from eshop.models import Order

register=template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs=Order.objects.filter(user=user,ordered=False)
        if qs.exists():
             order_items = qs[0].items.all()
             return order_items.count()
            # return qs[0].items.count()
    return 0


