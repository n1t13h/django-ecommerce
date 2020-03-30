from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Cart
from products.models import Product
from django.contrib import messages
from billing.models import BillingProfile
from addresses.forms import AddressForm
from orders.models import Order
from django.contrib.auth.forms import AuthenticationForm
from main.forms import GuestForm
from main.models import GuestEmail
from addresses.models import Address

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
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    user = request.user
    address_form = AddressForm()
    billing_address_form = AddressForm()
    guestform = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    billing_profile,billing_profile_created = BillingProfile.objects.new_or_get(request)
    order_obj = Order.objects.new_or_get(billing_profile=billing_profile,cart_obj=cart_obj)

    shipping_id = request.session.get('shipping_address_id',None)
    billing_id = request.session.get('billing_address_id',None)

    if shipping_id:
        order_obj.shipping_address = Address.objects.get(id=shipping_id)
        del request.session['shipping_address_id']
    if billing_id:
        order_obj.billing_address = Address.objects.get(id=billing_id)
        del request.session['billing_address_id']

    if billing_id or shipping_id:
        order_obj.save()

    if request.method=="POST":
        if order_obj.check_done():
            order_obj.mark_done()
            del request.session['cart_id']
        return  redirect('cart:success')
    
    context = {
        "order":order_obj,
        'billing_profile':billing_profile,
        'address_form':address_form,
        'billing_address_form':billing_address_form,
        'guestform':guestform
    }

    return render(request,"cart/checkout.html",context)



def success(request):
    return render(request,"cart/success.html",{})