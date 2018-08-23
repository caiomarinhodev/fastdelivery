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

    def get(self, request, *args, **kwargs):
        if 'checks' in self.request.session:
            self.request.session['checks'] = []
        return super(ListLojas, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['lojas_off'] = Estabelecimento.objects.filter(is_online=False, is_approved=True).order_by('?')
        return super(ListLojas, self).get_context_data(**kwargs)

    def get_queryset(self):
        est = Estabelecimento.objects.filter(is_online=True, is_approved=True).order_by('?')
        return est


class ListProducts(LoginRequiredMixin, DetailView, LojaFocusMixin):
    template_name = 't_app/produtos.html'
    context_object_name = 'loja'
    model = Estabelecimento
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.request.session['lojaid'] = self.get_object().pk
        return super(ListProducts, self).get(request, *args, **kwargs)


# Paginar os grupos de um determinado produto (OK), e a medida que o usuario seleciona um item, o
# sistema guarda o item(s) escolhidos daquele grupo (OK) e ao fim da paginacao, mostrar botao adicionar ao carrinho. (OK)
# Caso não haja grupos nem opcionais, mostrar direto o botao, e ir para o carrinho ao final.

# page_number, paginator.num_pages, page, page_range

# No Carrinho, implementar 2 botoes,(OK) finalizar pedido e continuar comprando.(OK) Para continuar comprando, voltar para a
# loja,(OK) e em finaizar pedido, navegar para tela de cadastro ou selecao de enderecos -> forma de pagamento -> acompanhar.

# Class para ver os opcionais do grupo do produto selecionado

class ProductView(LoginRequiredMixin, DetailView, LojaFocusMixin):
    template_name = 't_app/product-detail.html'
    context_object_name = 'produto'
    model = Produto
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.request.session['produto'] = self.get_object().pk
        if 'checks' in self.request.session:
            self.request.session['checks'] = []
        return super(ProductView, self).get(request, *args, **kwargs)


class ChooseGroupListView(LoginRequiredMixin, LojaFocusMixin, ListView):
    context_object_name = 'grupos'
    model = Grupo
    template_name = 't_app/choose_group.html'
    ordering = '-created_at'
    paginate_by = 1
    page_kwarg = 'page'

    def insert_in_session(self, array):
        check_session = self.request.session['checks']
        for e in array:
            if e not in check_session:
                check_session.append(e)
        self.request.session['checks'] = check_session

    def get(self, request, *args, **kwargs):
        if self.kwargs.get(self.page_kwarg) == '1':
            self.request.session['checks'] = []
        if 'checks' in self.request.session:
            if 'checks' in request.GET:
                self.insert_in_session(request.GET.getlist('checks'))
                print(self.request.session['checks'])
        else:
            self.request.session['checks'] = []
        return super(ChooseGroupListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Paginate the queryset, if needed.
        """
        pk = self.kwargs['pk']
        queryset = Produto.objects.get(id=pk).grupo_set.order_by('created_at').filter(disponivel=True)
        return queryset
