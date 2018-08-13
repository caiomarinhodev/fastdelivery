#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from app.models import Estabelecimento, Produto, Grupo
from app.views.mixins.Mixin import LojaFocusMixin


class ListLojas(LoginRequiredMixin, ListView, LojaFocusMixin):
    login_url = '/aplicativo/login/'
    template_name = 't_app/lojas.html'
    context_object_name = 'lojas'
    model = Estabelecimento

    def get_context_data(self, **kwargs):
        kwargs['lojas_off'] = Estabelecimento.objects.filter(is_online=False, is_approved=True).order_by('?')
        return super(ListLojas, self).get_context_data(**kwargs)

    def get_queryset(self):
        est = Estabelecimento.objects.filter(is_online=True, is_approved=True).order_by('?')
        return est


class ListProducts(DetailView, LojaFocusMixin):
    template_name = 't_app/produtos.html'
    context_object_name = 'loja'
    model = Estabelecimento
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.request.session['lojaid'] = self.get_object().pk
        return super(ListProducts, self).get(request, *args, **kwargs)


# Class para ver os opcionais do grupo do produto selecionado
class GroupView(DetailView, LojaFocusMixin):
    template_name = ''
    context_object_name = 'grupo'
    model = Grupo
    pk_url_kwarg = 'pk'
