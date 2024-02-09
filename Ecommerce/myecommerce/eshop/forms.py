from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms
from django.core.validators import validate_email
from .models import ChapaTransaction, Contactus, Subscription
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES={
    ('CH','CHAPA'),
    ('PP','PAYPAL')
}
class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        
    
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        
    # email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}), validators=[validate_email])
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}), validators=[validate_email])
    password1 = forms.CharField( widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField( widget=forms.PasswordInput(attrs={'class':'form-control'}))
        
    
    

    class Meta:
        model = User
        
        fields = ('first_name','last_name','username','email', 'password1', 'password2')
        
class UserLoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}))
    # email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control',
    #                                                         'placeholder':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'password',
                                                                 'id': 'login-pwd'}))
class ContactForm(forms.ModelForm):
    class Meta:
        model=Contactus
        fields=['name','email','subject','message']
class CheckoutForm(forms.Form):
    first_name=forms.CharField(required=False)
    last_name=forms.CharField(required=False)
    username=forms.CharField(required=False)
    email=forms.EmailField(required=False)
    shipping_address1=forms.CharField(required=False)
    shipping_address2=forms.CharField(required=False)
    shipping_country=CountryField(blank_label='(select country)').formfield(required=False,widget=CountrySelectWidget(attrs={'class':'wide w-100'}))
    # state=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    shipping_zip=forms.CharField(required=False)
    same_billing_address=forms.BooleanField(required=False)
    
    
    first_name=forms.CharField(required=False)
    last_name=forms.CharField(required=False)
    username=forms.CharField(required=False)
    email=forms.EmailField(required=False)
    billing_address1=forms.CharField(required=False)
    billing_address2=forms.CharField(required=False)
    billing_country=CountryField(blank_label='(select country)').formfield(required=False,widget=CountrySelectWidget(attrs={'class':'wide w-100'}))
    # state=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    billing_zip=forms.CharField(required=False)
    same_shipping_address=forms.BooleanField(required=False)
    set_default_shipping=forms.BooleanField(required=False)
    use_default_shipping=forms.BooleanField(required=False)

    set_default_billing=forms.BooleanField(required=False)
    use_default_billing=forms.BooleanField(required=False)
    payment_method=forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)
class CouponForm(forms.Form):
    code=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
         'placeholder':'promo code',
         'arial-label' :'recipent\'s username',
        'aria-describedby':'basic-addon2'
    }))
class RefundForm(forms.Form):
    ref_code=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    message=forms.CharField(widget=forms.Textarea(attrs={'rows':4,'class':'form-control'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']
class PaymentForm(forms.Form):
     class Meta:
        model = ChapaTransaction
        fields = ['first_name', 'last_name', 'username', 'email', 'tx_ref', 'amount', 'currency', 'return_url']
    # public_key = forms.CharField(widget=forms.HiddenInput)
    # tx_ref = forms.CharField() #widget=forms.HiddenInput 
    # amount = forms.DecimalField()
    # currency = forms.CharField()
    # email = forms.EmailField()
    # first_name = forms.CharField()
    # last_name = forms.CharField()
    # description = forms.CharField(widget=forms.HiddenInput)
    # callback_url = forms.URLField(widget=forms.HiddenInput)
    # return_url = forms.URLField(widget=forms.HiddenInput)
   


