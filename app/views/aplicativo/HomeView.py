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


# Paginar os grupos de um determinado produto, e a medida que o usuario seleciona um item, o
# sistema guarda o item(s) escolhidos daquele grupo e ao fim da paginacao, mostrar botao adicionar ao carrinho.
# Caso não haja grupos nem opcionais, mostrar direto o botao, e ir para o carrinho ao final.

# page_number, paginator.num_pages, page, page_range

# No Carrinho, implementar 2 botoes, finalizar pedido e continuar comprando. Para continuar comprando, voltar para a
# loja, e em finaizar pedido, navegar para tela de cadastro ou selecao de enderecos -> forma de pagamento -> acompanhar.

# Class para ver os opcionais do grupo do produto selecionado
class GroupListView(ListView, LojaFocusMixin):
    template_name = ''
    paginate_by = 1
    context_object_name = 'grupo'
    model = Grupo
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return Grupo.objects.filter(produto_id=self.kwargs.get(self.page_kwarg))
