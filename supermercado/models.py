from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Supermercado(models.Model):
    idSupermercado= models.AutoField(primary_key=True, auto_created=True)
    nome= models.CharField(max_length=45)
    localizacao= models.CharField(max_length=255)


class Dono(models.Model):
    class Meta:
        unique_together = (("idEmpresario", "idSupermercado"))
    idEmpresario = models.ForeignKey(User)
    idSupermercado = models.ForeignKey(Supermercado)
    CNPJ= models.CharField(max_length=45)


class Produto(models.Model):
    idProduto= models.AutoField(primary_key=True, auto_created=True)
    nome= models.CharField(max_length=45)
    marca= models.CharField(max_length=45)
    tipo= models.CharField(max_length=45)


class Possui(models.Model):
    class Meta:
        unique_together = (("idSupermercado", "idProduto"))
    idSupermercado = models.ForeignKey(Supermercado)
    idProduto = models.ForeignKey(Produto)
    quantidade = models.IntegerField()
    preco = models.FloatField()


class Favorito(models.Model):
    class Meta:
        unique_together = (("idCliente", "idProduto"))
    idCliente = models.ForeignKey(User)
    idProduto = models.ForeignKey(Produto)