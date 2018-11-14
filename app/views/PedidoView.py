#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.forms import PontoFormSet, PontoFormUpdateSet
from app.mixins.CustomContextMixin import RedirectMotoristaOcupadoView, CustomContextMixin
from app.models import Pedido, Estabelecimento, Motorista, Notification, Ponto, Classification, Bairro
from app.views.fcm import func
from app.views.snippet_template import render_block_to_string
from app.views.script_tools import logger


class CozinhaListView(LoginRequiredMixin, RedirectMotoristaOcupadoView, ListView, CustomContextMixin):
    login_url = '/login/'
    context_object_name = 'rotas'
    template_name = 'entrega/acompanhar/view_cozinha.html'

    def get_queryset(self):
        return Pedido.objects.filter(coletado=False, estabelecimento=self.request.user.estabelecimento,
                                     btn_finalizado=False).order_by(
            '-created_at')


def set_to_prepared_pedido(request, id_ponto):
    if not request.user.is_authenticated:
        messages.error(request, "Usuario precisa estar logado para esta operacao")
        raise PermissionDenied("Usuario precisa estar logado para esta operacao")
    else:
        ponto = Ponto.objects.get(id=id_ponto)
        pedido = ponto.pedido
        try:
            reqs = pedido.request_set.all()
            for req in reqs:
                req.status_pedido = 'PREPARANDO'
                req.save()
        except (Exception,):
            pass
        ponto.is_prepared = True
        pedido.save()
        ponto.save()
        try:
            logger(request.user, 'setou para preparar o pedido')
        except:
            pass
        return HttpResponseRedirect('/app/cozinha/')

def select_motoboy_fixo_painel(request, pk):
    id_motorista = request.GET['motoboy']
    print(id_motorista)
    motorista = Motorista.objects.get(id=id_motorista)
    pedido = Pedido.objects.get(id=pk)
    if pedido.motorista:
        try:
            messages.error(request,
                           'O motorista ' + pedido.motorista.first_name + ' pegou esta entrega antes de você')
        except (Exception,):
            messages.error(request, 'Outro Motorista pegou esta entrega antes de você')
        return HttpResponseRedirect('/app/pedidos/motorista/')
    else:
        a = func()
        pedido.status = False
        pedido.motorista = motorista.user
        pedido.save()
        motorista.ocupado = True
        motorista.save()
        try:
            logger(request.user, "Aceitou fazer a Rota #" + str(pedido.pk))
        except (Exception,):
            pass
    return redirect('/app/pedidos/loja')


def select_motoboy_fixo_cozinha(request, pk):
    id_motorista = request.GET['motoboy']
    print(id_motorista)
    motorista = Motorista.objects.get(id=id_motorista)
    pedido = Pedido.objects.get(id=pk)
    if pedido.motorista:
        try:
            messages.error(request,
                           'O motorista ' + pedido.motorista.first_name + ' pegou esta entrega antes de você')
        except (Exception,):
            messages.error(request, 'Outro Motorista pegou esta entrega antes de você')
        return HttpResponseRedirect('/app/pedidos/motorista/')
    else:
        a = func()
        pedido.status = False
        pedido.motorista = motorista.user
        pedido.save()
        motorista.ocupado = True
        motorista.save()
        try:
            logger(request.user, "Aceitou fazer a Rota #" + str(pedido.pk))
        except (Exception,):
            pass
    return redirect('/app/cozinha')


@require_http_methods(["GET"])
def liberar_corrida_cozinha(request, pk_pedido):
    pedido = Pedido.objects.get(id=pk_pedido)
    pedido.coletado = True
    pedido.status_cozinha = True
    pedido.save()
    try:
        if pedido.request_set.first():
            reqs = pedido.request_set.all()
            for req in reqs:
                req.status_pedido = 'ENTREGANDO'
                req.save()
    except (Exception,):
        pass
    if Motorista.objects.get(user=pedido.motorista).is_online:
        message = "Voce foi liberado pela loja para realizar a(s) entrega(s). Sua Rota atual esta no menu ENTREGAS. Quando terminar uma entrega, marque finalizar. Qualquer problema, ligue para a loja: " + pedido.estabelecimento.phone
        n = Notification(type_message='ENABLE_ROTA', to=pedido.motorista, message=message)
        n.save()
    try:
        logger(request.user, "Liberou a rota pela cozinha. A Rota #" + str(pedido.pk))
    except (Exception,):
        pass
    return redirect('/app/cozinha')


