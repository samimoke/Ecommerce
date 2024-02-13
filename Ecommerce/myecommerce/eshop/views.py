from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView,View
from .models import Item,OrderItem,Order,Address,ChapaTransaction,Coupon,Refund_Request
from django.core.mail import send_mail
from django.utils import timezone
from myecommerce import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from.forms import UserLoginForm,RegistrationForm,ContactForm,CheckoutForm,CouponForm,RefundForm, SubscriptionForm,PaymentForm
from myecommerce.settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group,User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
import random
import string
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Wishlist
from django.http import Http404
# from chapaclient import ChapaClient
# from django_chapa.client import ChapaClient
# from .tokens import account_activation_token

# Create your views here.
def products(request):
    context={
        'items':Item.objects.all()

    }
    return render(request,'shop.html',context)
class ProductDetailView(DetailView):
    template_name = 'shop-detail.html'
    model = Item
    context_object_name = 'product'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     item = self.get_object()  # Fetch the item object

    #     context['item_quantity'] = item.quantity  # Pass the quantity to the template's context

    #     return context
class Home(ListView):
    model=Item
    template_name='index.html'
@login_required
def add_to_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
           order_item.quantity +=1
           order_item.save()
           messages.info(request,'This item quantity is uppdated ')
           return redirect('order_summery')
        else:
            order.items.add(order_item)
            messages.info(request,'This item  is added into your cart')
            return redirect('order_summery')
           
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,'This item is added into your cart')
    return redirect('order_summery')
@login_required(login_url='login')
def remove_from_cart(request,slug):
     item=get_object_or_404(Item,slug=slug)
     order_qs=Order.objects.filter(user=request.user,ordered=False)
     if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
           order_item=OrderItem.objects.filter(user=request.user,ordered=False)[0]
           order.items.remove(order_item)
           messages.info(request,'This item is removed from your cart')
           return redirect('order_summery') 
        else:
          messages.info(request,'This item  is not found in your cart')
          return redirect('product',slug=slug)
     else:
       messages.info(request,'You do not have an active cart')
       return redirect('product',slug=slug)
       
    #  return redirect('product',slug=slug)
@login_required(login_url='login')
def remove_single_item_from_cart(request,slug):
     item=get_object_or_404(Item,slug=slug)
     order_qs=Order.objects.filter(user=request.user,ordered=False)
     if order_qs.exists():
        order=order_qs[0]
        
        if order.items.filter(item__slug=item.slug).exists():
           order_item=OrderItem.objects.filter(
               user=request.user,
               ordered=False)[0]
           if order_item.quantity > 1:
               
              order_item.quantity -=1
              order_item.save()
           else:
               order.items.remove(order_item)
           messages.info(request,'This item is updated')
           return redirect('order_summery') 
        else:
          messages.info(request,'This item  is not found in your cart')
          return redirect('order_summery')
     else:
       messages.info(request,'You do not have an active cart')
       return redirect('order_summery') 

from django.contrib.auth.models import Group
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                group=Group.objects.get(name="Member")
                user.groups.add(group)
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                # to_email = form.cleaned_data.get('email')
                # email = EmailMessage(mail_subject, message, to=[to_email])
                send_mail(mail_subject, message, 'samimokehirpa@gmail.com', [user.email])
                # email.send()
                return redirect('login')
        else:
            form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})




        
# @login_required
# @cache_control(max_age=3600)  # Set cache control to 1 hour
# def deactivate_account(request):
#     user = request.user
#     # Deactivate user's account
#     user.is_active = False
#     user.save()
#     # Logout user
#     logout(request)
#     return redirect('login')

