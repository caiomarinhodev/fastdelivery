#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, RedirectView, DetailView

from app.models import ItemPedido, Opcional, OpcionalChoice, Cliente, Request, Estabelecimento, Produto, Endereco, \
    Bairro, FormaPagamento, FormaEntrega, Notificacao
from app.views.mixins.Mixin import LojaFocusMixin


def check_same_store(id_loja, pedido):
    if int(id_loja) == int(pedido.estabelecimento.id):
        return True
    return False


def get_item_pedido_default(pedido, produto, obs):
    itempedido = ItemPedido(pedido=pedido, quantidade='1', produto=produto, observacoes=obs)
    itempedido.save()


def insert_optionals_item_pedido(checks, itempedido=None):
    for id in checks:
        opc = Opcional.objects.get(id=id)
        opcc = OpcionalChoice(opcional=opc, item_pedido=itempedido)
        opcc.save()
    itempedido.save()


def cria_item_pedido(checks, pedido, produto, obs):
    itempedido = ItemPedido(pedido=pedido, quantidade='1', produto=produto, observacoes=obs)
    itempedido.save()
    for id in checks:
        opc = Opcional.objects.get(id=id)
        opcc = OpcionalChoice(opcional=opc, item_pedido=itempedido)
        opcc.save()
    itempedido.save()


def is_logged(request):
    try:
        if request.user:
            cliente = Cliente.objects.get(usuario=request.user)
            if cliente:
                return True
            else:
                return False
        else:
            return False
    except (Exception,):
        return False


def get_pedido(request, id_loja):
    try:
        req = Request.objects.get(id=request.session['pedido'])
        try:
            cliente = request.user.cliente
        except:
            cliente = None
        req.cliente = cliente
        req.save()
        return req
    except (Exception,):
        estabelecimento = Estabelecimento.objects.get(id=id_loja)
        try:
            cliente = request.user.cliente
        except:
            cliente = None
        pedido = Request(cliente=cliente, estabelecimento=estabelecimento)
        pedido.save()
        request.session['pedido'] = pedido.id
        return pedido


def add_cart(request, id_loja):
    checks = request.POST.getlist('checks')
    if is_logged(request):
        pedido = get_pedido(request, id_loja)
        if check_same_store(id_loja, pedido) and ('produto' in request.POST):
            produto = Produto.objects.get(id=request.POST['produto'])
            obrigatorios = produto.grupo_set.filter(obrigatoriedade=True)
            if check_required_selected(checks, obrigatorios) or obrigatorios.count() == 0:
                obs = request.POST['observacoes']
                cria_item_pedido(checks, pedido, produto, obs)
            else:
                messages.error(request, u'Você deve selecionar 1 item das opcoes com *(asterisco)')
                return redirect('/loja/' + str(pedido.estabelecimento.id))
        else:
            messages.error(request, u'Você deve comprar produtos no mesmo estabelecimento')
            return redirect('/loja/' + str(pedido.estabelecimento.id))
        pedido.save()
        return redirect('/loja/' + str(pedido.estabelecimento.id))
    pedido = get_pedido(request, id_loja)
    if check_same_store(id_loja, pedido) and ('produto' in request.POST):
        produto = Produto.objects.get(id=request.POST['produto'])
        obrigatorios = produto.grupo_set.filter(obrigatoriedade=True)
        if check_required_selected(checks, obrigatorios) or obrigatorios.count() == 0:
            obs = request.POST['observacoes']
            cria_item_pedido(checks, pedido, produto, obs)
        else:
            messages.error(request, u'Você deve selecionar 1 item das opcoes com *(asterisco)')
            return redirect('/loja/' + str(pedido.estabelecimento.id))
    pedido.save()
    messages.error(request, u'Para fazer um pedido você deve estar logado')
    return redirect('/define/login/')


def remove_cart(request, pk):
    pedido = Request.objects.get(id=request.session['pedido'])
    id_loja = pedido.estabelecimento.id
    del request.session['pedido']
    pedido.delete()
    messages.success(request, 'Pedido deletado com sucesso')
    return redirect('/loja/' + str(id_loja))  # redirecionar para a loja


def check_required_selected(checks, list):
    count = 0
    for group in list:
        if group:
            for check in checks:
                opc = Opcional.objects.filter(id=check).first()
                if opc.grupo.id == group.id:
                    count += 1
    return (int(count) >= int(list.count()))


def check_loja_is_online(request):
    loja = Request.objects.get(id=request.session['pedido']).estabelecimento
    return loja.is_online


class FinalizaRequest(LoginRequiredMixin, TemplateView, LojaFocusMixin):
    template_name = 'loja/finaliza_pedido.html'
    login_url = '/define/login/'

    def get(self, request, *args, **kwargs):
        if not check_loja_is_online(self.request):
            messages.error(self.request, u'A Loja não está mais online para receber pedidos.')
            return redirect('/')
        return super(FinalizaRequest, self).get(request, *args, **kwargs)


