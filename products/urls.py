from django.contrib import admin
from django.urls import path
from . import views
app_name="products"
urlpatterns = [
    path('',views.products_home,name="product_home"),
    path('<slug:slug>/',views.products_detail,name="product_detail"),
]
