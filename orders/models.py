from django.db import models
from cart.models import Cart 
import math
from billing.models import BillingProfile
from addresses.models import Address
# Create your models here.
from django.db.models.signals import pre_save ,post_save
from ecommerce.utils import *
ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)
class OrderManager(models.Manager):
    def new_or_get(self,billing_profile,cart_obj):
        order_qs = self.get_queryset().filter(cart=cart_obj,billing_profile=billing_profile,active=True).exclude(status='paid')
        if order_qs.count()==1:
            order_obj = order_qs.first()
        else:
            order_obj = self.model.objects.create(cart=cart_obj,billing_profile=billing_profile)
        return order_obj
class Order(models.Model):
    order_id = models.CharField(max_length=120,blank=True)
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE,null=True,blank=True)
    # shipping_address
    # billing_address
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status = models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES,)
    shipping_total =  models.DecimalField(max_digits=20,decimal_places=2,default=50.0)
    shipping_address= models.ForeignKey(Address,null=True,related_name="shipping_address",blank=True,on_delete=models.CASCADE)
    billing_address= models.ForeignKey(Address,null=True,blank=True,name="billing_address",on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=20,decimal_places=2,default=0.0)
    active = models.BooleanField(default=True)
    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total ,shipping_total])
        formatted_total = format(new_total,'.2f')
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if billing_address and shipping_address and billing_profile and total > 0:
            return True
        return False
        
    def mark_done(self):
        if self.check_done():
            self.status='paid'
            self.save()
        return self.status






def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)
pre_save.connect(pre_save_create_order_id,sender=Order)

def post_save_cart_total(sender,instance,created,*args,**kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()
            
post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=Order)