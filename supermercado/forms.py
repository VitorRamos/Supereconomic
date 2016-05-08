from django import forms
from models import *


class ClienteForm(forms.Form):
        nome = forms.CharField(max_length=45)
        senha = forms.CharField(max_length=45, widget=forms.PasswordInput())
        CPF = forms.CharField(max_length=45)