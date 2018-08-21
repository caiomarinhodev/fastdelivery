#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.forms import FormPontoCliente
from app.mixins.CustomContextMixin import CustomContextMixin
from app.models import Ponto
from app.views.script_tools import logger


class ClientesListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Ponto
    context_object_name = 'clientes'
    template_name = 'entrega/clientes/list_clientes.html'

    def get(self, request, *args, **kwargs):
        now = datetime.now()
        if 'type' in self.request.GET:
            if self.request.GET['type'] == 'tudo':
                self.queryset = Ponto.objects.filter(Q(pedido__estabelecimento=self.request.user.estabelecimento) | Q(
                    estabelecimento=self.request.user.estabelecimento)).order_by(
                    '-created_at')
            elif self.request.GET['type'] == 'mes':
                self.queryset = Ponto.objects.filter(Q(pedido__estabelecimento=self.request.user.estabelecimento) | Q(
                    estabelecimento=self.request.user.estabelecimento), Q(created_at__month=now.month,
                                                                          created_at__year=now.year)).order_by(
                    '-created_at')
            else:
                self.queryset = Ponto.objects.filter(Q(pedido__estabelecimento=self.request.user.estabelecimento) | Q(
                    estabelecimento=self.request.user.estabelecimento), Q(created_at__month=now.month,
                                                                          created_at__year=now.year,
                                                                          created_at__day=now.day)).order_by(
                    '-created_at')
        else:
            self.queryset = Ponto.objects.filter(Q(pedido__estabelecimento=self.request.user.estabelecimento) | Q(
                estabelecimento=self.request.user.estabelecimento), Q(created_at__month=now.month,
                                                                      created_at__year=now.year)).order_by(
                '-created_at')

        return super(ClientesListView, self).get(request, *args, **kwargs)


class ClienteCreateView(LoginRequiredMixin, CreateView, CustomContextMixin):
    model = Ponto
    success_url = '/app/clientes/'
    form_class = FormPontoCliente
    template_name = 'entrega/clientes/cliente.html'

    def form_valid(self, form):
        loja = self.request.user.estabelecimento
        self.object = form.save()
        pto = self.object
        pto.estabelecimento = loja
        pto.save()
        try:
            logger(self.request.user, 'Criou um cliente')
        except:
            pass
        return super(ClienteCreateView, self).form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView, CustomContextMixin):
    model = Ponto
    success_url = '/app/clientes/'
    form_class = FormPontoCliente
    template_name = 'entrega/clientes/cliente.html'