class OrderMotoristaDetailView(LoginRequiredMixin, DetailView, CustomContextMixin):
    model = Pedido
    template_name = 'entrega/acompanhar/order_view.html'
    context_object_name = 'pedido'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super(OrderMotoristaDetailView, self).get(request, *args, **kwargs)
        except:
            messages.error(request, 'Este pedido foi cancelado pela loja')
            return HttpResponseRedirect('/app/pedidos/motorista/')


class RouteMotoristaDetailView(LoginRequiredMixin, DetailView, CustomContextMixin):
    model = Pedido
    template_name = 'entrega/acompanhar/route_view.html'
    context_object_name = 'pedido'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super(RouteMotoristaDetailView, self).get(request, *args, **kwargs)
        except:
            messages.error(request, 'Este pedido foi cancelado pela loja')
            return HttpResponseRedirect('/app/pedidos/motorista/')


class MapRouteMotoristaView(LoginRequiredMixin, DetailView, CustomContextMixin):
    model = Pedido
    template_name = 'entrega/acompanhar/map_view.html'
    context_object_name = 'pedido'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super(MapRouteMotoristaView, self).get(request, *args, **kwargs)
        except:
            messages.error(request, 'Este pedido foi cancelado pela loja')
            return HttpResponseRedirect('/app/pedidos/motorista/')


class PedidosLojaListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Pedido
    # permission_required = ('app.view_dashboard_1', 'app.view_dashboard_2', 'app.view_dashboard_3', )
    context_object_name = 'pedidos'
    template_name = 'entrega/pedidos/list_pedidos_loja.html'

    def get(self, request, *args, **kwargs):
        now = datetime.now()
        if 'type' in self.request.GET:
            if self.request.GET['type'] == 'tudo':
                self.queryset = Pedido.objects.filter(estabelecimento__user=self.request.user).order_by('-created_at')
            elif self.request.GET['type'] == 'mes':
                self.queryset = Pedido.objects.filter(estabelecimento__user=self.request.user,
                                                      created_at__month=now.month,
                                                      created_at__year=now.year).order_by('-created_at')
            else:
                self.queryset = Pedido.objects.filter(estabelecimento__user=self.request.user,
                                                      created_at__month=now.month,
                                                      created_at__year=now.year, created_at__day=now.day).order_by(
                    '-created_at')
        else:
            self.queryset = Pedido.objects.filter(estabelecimento__user=self.request.user,
                                                  created_at__month=now.month,
                                                  created_at__year=now.year, created_at__day=now.day).order_by(
                '-created_at')
        return super(PedidosLojaListView, self).get(request, *args, **kwargs)


