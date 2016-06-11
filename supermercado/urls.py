"""projetoPDS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required, permission_required

from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^cadastro/$', cadastro, name='cadastro'),
    url(r'^cadastroDono/$', cadastroDono, name='dono'),
    url(r'^produtos/$', produtos, name='produtos'),
    url(r'^favoritos/$', favoritos, name='favoritos'),
    url(r'^carrinho/$', carrinho, name='carrinho'),
    url(r'^pesquisa/$', pesquisa, name='pesquisa'),
    url(r'^sobre/$', sobre, name='sobre')
]