def logins(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
           username=request.POST.get('username')
           password=request.POST.get('password')
           try:
               user=User.objects.get(username=username)
    
           except:
            # print('Username does not exist!')
            
               messages.error(request, " username does not exist")
               return render(request,"login.html")

           authenticate(request,username=username,password=password)
           user = authenticate(request, username=username, password=password)
           if user is not None:
               login(request, user)
            # if request.user.is_authenticated and user:
               if user.is_authenticated and user.is_staff and user.is_superuser:
                   messages.success(request,'Authentication is successful')
                   return redirect('admin:index')
               elif user.is_authenticated:
                   return redirect('my_account')
               else:
                  return redirect('home')
           else:
               messages.error(request, "Username or password incorrect")
               return render(request,"login.html")
       else:
           f = UserLoginForm()
           return render(request = request,
                    template_name = "login.html",
                context={"f":f})
def is_valid_form(values):
    valid=True
    for field in values:
        if field=='':
            valid=False
        return valid


class Checkout(LoginRequiredMixin,View):
    login_url='login'
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            form=CheckoutForm()
            context={
                'form':form,
                'couponform':CouponForm(),
                'order':order,
                'DISPLAY_COUPON_FORM':True
            }
            shipping_address_qs=Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True

            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address':shipping_address_qs[0]})

            billing_address_qs=Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True

            )
            if billing_address_qs.exists():
                context.update({'default_billing_address':billing_address_qs[0]})

            return render(self.request,'checkout.html',context)
        except ObjectDoesNotExist:
            # messages.info(self.request,'You donot have an active order')
           return redirect('checkout')
    def post(self,*args, **kwargs):
        form=CheckoutForm(self.request.POST or None)
        order_not_exist_message_displayed = False
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                use_default_shipping=form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print("Use this default shipping")
                    address_qs=Address.objects.filter(
                    user=self.request.user,
                    address_type='S',
                    default=True

            )
                    if address_qs.exists():
                        shipping_address=address_qs[0]
                        order.shipping_address=shipping_address
                        order.save()
                    else:
                        print('You do not have default shipping address')
                        return redirect('checkout')
                else:
                    print('User enter new shipping address')

                    first_name=form.cleaned_data.get('first_name')
                    last_name=form.cleaned_data.get('last_name')
                    username=form.cleaned_data.get('username')
                    email=form.cleaned_data.get('email')
                    shipping_address1=form.cleaned_data.get('shipping_address1')
                    shipping_address2=form.cleaned_data.get('shipping_address2')
                    shipping_country=form.cleaned_data.get('shipping_country')
                    shipping_zip=form.cleaned_data.get('shipping_zip')
                    # set_billing_address=form.cleaned_data.get('set_billing_address')
                    # save_info=form.cleaned_data.get('save_info')
                    payment_method=form.cleaned_data.get('payment_method')
                    if is_valid_form(['first_name','last_name','username','email','shipping_address1','sipping_country','shipping_zip']):
                            
                        shipping_address=Address(
                        user=self.request.user,
                        first_name= first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        address1=shipping_address1,
                        address2=shipping_address2,
                        country=shipping_country,
                        zip=shipping_zip,
                        address_type='S'


                        )
                        shipping_address.save()
                        order.shipping_address=shipping_address
                        order.save()
                        set_default_shipping=form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default=True
                            shipping_address.save()
                        else:
                            messages.info(self.request,'Please fill in the required fields in shipping address')
                    
                    
                use_default_billing=form.cleaned_data.get('use_default_billing')
                same_billing_address=form.cleaned_data.get('same_billing_address')
                if same_billing_address:
                    billing_address=shipping_address
                    billing_address.pk=None
                    billing_address.save()
                    billing_address.address_type='B'
                    billing_address.save()
                    order.billing_address=billing_address
                    order.save()

                elif use_default_billing:
                    print("Use this default billing")
                    address_qs=Address.objects.filter(
                    user=self.request.user,
                    address_type='B',
                    default=True

            )
                    if address_qs.exists():
                        billing_address=address_qs[0]
                        order.billing_address=billing_address
                        order.save()
                    else:
                        messages.info(self.request,'You do not have default billing address')
                        return redirect('checkout')
                else:
                    print('User enter new billing address')

                    first_name=form.cleaned_data.get('first_name')
                    last_name=form.cleaned_data.get('last_name')
                    username=form.cleaned_data.get('username')
                    email=form.cleaned_data.get('email')
                    billing_address1=form.cleaned_data.get('billing_address1')
                    billing_address2=form.cleaned_data.get('billing_address2')
                    billing_country=form.cleaned_data.get('billing_country')
                    billing_zip=form.cleaned_data.get('billing_zip')
                    # set_billing_address=form.cleaned_data.get('set_billing_address')
                    # save_info=form.cleaned_data.get('save_info')
                    payment_method=form.cleaned_data.get('payment_method')
                    if is_valid_form(['first_name','last_name','username','email','billing_address1','billing_country','billing_zip']):
                            
                        billing_address=Address(
                        user=self.request.user,
                        first_name= first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        address1=billing_address1,
                        address2=billing_address2,
                        country=billing_country,
                        zip=billing_zip,
                        address_type='B'


                        )
                        billing_address.save()
                        order.billing_address=billing_address
                        order.save()
                        set_default_billing=form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                           billing_address.default=True
                           billing_address.save()
                    else:
                        messages.info(self.request,'Please fill in the required fields in billing address')

                payment_method=form.cleaned_data.get('payment_method')

                if payment_method=='CH':
                    return redirect('payment',payment_method='chapa')
                elif payment_method=='PP':
                    return render('payment',payment_method='paypal')
                else:
                    messages.warning(self.request,'invalid payment option is selected')
                return redirect('checkout')
            else:
                messages.warning(self.request,'Checkout Failed')
        except ObjectDoesNotExist:  
            if not order_not_exist_message_displayed:  # Display message only once
                # messages.warning(self.request, 'You do not have an active order')
                order_not_exist_message_displayed = True  # Set flag to True
  
            # messages.warning(self.request,'You donot have an active order')
        return redirect('checkout')
