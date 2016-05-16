from django import forms
from models import *


class CadastroForm(forms.Form):
        nome = forms.CharField(max_length=45)
        senha = forms.CharField(max_length=45, widget=forms.PasswordInput())
        CPF = forms.CharField(max_length=45, label="CPF")

class LoginForm(forms.Form):
        nome = forms.CharField(max_length=45)
        senha = forms.CharField(max_length=45, widget=forms.PasswordInput())

class CadastroProd(forms.Form):
        nome = forms.CharField(max_length=45)
        marca = forms.CharField(max_length=45)

class CadastroDono(forms.Form):
        nome = forms.CharField(max_length=45)
        senha = forms.CharField(max_length=45, widget=forms.PasswordInput())
        CNPJ = forms.CharField(max_length=45, label="CNPJ")
        nomeSupermercado = forms.CharField(max_length=45, label="Supermercado")
        localizacao = forms.CharField(max_length=255, label="Localizacao")
