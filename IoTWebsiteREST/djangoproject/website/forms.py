# forms.py

from allauth.account.forms import SignupForm
from django import forms
from REST.models import Irrigatore, CustomUser

class IrrigatoreForm(forms.ModelForm):
    class Meta:
        model = Irrigatore
        fields = ['nome', 'latitudine', 'longitudine', 'quota', 'attivo']

""" 
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())   def save(self, request):
        user = super(CustomSignupForm, self).save(request)

        user.save()
        return user
 """

from django import forms
from REST.models import Igrometro, MasterIgrometri

class IgrometroForm(forms.ModelForm):
    class Meta:
        model = Igrometro
        fields = ['nome', 'latitudine', 'longitudine', 'master']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default "-------" option for the 'master' field
        self.fields['master'].empty_label = None


class MasterForm(forms.ModelForm):
    class Meta:
        model = MasterIgrometri
        fields = ['nome', 'latitudine', 'longitudine', 'quota']

class SprinklerForm(forms.ModelForm):
    class Meta:
        model = Irrigatore
        fields = ['nome', 'longitudine', 'quota', 'attivo']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name']