# def wishlists(request):
#     return render(request,'wishlist.html')
def myaccount(request):
    return render(request,'my-account.html')
def gallery(request):
    return render(request,'gallery.html')
def account_logout(request):
    logout(request)
    return redirect('login')
def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Save the form data to database (assuming contactform is a ModelForm)
            form.save()

            # Send email to receiver
            # receiver_email = 'samimokehirpa@gmail.com'  # Replace with the receiver's email address
            receiver_email=EMAIL_HOST_USER
            send_mail(
                'Contact Form Submission from {}'.format(name),
                message,
                email,  # Sender's email
                [receiver_email],
                fail_silently=False,
            )

            # Send a reply email to the sender
            sender_message = "Welcome to our page! We will contact you soon."
            send_mail(
                'Thank you for contacting us',
                sender_message,
                receiver_email,  # Replace with your own email address
                [email],  # Sender's email
                fail_silently=False,
            )

            return render(request, 'thanks.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'contact-us.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'account_activation_invalid.html')
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class OrderSummeryView(LoginRequiredMixin,View):
    login_url='login'
    def get(self, *args, **kwargs):
        try:
           order=Order.objects.get(user=self.request.user, ordered=False)
           context={
               'object':order
           }
           return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,'You donot have an active order')
            return redirect('/')
    

        return render (self.request, 'order_summary.html')
def update_order_status(order_id, new_status):
        order = get_object_or_404(Order, order_id=order_id)
        order.status = new_status
        order.save()

class Payment(LoginRequiredMixin,View):
    login_url='login'
    def get(self,*args,**kwargs):
        # form=CheckoutForm
        order=Order.objects.get(user=self.request.user,ordered=False)
        if order.billing_address:
                
            context={
                # 'form':form,
                'couponform':CouponForm,
                'order':order,
                'DISPLAY_COUPON_FORM':False
            }

            return render(self.request,'payment.html',context)
        else:
            messages.info(self.request,'You do not have billing address')
            return redirect('checkout')
   
# def payment(request,self,*args, **kwargs):
               
def get_coupon(request,code):
    try:
        coupon= Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request,'Coupon doesnot exist')
        return redirect('checkout')

class Add_Coupon(LoginRequiredMixin,View):
    login_url='login'
    def post(self, *args, **kwargs):
        form=CouponForm(self.request.POST or None)
        if self.request.method=="POST":
            if form.is_valid():
                code=form.cleaned_data.get('code')
                try:
                    order=Order.objects.get(user=self.request.user,ordered=False)
                    
                    order.coupon=get_coupon(self.request,code)
                    order.save()
                    messages.success(self.request,'Successfully Coupon is added')
                    return redirect('checkout')

                except ObjectDoesNotExist:
                    messages.info(self.request,'You donot have coupon')
                    return redirect('checkout')
        return redirect('checkout') 
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():   
            order=Order.objects.get(user=request.user,ordered=False)
            # total_amount = order.get_final_price() * 100  
        
            # order_id = order.id
        
        # Get form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            tx_ref = request.POST.get('tx_ref')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            return_url = request.POST.get('return_url')
            
            
            # Save form data to the ChapaTransactionMixin model
            chapa_transaction = ChapaTransaction.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                tx_ref=tx_ref,
                amount=amount,
                currency=currency,
                return_url=return_url
            )

            chapa_transaction.save()
            # Redirect user to Chapa website URL with the necessary parameters
            chapa_url = 'https://api.chapa.co/v1/hosted/pay'

            payload = {
                # 'public_key': settings.CHAPA_PUBLIC_KEY,  # Assuming you have stored the public key in settings
                'public_key':settings.CHAPA_PUBLIC_KEY,
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'tx_ref': tx_ref,
                'amount': amount,
                'currency': currency,
                'return_url': return_url,
                'cancel_url': 'http://127.0.0.1:8000'  # Assuming you have a cancel URL
            }
            
            # Make a POST request to Chapa website URL
            response = requests.post(chapa_url, data=payload)
            order_items=order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save() 

            order.ordered=True
            # order.payment=payment
            order.payment = chapa_transaction
            order.ref_code=create_ref_code()
            # order.coupon=coupon
            coupon_code = request.POST.get('coupon_code')
            if coupon_code:
                coupon = get_coupon(request, coupon_code)
                if coupon:
                    order.coupon = coupon
            order.save()
            # Redirect the user to the Chapa website
            return redirect(response.url)
    else:
        return render(request, 'index.html')

       
