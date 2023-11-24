# forms.py

from allauth.account.forms import SignupForm
from django import forms
from REST.models import Irrigatore

class IrrigatoreForm(forms.ModelForm):
    class Meta:
        model = Irrigatore
        fields = ['nome', 'latitudine', 'longitudine', 'quota']

""" 
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())   def save(self, request):
        user = super(CustomSignupForm, self).save(request)

        user.save()
        return user
 """