from django.db import models
import os
from uuid import uuid4
from django.urls import reverse
# Create your models here.
def path_and_rename(instance, filename):
    upload_to = 'products'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class ProductManager(models.Manager):
    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)  
        if qs.count()==1:
            return qs.first()
        return None


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=2)
    image = models.ImageField(upload_to=path_and_rename, max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True)

    objects = ProductManager()

    class Meta:
        unique_together = ('title','slug')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
    