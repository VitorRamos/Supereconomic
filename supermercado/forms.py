from django import forms
from models import *


class CadastroForm(forms.Form):
    nome = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder": "Usuario"}))
    senha = forms.CharField(max_length=45, label= "",
                            widget=forms.TextInput(attrs={"placeholder":"Senha", "type":"password"}))
    CPF = forms.CharField(max_length=45, label="",
                          widget=forms.TextInput(attrs={"placeholder": "CPF"}))


class LoginForm(forms.Form):
    nome = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder":"Usuario"}))
    senha = forms.CharField(max_length=45, label="",
                            widget=forms.TextInput(attrs={"placeholder":"Senha", "type":"password"}))


class CadastroProd(forms.Form):
    nome = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder": "Produto"}))
    marca = forms.CharField(max_length=45, label="",
                            widget=forms.TextInput(attrs={"placeholder": "Marca"}))
    preco= forms.FloatField()
    quantidade= forms.IntegerField()


class CadastroDono(forms.Form):
    nome = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder": "Usuario"}))
    senha = forms.CharField(max_length=45, label="",
                            widget=forms.TextInput(attrs={"placeholder": "Senha","type":"password"}))
    CNPJ = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder": "CNPJ"}))
    nomeSupermercado = forms.CharField(max_length=45, label="",
                                       widget=forms.TextInput(attrs={"placeholder": "Supermercado"}))
    localizacao = forms.CharField(max_length=255, label="",
                                  widget=forms.TextInput(attrs={"placeholder": "Localizacao"}))
