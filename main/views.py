from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import NewUserForm,GuestForm
from django.utils.http import url_has_allowed_host_and_scheme,is_safe_url
from .models import GuestEmail
from django.conf import settings
# Create your views here.
def home_page(request):
    return render(request,"main/index.html",{})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"New Account Created :{username}")
            login(request,user)
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request,f"{msg}:{form.error_messages[msg]}")


    form = NewUserForm
    
    return render(request,'main/register.html',{"form":form})

def logout_request(request):
    logout(request)
    messages.info(request,"Logged Out Successfully")
    return redirect("main:homepage")

def login_request(request):
    if request.method=="POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f"Logged in as:{username}")
                return redirect("main:homepage")
            else:
                messages.error(request,"User Not Found!")
        
    form = AuthenticationForm()
    return render(request,"main/login.html",{"form":form})


def guest_login_view(request):
    form = GuestForm(request.POST or None)
    context = {
        'form':form
    }
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next or next_post
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id']=new_guest_email.id
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect("/")
    return redirect("/")
