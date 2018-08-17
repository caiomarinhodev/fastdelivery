#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView

from app.models import Request
from app.views.mixins.Mixin import FocusMixin

"""HomeView.py: Especifica a pagina inicial da aplicacao."""

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class DashboardPedidosListView(LoginRequiredMixin, ListView, FocusMixin):
    login_url = '/loja/login/'
    template_name = 'painel/dashboard.html'
    model = Request
    context_object_name = 'pedidos'

    def get_queryset(self):
        return Request.objects.filter(estabelecimento=self.request.user.estabelecimento,
                                      endereco_entrega__isnull=False).order_by('-created_at')


class PrintView(LoginRequiredMixin, DetailView, FocusMixin):
    login_url = '/loja/login/'
    template_name = 'painel/print_pedido.html'
    model = Request
    context_object_name = 'pedido'
