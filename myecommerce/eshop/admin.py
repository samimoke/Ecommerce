from django.contrib import admin
from .models import Item,OrderItem,Order,Contactus,Address,ChapaTransaction,Coupon,Refund_Request, Subscription,Wishlist

def make_refund_accepted(modeladmin,request,queryset):
   queryset.update(refund_requested=False,refund_granted=True)
make_refund_accepted.short_description='Orders updated to refund granted'
class AdminOrder(admin.ModelAdmin):
   list_display=['user',
                 'ordered',
                 'being_delivered',
                 'received',
                 'refund_requested',
                 'refund_granted',
                 'coupon',
                 'billing_address',
                 'shipping_address',
                 'payment'
                 ]
   list_filter=['user',
                 'being_delivered',
                 'received',
                 'refund_requested',
                 'refund_granted'
                 ]
   list_display_links=[
                  'user',
                 'coupon',
                 'billing_address',
                 'shipping_address',
                 'payment',
               
                 ]
   actions=[
      make_refund_accepted
   ]
   
class AddressAdmin(admin.ModelAdmin):
   list_display=[
      'user',
      'first_name',
      'last_name',
      'username',
      'email',
      'address1',
      'address2',
      'country',
      'zip',
      'address_type',
      'default'
   ] 
   list_filter=[
      'default',
      'address_type',
      'country'
   ]
   search_fields=[
      'user',
      'default',
      'address1',
      'address2',
      'zip',
      'country'
   ]
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order,AdminOrder)
admin.site.register(Contactus)
admin.site.register(Address,AddressAdmin)
admin.site.register(ChapaTransaction)
admin.site.register(Coupon)
admin.site.register(Refund_Request)
admin.site.register(Subscription)
admin.site.register(Wishlist)