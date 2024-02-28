from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns=[
    path('admin/login/', views.logins, name='login'),
    path('',views.Home.as_view(),name='home'),
    path('checkout/',views.Checkout.as_view(),name='checkout'),
    path('product/<slug>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('add_to_cart/<slug>/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<slug>',views.remove_from_cart,name='remove_from_cart'),
    # path('wishlist',views.wishlists,name='wishlist'),
    path('gallery',views.gallery,name='gallery'),
    path('myaccount',views.myaccount,name='my_account'),
    path('products',views.products,name='products'),
    # path('product_detail',views.ProductDetailView.as_views(),name='product_detail'),
    path('register/',views.register,name='register'),
    path('login/',views.logins,name='login'),
    path('logout',views.account_logout,name='logout'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('order_summery',views.OrderSummeryView.as_view(),name='order_summery'),
    path('remove_single_item_from_cart/<slug>/',views.remove_single_item_from_cart,name='remove_single_item_from_cart'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('payment/<payment_method>/',views.Payment.as_view(),name="payment"),
    path('payments/',views.payment,name="payments"),
    # path('payment/<payment_method>/payments',views.payment,name="payments"),
    path('add_coupon/',views.Add_Coupon.as_view(),name="add_coupon"),
    path('request_refund/',views.Refund_Requests.as_view(),name='request_refund'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe/success/', views.subscribe_success, name='subscribe_success'),
    path('add-to-wishlist/<slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)