# def get_coupon(request,code):
#     try:
#         coupon= Coupon.objects.get(code=code)
#         return coupon
#     except ObjectDoesNotExist:
#         messages.info(request,'Coupon doesnot exist')
#         return redirect('checkout')

# class Add_Coupon(LoginRequiredMixin,View):
#     login_url='login'
#     def post(self, *args, **kwargs):
#         form=CouponForm(self.request.POST or None)
#         if self.request.method=="POST":
#             if form.is_valid():
#                 code=form.cleaned_data.get('code')
#                 try:
#                     order=Order.objects.get(user=self.request.user,ordered=False)
                    
#                     order.coupon=get_coupon(self.request,code)
#                     order.save()
#                     messages.success(self.request,'Successfully Coupon is added')
#                     return redirect('checkout')

#                 except ObjectDoesNotExist:
#                     messages.info(self.request,'You donot have coupon')
#                     return redirect('checkout')
#         return redirect('checkout') 
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase+string.digits,k=20))
class Refund_Requests(View):
    def get(self,*args, **kwargs):
        form=RefundForm()
        context={
            'form':form
        }
        return render(self.request,'request_refund.html',context)

    def post(self,*args, **kwargs):
        form=RefundForm(self.request.POST)
        if form.is_valid():
            ref_code=form.cleaned_data.get('ref_code')
            message=form.cleaned_data.get('message')
            email=form.cleaned_data.get('email')
            try:
                order=Order.objects.get(ref_code=ref_code)
                order.refund_requested=True
                order.save()
                refund=Refund_Request()
                refund.order=order
                refund.reason=message
                refund.email=email
                refund.save()
                messages.info(self.request,'your request is recieved')
            except ObjectDoesNotExist:
                messages.info(self.request,'You  do not have an order')
                return redirect("/")
        return redirect("/")
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscribe_success')
    else:
        form = SubscriptionForm()
    return render(request, 'shop.html', {'form': form})

def subscribe_success(request):
    return render(request, 'subscribe_succuss.html')
@login_required
# @require_POST
def add_to_wishlist(request, slug):
     product=get_object_or_404(Item,slug=slug)
     if request.method == 'POST':
        # product = Item.objects.get(slug=slug)
        try:
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect to login if user is not authenticated
            wishlist, created = Wishlist.objects.get_or_create(user=request.user,id=product.pk)
            product_qs=Wishlist.objects.filter(user=request.user,id=product.pk)
            # order_item,created=OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
            # order_qs=Order.objects.filter(user=request.user,ordered=False)
            if product_qs.exists():
             myproduct=product_qs[0]
            if myproduct.products.filter(id=product.pk).exists():
            
                 messages.info(request,'This item already in wishlist ')
                 return redirect('add_to_wishlist', slug=slug)
            else:
                wishlist.products.add(product)
                messages.info(request,'This item is added to your wishlist ')
            
                return redirect('add_to_wishlist', slug=slug)  # Redirect to wishlist page
        except Item.DoesNotExist:
                raise Http404("Item does not exist") 
     else:
        products = Item.objects.all()
        return render(request, 'wishlist.html', {'products': products})
     
@login_required(login_url='login')
def remove_from_wishlist(request, slug):
    
        product = get_object_or_404(Item, slug=slug)
        product_qs = Wishlist.objects.filter(user=request.user)
    
        if product_qs.exists():
           for product_to_remove in product_qs:
        
              if product_to_remove.products.filter(id=product.pk).exists():
        
                 product_to_remove.products.remove(product)
                 messages.info(request,'This item is removed from wishlist')
              else:
                messages.info(request,'This item  is not found in your wishlist')
              return redirect('add_to_wishlist', slug=slug) 
        
        else:
            messages.info(request,'You do not have a wishlist')
            return redirect('add_to_wishlist',slug=slug) 


    

 