class CarrinhoReqView(LoginRequiredMixin, TemplateView, LojaFocusMixin):
    template_name = 'loja/carrinho.html'
    login_url = '/define/login/'

    def get(self, request, *args, **kwargs):
        return super(CarrinhoReqView, self).get(request, *args, **kwargs)


def submit_pedido(request):
    data = request.POST
    endereco = None
    try:
        cliente = request.user.cliente
        pedido = Request.objects.get(id=request.session['pedido'])
        pedido.cliente = cliente
    except (Exception,):
        messages.error(request, 'Faça Login para finalizar o pedido')
        return redirect('/define/login/')
    try:
        if 'endereco' in data:
            if data['endereco'] != '':
                endereco = Endereco.objects.get(id=data['endereco'])
                endereco.save()
        else:
            if ('bairro' in data) and ('rua' in data) and ('numero' in data) and ('complemento' in data):
                if (data['bairro'] != u'') and (data['rua'] != u'' and (data['numero'] != u'')):
                    bairro = Bairro.objects.get(id=data['bairro'])
                    endereco = Endereco(cliente=cliente, bairro=bairro, endereco=data['rua'], numero=data['numero'],
                                        complemento=data['complemento'])
                    endereco.save()
                else:
                    messages.error(request, u'Nao conseguimos cadastrar seu endereco')
                    return redirect('/finaliza-pedido/')
            else:
                messages.error(request, u'Selecione o endereco de entrega ou Informe o endereco de entrega')
                return redirect('/finaliza-pedido/')
    except (Exception,):
        messages.error(request, u'Selecione o endereco de entrega ou Informe o endereco de entrega')
        return redirect('/finaliza-pedido/')
    try:
        if 'pgto' in data:
            if data['pgto'] != u'':
                forma_pagamento = FormaPagamento.objects.get(id=data['pgto'])
            else:
                messages.error(request, u'Insira uma forma de pagamento')
                return redirect('/finaliza-pedido/')
        else:
            messages.error(request, u'Insira uma forma de pagamento')
            return redirect('/finaliza-pedido/')
    except (Exception,):
        messages.error(request, u'Insira uma forma de pagamento')
        return redirect('/finaliza-pedido/')
    try:
        pedido.troco = data['troco']
    except (Exception,):
        pass
    try:
        pedido.forma_pagamento = forma_pagamento
        if endereco:
            pedido.endereco_entrega = endereco
        else:
            messages.error(request, u'Selecione o endereco de entrega ou Informe o endereco de entrega')
            return redirect('/finaliza-pedido/')
        pedido.save()
        messages.success(request, 'Pedido Realizado com Sucesso')
        message = make_message(pedido)
        n = Notificacao(type_message='NOVO_PEDIDO', to=pedido.estabelecimento.user, message=message, pedido=pedido)
        n.save()
    except (Exception,):
        messages.error(request, u'Selecione o endereco de entrega ou Informe o endereco de entrega')
        return redirect('/finaliza-pedido/')
    return redirect('/acompanhar-pedido/' + str(pedido.pk))


def make_message(pedido):
    try:
        message = 'Cliente: ' + str(pedido.cliente.usuario.first_name) + u' ' + str(
            pedido.cliente.usuario.last_name) + ' ' + 'Telefone: ' + str(
            pedido.cliente.telefone) + ' ' + 'Pedido:' + ' '
        for it in pedido.itempedido_set.all():
            message += ' ' + str(it.produto.nome) + '('
            for opc in it.opcionalchoice_set.all():
                message += str(opc.opcional.nome) + ','
            message += ') '
        return message
    except (Exception,):
        message = 'Cliente: ' + unicode(pedido.cliente.usuario.first_name) + u' ' + unicode(
            pedido.cliente.usuario.last_name) + ' ' + 'Telefone: ' + str(
            pedido.cliente.telefone) + ' ' + 'Pedido:' + ' '
        for it in pedido.itempedido_set.all():
            message += ' ' + unicode(it.produto.nome) + '('
            for opc in it.opcionalchoice_set.all():
                message += unicode(opc.opcional.nome) + ','
            message += ') '
        return message


class AcompanharRequest(LoginRequiredMixin, DetailView):
    template_name = 'loja/acompanha_pedido.html'
    login_url = '/define/login/'
    model = Request
    context_object_name = 'pedido_obj'

    def get(self, request, *args, **kwargs):
        if 'pedido' in self.request.session:
            del self.request.session['pedido']
        return super(AcompanharRequest, self).get(request, *args, **kwargs)


class MeusRequests(LoginRequiredMixin, TemplateView, LojaFocusMixin):
    template_name = 'loja/meus_pedidos.html'
    login_url = '/define/login/'