class PedidosMotoristaListView(LoginRequiredMixin, RedirectMotoristaOcupadoView, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'entrega/pedidos/list_pedidos_motorista.html'

    def get_queryset(self):
        return Pedido.objects.filter(is_complete=False, coletado=False, status=True, is_draft=False,
                                     chamar_motoboy=False).order_by(
            '-created_at')


class PedidosMotoristaPremiumListView(LoginRequiredMixin, RedirectMotoristaOcupadoView, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'entrega/pedidos/list_pedidos_premium.html'

    def get_queryset(self):
        return Pedido.objects.filter(is_complete=False, coletado=False, status=True, is_draft=False,
                                     chamar_motoboy=False).order_by(
            '-created_at')


class EntregasMotoristaListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'entrega/pedidos/list_entregas_motorista.html'

    def get_queryset(self):
        return Pedido.objects.filter(motorista=self.request.user).order_by('-published_at')


@require_http_methods(["GET"])
def buscar_cliente(request):
    q = request.GET['q']
    results = []
    try:
        qs = Ponto.objects.filter(telefone__icontains=q).order_by('-created_at')
        for ponto in qs:
            results.append({
                'cliente': ponto.cliente,
                'endereco': ponto.endereco,
                'numero': ponto.numero,
                'bairro': ponto.bairro.nome,
                'complemento': ponto.complemento,
                'observacoes': ponto.observacoes
            })
    except (Exception,):
        pass
    return JsonResponse({'results': results})


class PedidoCreateView(LoginRequiredMixin, CreateView, CustomContextMixin):
    model = Pedido
    success_url = '/app/pedidos/loja/'
    fields = ['estabelecimento', 'is_draft']
    template_name = 'entrega/pedidos/add_pedido.html'
    login_url = '/login/'

    # def get_success_url(self):
    # return reverse('view_pedido_view', kwargs={'pk': self.object.pk})

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }

    def get_context_data(self, **kwargs):
        data = super(PedidoCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['pontoset'] = PontoFormSet(self.request.POST)
        else:
            data['pontoset'] = PontoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pontoset = context['pontoset']
        with transaction.atomic():
            self.object = form.save()
            if pontoset.is_valid():
                pontoset.instance = self.object
                pontoset.save()
        pedido = self.object
        try:
            logger(self.request.user, "Criou a Rota #" + str(pedido.pk))
        except (Exception,):
            pass
        if not pedido.is_draft:
            no = Notification(type_message='NOTIFICACAO_COZINHA', to=self.request.user, message='NOVO PEDIDO REALIZADO')
            no.save()
        return super(PedidoCreateView, self).form_valid(form)


def get_or_create_rota(request, loja, bairro):
    rotas = Pedido.objects.filter(coletado=False, status_cozinha=False)
    if rotas:
        return rotas.last()
    else:
        rota = Pedido(estabelecimento=loja, valor_total='6')
        rota.save()
        return rota


class PedidoDetailView(LoginRequiredMixin, DetailView, CustomContextMixin):
    model = Pedido
    login_url = '/login/'
    template_name = 'entrega/acompanhar/view_pedido.html'

    def get_context_data(self, **kwargs):
        data = super(PedidoDetailView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['pontoset'] = PontoFormUpdateSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['pontoset'] = PontoFormUpdateSet(instance=self.object)
        return data


class PedidoUpdateView(LoginRequiredMixin, UpdateView, CustomContextMixin):
    model = Pedido
    login_url = '/login/'
    success_url = '/app/pedidos/loja/'
    fields = ['estabelecimento', 'is_draft']
    template_name = 'entrega/pedidos/edit_pedido.html'

    def get_initial(self):
        return {
            'estabelecimento': Estabelecimento.objects.get(user=self.request.user)
        }

    def get_context_data(self, **kwargs):
        data = super(PedidoUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['pontoset'] = PontoFormUpdateSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['pontoset'] = PontoFormUpdateSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pontoset = context['pontoset']
        with transaction.atomic():
            if pontoset.is_valid():
                pontoset.instance = self.object
                pontoset.save()
            self.object = form.save()
        pedido = self.object
        try:
            logger(self.request.user, "Editou a Rota #" + str(pedido.pk))
        except (Exception,):
            pass
        return super(PedidoUpdateView, self).form_valid(form)


def delete_pedido(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Usuario precisa estar logado para esta operacao")
        raise PermissionDenied("Usuario precisa estar logado para esta operacao")
    else:
        pedido = Pedido.objects.get(id=pk)
        try:
            user_motorista = pedido.motorista
            motorista = Motorista.objects.get(user=user_motorista)
        except:
            user_motorista = None
        if user_motorista:
            if user_motorista.pedido_set.last() == pedido:
                motorista.ocupado = False
                motorista.save()
                loja = Estabelecimento.objects.get(user=request.user)
                if motorista.is_online:
                    message = "O Pedido que voce ia entregar foi deletado pela loja " + request.user.first_name + ". Desculpe pelo transtorno! Qualquer coisa, ligue para a loja: " + loja.phone
                    n = Notification(type_message='DELETE_LOJA', to=motorista.user, message=message)
                    n.save()
        pedido.delete()
        try:
            logger(request.user, "Deletou a Rota #" + str(pedido.pk))
        except (Exception,):
            pass
        messages.success(request, "Pedido deletado com sucesso")
        return HttpResponseRedirect('/app/pedidos/loja/')


def cancel_pedido(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Usuario precisa estar logado para esta operacao")
        raise PermissionDenied("Usuario precisa estar logado para esta operacao")
    else:
        pedido = Pedido.objects.get(id=pk)
        try:
            user_motorista = pedido.motorista
            motorista = Motorista.objects.get(user=user_motorista)
        except:
            user_motorista = None
        if user_motorista:
            if user_motorista.pedido_set.last() == pedido:
                motorista.ocupado = False
                motorista.save()
                loja = Estabelecimento.objects.get(user=request.user)
                if motorista.is_online:
                    message = "O Pedido que voce ia entregar foi cancelado pela loja " + request.user.first_name + ". Desculpe pelo transtorno! Qualquer coisa, ligue para a loja: " + loja.phone
                    n = Notification(type_message='DELETE_LOJA', to=motorista.user, message=message)
                    n.save()
        pedido.status = True
        pedido.motorista = None
        pedido.save()
        try:
            logger(request.user, "Cancelou a Rota #" + str(pedido.pk))
        except (Exception,):
            pass
        messages.success(request, "Pedido deletado com sucesso")
        return HttpResponseRedirect('/app/pedidos/loja/')


@require_http_methods(["GET"])
def get_pedidos_motorista(request):
    pedidos = Pedido.objects.filter(is_complete=False, coletado=False, status=True, is_draft=False,
                                    chamar_motoboy=False).order_by(
        '-created_at')
    context = Context({'pedidos': pedidos, 'user': request.user})
    return_str = render_block_to_string('entrega/includes/table_pedidos_motorista.html', context)
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def get_entregas_motorista(request):
    pedidos = Pedido.objects.filter(motorista=request.user).order_by('-published_at')
    context = Context({'pedidos': pedidos, 'user': request.user})
    return_str = render_block_to_string('entrega/includes/table_entregas_motorista.html', context)
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def accept_corrida(request, pk_pedido):
    try:
        pedido = Pedido.objects.get(id=pk_pedido)
        if pedido.motorista:
            try:
                messages.error(request,
                               'O motorista ' + pedido.motorista.first_name + ' pegou esta entrega antes de você')
            except (Exception,):
                messages.error(request, 'Outro Motorista pegou esta entrega antes de você')
            return HttpResponseRedirect('/app/pedidos/motorista/')
        else:
            pedido.status = False
            pedido.motorista = request.user
            pedido.save()
            motorista = Motorista.objects.get(user=request.user)
            motorista.ocupado = True
            motorista.save()
            if pedido.estabelecimento.is_online:
                message = "O motorista " + str(
                    motorista.user.first_name) + " aceitou fazer a entrega do Pedido ID #" + str(
                    pedido.pk) + ". Qualquer problema, ligue para o motorista: " + motorista.phone
                n = Notification(type_message='ACCEPT_ORDER', to=pedido.estabelecimento.user, message=message)
                n.save()
                message = 'A Loja ' + pedido.estabelecimento.user.first_name + ', localizado na ' + pedido.estabelecimento.full_address + ', esta aguardando a coleta.'
                no = Notification(type_message='DELETE_LOJA', to=pedido.motorista,
                                  message=message)  # está delete loja por enquanto.
                no.save()
            try:
                logger(request.user, "Aceitou fazer a Rota #" + str(pedido.pk))
            except (Exception,):
                pass
            return HttpResponseRedirect('/app/pedido/route/' + str(pedido.pk))
    except (Exception,):
        messages.error(request, 'Este pedido foi deletado pela Loja')
        return HttpResponseRedirect('/app/pedidos/motorista/')


@require_http_methods(["GET"])
def liberar_corrida(request, pk_pedido):
    pedido = Pedido.objects.get(id=pk_pedido)
    pedido.coletado = True
    pedido.save()
    try:
        if pedido.request_set.first():
            reqs = pedido.request_set.all()
            for req in reqs:
                req.status_pedido = 'ENTREGANDO'
                req.save()
    except (Exception,):
        pass
    if Motorista.objects.get(user=pedido.motorista).is_online:
        message = "Voce foi liberado pela loja para realizar a(s) entrega(s). Sua Rota atual esta no menu ENTREGAS. Quando terminar uma entrega, marque finalizar. Qualquer problema, ligue para a loja: " + pedido.estabelecimento.phone
        n = Notification(type_message='ENABLE_ROTA', to=pedido.motorista, message=message)
        n.save()
    try:
        logger(request.user, "Foi liberada a Rota #" + str(pedido.pk))
    except (Exception,):
        pass
    return redirect('/app/acompanhar')


@require_http_methods(["GET"])
def avaliar_motorista(request, pk_pedido, nota):
    pedido = Pedido.objects.get(id=pk_pedido)
    motorista = Motorista.objects.get(user=pedido.motorista)
    new_class = Classification(user=motorista.user, pedido=pedido, nota=nota)
    new_class.save()
    return redirect('/app/pedidos/loja')


@require_http_methods(["GET"])
def finalizar_entrega(request, pk_ponto, pk_pedido):
    try:
        ponto = Ponto.objects.get(id=pk_ponto)
        pedido = Pedido.objects.get(id=pk_pedido)
        ponto.status = True
        ponto.save()
        try:
            if pedido.request_set.first():
                reqs = pedido.request_set.all()
                for req in reqs:
                    req.status_pedido = 'ENTREGUE'
                    req.save()
        except (Exception,):
            pass
        pto_entregues = len(pedido.ponto_set.filter(status=True))
        if len(pedido.ponto_set.all()) == pto_entregues:
            pedido.is_complete = True
            pedido.save()
            messages.success(request, 'Tudo entregue! Finalize esta Rota para poder pegar outros.')
        if pedido.estabelecimento.is_online:
            message = "Motorista " + request.user.first_name + " entregou pedido ao cliente " + ponto.cliente + " no endereco " + ponto.full_address
            n = Notification(type_message='ORDER_DELIVERED', to=pedido.estabelecimento.user, message=message)
            n.save()
        try:
            logger(request.user, "Finalizou a Entrega #" + str(ponto.pk))
        except (Exception,):
            pass
        return HttpResponseRedirect('/app/pedido/route/' + str(pedido.pk))
    except:
        messages.error(request, 'Este pedido foi deletado pela Loja')
        return HttpResponseRedirect('/app/pedidos/motorista/')


@require_http_methods(["GET"])
def finalizar_pedido(request, pk_pedido):
    try:
        pedido = Pedido.objects.get(id=pk_pedido)
        pedido.btn_finalizado = True
        pedido.save()
        motorista = Motorista.objects.get(user=request.user)
        motorista.ocupado = False
        motorista.save()
        message = "O motorista " + request.user.first_name + " finalizou por completo a ROTA ID #" + str(
            pedido.pk) + ". Se desejar confirmar, ligue para o motorista: " + motorista.phone
        n = Notification(type_message='ALL_DELIVERED', to=pedido.estabelecimento.user, message=message)
        n.save()
        message = 'Voce concluiu a Rota, se voce estiver com algum material (maquineta ou bag) da Loja ' + pedido.estabelecimento.user.first_name + ',  favor devolver. Obrigado!'
        messages.success(request, message)
        try:
            logger(request.user, "Finalizou a Rota #" + str(pedido.pk))
        except (Exception,):
            pass
        if motorista.configuration.plano == 'PREMIUM':
            return HttpResponseRedirect('/app/pedidos/motorista/premium/')
        return HttpResponseRedirect('/app/pedidos/motorista/')
    except:
        messages.error(request, 'Este pedido foi deletado pela Loja')
        if motorista.configuration.plano == 'PREMIUM':
            return HttpResponseRedirect('/app/pedidos/motorista/premium/')
        return HttpResponseRedirect('/app/pedidos/motorista/')


@require_http_methods(["GET"])
def get_pedidos(request):
    pedidos = Pedido.objects.filter(status=True)
    if len(pedidos) > 0:
        return JsonResponse({'result': '1'})
    return JsonResponse({'result': '0'})
