from typing import Set
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from uuid import uuid4
from django.utils.text import slugify

Category_Choice=(
    ('fr','fruit'),
    ('vg','vegitable'),
)

Address_Choice=(
    ('B','billing_address'),
    ('S','Shipping_address')
)

class Item(models.Model):
     title=models.CharField(max_length=500)
     discount_price=models.FloatField(blank=True, null=True)
     price=models.FloatField()
     slug = models.SlugField(unique=True, max_length=150, blank=True)
     description=models.TextField()
     image=models.ImageField( upload_to='img',blank=True,null=True)
     
     def save(self, *args, **kwargs):
        # Generate slug from the title
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
     def __str__(self):
         return self.title
     
     def get_absolute_url(self):
         return reverse("product_detail", kwargs={"slug": self.slug})
     
     def get_add_to_cart_url(self):
         return reverse("add_to_cart",kwargs={"slug":self.slug})
     def get_add_to_wishlist_url(self):
         return reverse("add_to_wishlist",kwargs={"slug":self.slug})
     
     def get_remove_from_cart_url(self):
         return reverse("remove_from_cart", args=[self.slug])


class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    ordered=models.BooleanField(default=False)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price
    def get_total_saved_price(self):
        return self.get_total_item_price()-self.get_total_item_discount_price()
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()

    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ref_code=models.CharField(max_length=20)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateField(auto_now_add=True)
    ordered_date=models.DateField(auto_now_add=True)
    ordered=models.BooleanField(default=False)
    billing_address=models.ForeignKey('Address',related_name='billing_address' ,on_delete=models.SET_NULL,null=True,blank=True)
    shipping_address=models.ForeignKey('Address',related_name='shipping_address',on_delete=models.SET_NULL,null=True,blank=True)
    payment=models.ForeignKey('ChapaTransaction',on_delete=models.SET_NULL,null=True,blank=True)
    coupon=models.ForeignKey('Coupon',on_delete=models.SET_NULL,null=True,blank=True)
    being_delivered=models.BooleanField(default=False)
    received=models.BooleanField(default=False)
    refund_requested=models.BooleanField(default=False)
    refund_granted=models.BooleanField(default=False)
    # item_id=models.IntegerField(null=False)

    def __str__(self):
        return self.user.username
    def get_total(self):
        total=0
        for order_item in self.items.all():
       
            total +=order_item.get_final_price()
            if self.coupon:
              total-=self.coupon.amount
        return total
class Contactus(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,null=True)
    subject=models.CharField(max_length=300)
    message=models.CharField(max_length=1000)
    def __str__(self):
        return self.name
class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address1=models.CharField(max_length=100,null=True)
    address2=models.CharField(max_length=50,null=True)
    country=CountryField(multiple=False,null=True)
    zip=models.CharField(max_length=20,null=True)
    address_type=models.CharField(max_length=1,choices=Address_Choice)
    default=models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.user.username

class ChapaTransactionMixin(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    # # amount = models.FloatField()
    # # currency = models.CharField(max_length=25, default='ETB')
    # user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True, default='sami')
    time_stamp=models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    tx_ref = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10,default='ETB')
    return_url = models.URLField()
     # incase the response is valuable in the future

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.first_name} - {self.last_name} | {self.amount}"
    
    def serialize(self) -> dict:
       return {
            'amount': self.amount,
            'currency': self.currency,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'description': self.description
        }

class ChapaTransaction(ChapaTransactionMixin):
    pass
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # username = models.CharField(max_length=100)
    # email = models.EmailField()
    # tx_ref = models.CharField(max_length=100)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    # currency = models.CharField(max_length=10,default='ETB')
    # return_url = models.URLField()
    
class Coupon(models.Model):
    code=models.CharField(max_length=15)
    amount=models.FloatField()

    def __str__(self):
        return self.code  
class Refund_Request(models.Model):
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    reason=models.CharField(max_length=500)
    accepted=models.BooleanField(default=False)
    email=models.EmailField()

    def __str__(self):
        return f"{self.pk}"
class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Item)
    @property
    def item_names(self):
        return self.products.values_list('title', flat=True)
    
    def add_to_wishlist(self, item):
        self.products.add(item)
  


    
