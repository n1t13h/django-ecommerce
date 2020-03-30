from django.shortcuts import render,redirect
from .forms import AddressForm
from .models import Address
from billing.models import BillingProfile
# Create your views here.
def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form':form
    }
    if form.is_valid():
        address_type = request.POST.get('address_type','shipping')
        instance = form.save(commit=False)
        billing_profile,billing_profile_created = BillingProfile.objects.new_or_get(request)
        instance.billing_profile = billing_profile
        instance.address_type = address_type
        instance.save()
        request.session[address_type+'_address_id'] = instance.id
        return redirect("cart:checkout")
    return redirect("cart:checkout")
    