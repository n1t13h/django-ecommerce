from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Cart
from products.models import Product
from django.contrib import messages
from billing.models import BillingProfile

from orders.models import Order
def cart_home(request):
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    context = {}
    cart_products = cart_obj.products.all()
    context['cart_products'] = cart_products
    context['cart'] = cart_obj
    
    return render(request,"cart/index.html",context)

def cart_update(request):
    product_id = request.POST.get("id")
    obj = Product.objects.get(id=product_id)
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    if obj in cart_obj.products.all():
        cart_obj.products.remove(obj)
        messages.error(request,obj.title+" Removed From Cart")
    else:
        cart_obj.products.add(obj)
        messages.success(request,obj.title+" Added to Cart")

    request.session['cart_item'] = cart_obj.products.count()
    print(obj.get_absolute_url())
    return redirect(request.META['HTTP_REFERER'])
   
def checkout_home(request):
    cart_obj,cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    
    user = request.user
    billing_profile=None
  
    if user.is_authenticated:
        billing_profile,billing_profile_created = BillingProfile.objects.get_or_create(user=user,email=user.email)
        order_qs = Order.objects.filter(cart=cart_obj,active=True)
        if order_qs.exists():
            order_qs.update(active=False)
        else:
            order_obj,new_order_obj = Order.objects.get_or_create(cart=cart_obj,billing_profile=billing_profile)


    return render(request,"cart/checkout.html",{"order":order_obj,'billing_profile':billing_profile})
