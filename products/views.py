from django.shortcuts import render , get_object_or_404
from .models import Product
from cart.models import Cart
def products_home(request):
    return render(request,"products/index.html",{"products":Product.objects.all()})
def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {'query':q,'products':products}
        template='products/index.html'
    else:
        template ="main/index.html"
        context = {}
    return render(request,template,context)

def products_detail(request,slug):
    
    cart_obj = Cart.objects.new_or_get(request)
    product = Product.objects.get(slug=slug)
    context = {}
    context['product'] = product
    context['cart'] = cart_obj

    return render(request,"products/detail.html",context)