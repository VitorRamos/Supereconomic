from django import forms
from models import *


class CadastroForm(forms.Form):
    nome = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder": "Usuario", "class": "form-control"}))
    senha = forms.CharField(max_length=45, label= "",
                            widget=forms.TextInput(attrs={"placeholder":"Senha", "type":"password", "class": "form-control"}))
    CPF = forms.CharField(max_length=45, label="",
                          widget=forms.TextInput(attrs={"placeholder": "CPF", "class": "form-control"}))


class LoginForm(forms.Form):
    nome = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder":"Usuario", "class": "form-control"}))
    senha = forms.CharField(max_length=45, label="",
                            widget=forms.TextInput(attrs={"placeholder":"Senha", "class": "form-control", "type":"password"}))

TIPOS = (
    ('', 'Selecione...'),
    ('alimento', 'Alimento'),
    ('limpeza', 'Limpeza'),
    ('eletronico', 'Eletronico'),
    ('brinquedo', 'Brinquedo'),
)

class CadastroProd(forms.Form):
    nome = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder": "Produto", "class": "form-control"}))
    marca = forms.CharField(max_length=45, label="",
                            widget=forms.TextInput(attrs={"placeholder": "Marca", "class": "form-control"}))
    preco= forms.FloatField(label="",
                            required="true",
                            min_value=0,
                            widget=forms.NumberInput(attrs={"placeholder": "Preco", "step": "0.01", "class": "form-control form-control-2 col-lg-6 col-xs-6 col-sm-6 col-ms-6"}))
    quantidade= forms.IntegerField(label="",
                                   required="true",
                                   min_value=0,
                                   widget=forms.NumberInput(attrs={"placeholder": "Quantidade", "class": "form-control form-control-2 col-lg-6 col-xs-6 col-sm-6 col-ms-6 pull-right margin-bottom10px"}))
    tipo = forms.ChoiceField(label="",
                             choices=TIPOS,
                             required=True,
                             widget=forms.Select(attrs={"class": "form-control"}))


class CadastroDono(forms.Form):
    nome = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder": "Usuario", "class": "form-control margin-bottom10px"}))
    senha = forms.CharField(max_length=45, label="",
                            widget=forms.TextInput(attrs={"placeholder": "Senha","type":"password", "class": "form-control form-control-2 col-lg-6 col-xs-6 col-sm-6 col-md-6"}))
    CNPJ = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder": "CNPJ", "class": "form-control form-control-2 col-lg-6 col-xs-6 col-md-6 col-sm-6 pull-right margin-bottom10px"}))
    nomeSupermercado = forms.CharField(max_length=45, label="",
                                       widget=forms.TextInput(attrs={"placeholder": "Supermercado", "class": "form-control"}))
    localizacao = forms.CharField(max_length=255, label="",
                                  widget=forms.TextInput(attrs={"placeholder": "Localizacao", "class": "form-control"}))


class PesquisaProd(forms.Form):
    nome = forms.CharField(max_length=45, label="", required=False,
                           widget=forms.TextInput(attrs={"placeholder": "Nome", "class": "form-control"}))
    marca = forms.CharField(max_length=45, label="", required=False,
                            widget=forms.TextInput(attrs={"placeholder": "Marca", "class": "form-control"}))
    precoMin = forms.FloatField(label="",
                            min_value=0, required=False,
                            widget=forms.NumberInput(attrs={"placeholder": "Min", "step": "0.01", "class": "form-control form-control-2 col-lg-6 col-xs-6 col-sm-6 col-ms-6"}))
    precoMax = forms.FloatField(label="",
                                min_value=0, required=False,
                                widget=forms.NumberInput(attrs={"placeholder": "Max", "step": "0.01",
                                                                "class": "form-control form-control-2 col-lg-6 col-xs-6 col-sm-6 col-ms-6 pull-right margin-bottom15px"}))
    tipo = forms.ChoiceField(label="",
                             choices=TIPOS, required=False,
                             widget=forms.Select(attrs={"class": "form-control"}))
