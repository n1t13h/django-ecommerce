from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields = [
            # 'billing_profile',
            # 'address_type',
            'address_line1',
            'address_line2',
            'city',
            'country', 
            'state', 
            'postal_code' 
        ]