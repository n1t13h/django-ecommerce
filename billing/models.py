from django.db import models
from django.conf import settings
# Create your models here.
from django.db.models.signals import post_save
User = settings.AUTH_USER_MODEL
from main.models import GuestEmail

class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        user=request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            obj,created = BillingProfile.objects.get_or_create(user=user,email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj,created = BillingProfile.objects.get_or_create(user=None,email=guest_email_obj.email)
        return obj,created
class BillingProfile(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,unique=True,on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects= BillingProfileManager()
    def __str__(self):
        return self.email


# def billing_profile_created_receiver(sender,instance,created,*args,**kwargs):
#     if created:
        

def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)
    
post_save.connect(user_created_receiver,sender=User)