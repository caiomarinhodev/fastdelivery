#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from app.mixins.CustomContextMixin import DashboardMixin, ListMotoristasMixin, DashboardListMixin
from app.models import ConfigAdmin, Estabelecimento, Grupo, Produto, Opcional, Categoria, FotoProduto

"""HomeView.py: Especifica a pagina inicial da aplicacao."""

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class AppView(TemplateView):
    template_name = 'entrega/page/index.html'


class CollectView(TemplateView):
    template_name = 'entrega/page/collect.html'


class ContributeView(TemplateView):
    template_name = 'entrega/page/contribute.html'


class DashboardListPedidosView(LoginRequiredMixin, TemplateView, DashboardListMixin):
    login_url = '/login/'
    template_name = 'entrega/admin/list_pedidos.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/login')
        return super(DashboardListPedidosView, self).get(request, *args, **kwargs)


class DashboardDataView(LoginRequiredMixin, TemplateView, DashboardMixin):
    login_url = '/login/'
    template_name = 'entrega/admin/dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/login')
        return super(DashboardDataView, self).get(request, *args, **kwargs)


class ListMotoristasView(LoginRequiredMixin, TemplateView, ListMotoristasMixin):
    login_url = '/login/'
    template_name = 'entrega/admin/list_motoristas.html'


def set_feriado_admin(request):
    config = ConfigAdmin.objects.first()
    config.is_feriado = not config.is_feriado
    config.save()
    return redirect('/app/dashboard/')


def copy_group(request):
    data = request.GET
    print(data)
    try:
        grupo_origem = Grupo.objects.filter(identificador=data['grupo']).first()
        produto_destino = Produto.objects.get(id=data['produto'])
        grupo = Grupo(identificador=grupo_origem.identificador, titulo=grupo_origem.titulo,
                      limitador=grupo_origem.limitador,
                      produto=produto_destino,
                      obrigatoriedade=grupo_origem.obrigatoriedade, tipo=grupo_origem.tipo,
                      disponivel=grupo_origem.disponivel)
        grupo.save()
        for opc in grupo_origem.opcional_set.all():
            new_opc = Opcional(nome=opc.nome, descricao=opc.descricao, valor=opc.valor, disponivel=opc.disponivel,
                               grupo=grupo)
            new_opc.save()
        messages.success(request, 'Grupo copiado com sucesso')
    except (Exception,):
        messages.error(request, 'Erro ao copiar grupo')
    return redirect('/app/dashboard/')


def copy_catalogo(request):
    data = request.GET
    try:
        loja_origem = Estabelecimento.objects.get(id=data['origem'])
        loja_destino = Estabelecimento.objects.get(id=data['destino'])
        for categoria in loja_origem.categoria_set.all():
            new_cat = Categoria(nome=categoria.nome, disponibilidade=categoria.disponibilidade,
                                estabelecimento=loja_destino)
            new_cat.save()
            for produto in categoria.produto_set.all():
                new_prod = Produto(nome=produto.nome, descricao=produto.descricao, preco_base=produto.preco_base,
                                   disponivel=produto.disponivel, categoria=new_cat)
                new_prod.save()
                for grupo in produto.grupo_set.all():
                    new_grupo = Grupo(identificador=grupo.identificador, titulo=grupo.titulo, limitador=grupo.limitador,
                                      obrigatoriedade=grupo.obrigatoriedade, tipo=grupo.tipo, disponivel=grupo.disponivel,
                                      produto=new_prod)
                    new_grupo.save()
                    for opcional in grupo.opcional_set.all():
                        new_opc = Opcional(nome=opcional.nome, descricao=opcional.descricao, valor=opcional.valor,
                                           disponivel=opcional.disponivel,
                                           grupo=new_grupo)
                        new_opc.save()
                for foto in produto.fotoproduto_set.all():
                    new_foto = FotoProduto(url=foto.url, file=foto.file, produto=new_prod)
                    new_foto.save()
        messages.success(request, 'Catalogo copiado com sucesso')
    except (Exception,):
        messages.error(request, 'Erro ao copiar Catalogo')
    return redirect('/app/dashboard/')


def delete_group(request):
    data = request.GET
    grupo_origem = Grupo.objects.get(id=data['grupo'])
    try:
        grupo_origem.delete()
        messages.success(request, 'Grupo deletado com sucesso')
    except (Exception,):
        messages.error(request, 'Erro ao deletar Grupo')
    return redirect('/app/dashboard/')


def delete_catalogo(request):
    data = request.GET
    loja_origem = Estabelecimento.objects.get(id=data['origem'])
    try:
        for categoria in loja_origem.categoria_set.all():
            categoria.delete()
        messages.success(request, 'Catalogo deletado com sucesso')
    except (Exception,):
        messages.error(request, 'Erro ao deletar Catalogo')
    return redirect('/app/dashboard/')