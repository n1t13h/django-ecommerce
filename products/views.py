from django.shortcuts import render , get_object_or_404
from .models import Product

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
    product = Product.objects.get(slug=slug)
    
    return render(request,"products/detail.html",{"product":product})