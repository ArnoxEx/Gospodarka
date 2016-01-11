from Gospodarka.gospodarkaApp.models import *
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UsrForm(forms.ModelForm):
    class Meta:
        model = Usr
        fields = ('phone',)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('city', 'street', 'numb', 'postal_code',)

class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name',)
