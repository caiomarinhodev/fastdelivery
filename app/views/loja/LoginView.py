#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from django.views.generic import RedirectView
from pycpfcnpj import cpfcnpj

from app.forms import FormLogin, FormRegisterCliente, FormLoginCliente
from app.models import *

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class LojaRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user:
            try:
                loja = Cliente.objects.get(usuario=self.request.user)
                if loja:
                    return '/'
            except:
                return '/login/cliente'
        else:
            return '/login/cliente'


class EscolheLoginView(TemplateView):
    template_name = 'loja/escolhe_login.html'


class ClienteLoginView(FormView):
    template_name = 'loja/login_cliente.html'
    form_class = FormLoginCliente

    def get_success_url(self):
        session = self.request.session
        try:
            if 'lojaid' in session:
                return '/loja/' + str(session['lojaid'])
        except (Exception,):
            pass
        try:
            if 'pedido' in session:
                req = Request.objects.get(id=session['pedido'])
                return '/loja/' + str(req.estabelecimento.id)
        except (Exception,):
            return '/'
        return '/'

    def get(self, request, *args, **kwargs):
        if self.request.user:
            try:
                loja = self.request.user.cliente
                if loja:
                    return redirect('/')
            except (Exception,):
                return super(ClienteLoginView, self).get(request, *args, **kwargs)

        else:
            return super(ClienteLoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            user_data = {}
            user_data['username'] = data['telefone']
            user_data['password'] = data['password']
            user = authenticate(**user_data)
            if user is not None:
                login(self.request, user)
            else:
                return self.form_invalid(form)
        except:
            return self.form_invalid(form)
        return super(ClienteLoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Nenhum usuário encontrado')
        return super(ClienteLoginView, self).form_invalid(form)


class RegistroCliente(FormView):
    template_name = 'loja/registro_cliente.html'
    form_class = FormRegisterCliente
    success_url = '/login/cliente'

    def get(self, request, *args, **kwargs):
        return super(RegistroCliente, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        # try:
        user_data = {}
        if not str(data['telefone']).isdigit():
            messages.error(self.request, 'Insira apenas numeros no Telefone')
            return self.form_invalid(form)
        if len(data['telefone']) < 8:
            messages.error(self.request, 'Insira um Telefone valido')
            return self.form_invalid(form)
        if len(data['password']) < 5:
            messages.error(self.request, 'Insira uma senha maior que 5 caracteres')
            return self.form_invalid(form)
        # if not cpfcnpj.validate(str(data['cpf'])):
        #     messages.error(self.request, 'CPF invalido')
        #     return self.form_invalid(form)
        user_data['username'] = data['telefone']
        user_data['first_name'] = data['nome']
        user_data['last_name'] = data['sobrenome']
        user_data['password'] = data['password']
        try:
            user = User.objects.create_user(**user_data)
        except (Exception,):
            messages.error(self.request, 'Ja existe uma conta com este numero')
            return self.form_invalid(form)
        cliente = Cliente(
            cpf=' ',
            telefone=data['telefone'],
            usuario=user
        )
        cliente.save()
        messages.success(self.request, 'Registrado com Sucesso')
        return HttpResponseRedirect(self.get_success_url())
        # except (Exception,):
        #     messages.error(self.request, 'Houve algum erro, tente novamente')
        #     return self.form_invalid(form)

    def form_invalid(self, form):
        return super(RegistroCliente, self).form_invalid(form)
