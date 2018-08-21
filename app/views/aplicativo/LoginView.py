#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic import RedirectView

from app.forms import FormClienteLogin, FormClienteRegister
from app.models import *

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class LoginClienteView(FormView):
    template_name = 't_app/login.html'
    form_class = FormClienteLogin

    def get_success_url(self):
        return '/aplicativo/loja/'

    def get(self, request, *args, **kwargs):
        if self.request.user:
            try:
                loja = self.request.user.cliente
                if loja:
                    return redirect('/')
            except (Exception,):
                return super(LoginClienteView, self).get(request, *args, **kwargs)

        else:
            return super(LoginClienteView, self).get(request, *args, **kwargs)

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
        return super(LoginClienteView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Nenhum usuário encontrado')
        return super(LoginClienteView, self).form_invalid(form)


class RegistroClienteView(FormView):
    template_name = 't_app/signup.html'
    form_class = FormClienteRegister
    success_url = '/aplicativo/login'

    def get(self, request, *args, **kwargs):
        return super(RegistroClienteView, self).get(request, *args, **kwargs)

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
        return super(RegistroClienteView, self).form_invalid(form)


class LogoutClienteView(RedirectView):
    url = '/aplicativo/login'
    permanent = False

    def get(self, request, *args, **kwargs):
        user = self.request.user
        cliente = user.cliente
        if cliente:
            cliente.is_online = False
            cliente.save()
        logout(self.request)
        return super(LogoutClienteView, self).get(request, *args, **kwargs)
