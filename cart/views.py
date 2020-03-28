from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Cart
from products.models import Product

def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)
    context = {}
    cart_products = cart_obj.products.all()
    context['cart_products'] = cart_products
    context['cart'] = cart_obj
    
    return render(request,"cart/index.html",context)

def cart_update(request):
    product_id = request.POST.get("id")
    obj = Product.objects.get(id=product_id)
    cart_obj = Cart.objects.new_or_get(request)
    if obj in cart_obj.products.all():
        cart_obj.products.remove(obj)
    else:
        cart_obj.products.add(obj)
    request.session['cart_item'] = cart_obj.products.count()
    print(obj.get_absolute_url())
    return redirect(request.META['HTTP_REFERER'])
   
