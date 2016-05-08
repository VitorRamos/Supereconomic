from __future__ import unicode_literals

from django.db import models


class Usuario(models.Model):
    idUsuario = models.IntegerField(primary_key=True, auto_created=True)
    nome = models.CharField(max_length=45)
    senha = models.CharField(max_length=45)


class Cliente(models.Model):
    idCliente = models.OneToOneField(Usuario, primary_key=True)
    CPF = models.CharField(max_length=45)


class Empresario(models.Model):
    idEmpresario= models.OneToOneField(Usuario, primary_key=True)
    CPF= models.CharField(max_length=45)


class Supermercado(models.Model):
    idSupermercado= models.IntegerField(primary_key=True, auto_created=True)
    nome= models.CharField(max_length=45)
    localizacao= models.CharField(max_length=255)


class Dono(models.Model):
    class Meta:
        unique_together = (("idEmpresaio", "idSupermercado"))
    idEmpresaio= models.ForeignKey(Empresario)
    idSupermercado= models.ForeignKey(Supermercado)


class Produto(models.Model):
    idProduto= models.IntegerField(primary_key=True, auto_created=True)
    nome= models.CharField(max_length=45)
    marca= models.CharField(max_length=45)


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
    idCliente = models.ForeignKey(Cliente)
    idProduto = models.ForeignKey(Produto)