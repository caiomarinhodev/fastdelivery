#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base64 import b64encode

import pyimgur
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from app.forms import FormLogin, FormRegister, FormEditPerfil, FormMotoristaRegister, FormConfiguration
from app.models import *
from app.views.fcm import func

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class AppView(TemplateView):
    def get(self, request, *args, **kwargs):
        if self.request.user:
            try:
                motorista = self.request.user.motorista
                if motorista:
                    if motorista.configuration.plano == 'PREMIUM':
                        return redirect('/app/pedidos/motorista/premium/')
                    print ('--------- motorista is logged')
                    return redirect('/app/pedidos/motorista')
            except (Exception,):
                try:
                    loja = self.request.user.estabelecimento
                    if loja:
                        print ('--------- estabelecimento is logged')
                        return redirect('/app/pedidos/loja')
                except:
                    return redirect('/loja/')
        else:
            return redirect('/loja')


class LoginView(FormView):
    """
    Displays the login form.
    """
    template_name = 'entrega/page/login.html'
    form_class = FormLogin
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(**data)
        print(user)
        try:
            loja = user.estabelecimento
            if not loja.is_approved:
                return self.form_invalid(form)
        except:
            pass

        try:
            motorista = user.motorista
            if not motorista.is_approved:
                return self.form_invalid(form)
        except:
            pass

        if user is not None:
            login(self.request, user)
        else:
            return self.form_invalid(form)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Nenhum usuário encontrado')
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        url = '/'
        motorista = None
        loja = None
        try:
            user = self.request.user
        except:
            user = None
        try:
            motorista = user.motorista
        except:
            pass

        try:
            loja = user.estabelecimento
        except:
            pass

        if user:
            if loja:
                url = '/app/pedidos/loja'
                loja.is_online = True
                loja.save()
                self.success_url = url
            elif motorista:
                if motorista.configuration.plano == 'PREMIUM':
                    url = '/app/pedidos/motorista/premium/'
                else:
                    url = '/app/pedidos/motorista'
                motorista.is_online = True
                motorista.save()
                # if motorista.ocupado:
                #     url = '/app/entregas/motorista'
                self.success_url = url
            elif user.is_superuser:
                url = '/app/dashboard/'
                self.success_url = url
            else:
                url = '/'
                self.success_url = url
        else:
            url = '/'
            self.success_url = url
        return url


class LogoutView(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        user = self.request.user
        motorista = None
        loja = None
        try:
            motorista = user.motorista
        except:
            pass

        try:
            loja = user.estabelecimento
        except:
            pass
        if motorista:
            motorista.is_online = False
            motorista.save()
        elif loja:
            loja.is_online = False
            loja.save()
        logout(self.request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = 'entrega/page/register.html'
    form_class = FormRegister
    success_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        aux_obj = User.objects.filter(username=data['username'])
        if len(aux_obj) > 0:
            messages.error(self.request, 'Este Login já existe. Tente novamente!')
            return self.form_invalid(form)
        user_data = {}
        common_data = {}
        try:
            CLIENT_ID = "cdadf801dc167ab"
            bencode = b64encode(self.request.FILES['file'].read())
            client = pyimgur.Imgur(CLIENT_ID)
            r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': bencode})
            file = r['link']
            print(file)
        except (Exception,):
            file = "http://placehold.it/150x150"
        try:
            user_data['first_name'] = data['first_name']
            user_data['username'] = data['username']
            user_data['password'] = data['password']
            common_data['endereco'] = data['endereco']
            common_data['phone'] = data['phone']
            common_data['cnpj'] = data['cnpj']
            common_data['numero'] = data['numero']
            common_data['bairro'] = data['bairro']
            common_data['photo'] = file
            if data['username'] and data['password']:
                new_user = User.objects.create_user(**user_data)
                new_common_user = Estabelecimento(user=new_user, **common_data)
                new_common_user.save()
                messages.success(self.request, 'Sua conta será analisada pelos nossos administradores. Aguarde o contato!')
            else:
                messages.error(self.request, "Houve algum erro. Tente Novamente")
                return self.form_invalid(form)
        except (Exception,):
            messages.error(self.request, "Houve algum erro. Tente Novamente")
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(RegisterView, self).form_invalid(form)

    def str_to_bool(self, s):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:
            raise ValueError


class RegisterMotoristaView(FormView):
    template_name = 'entrega/page/register-driver.html'
    form_class = FormMotoristaRegister
    success_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        aux_obj = User.objects.filter(username=data['username'])
        if len(aux_obj) > 0:
            messages.error(self.request, 'Este Login já existe. Tente novamente!')
            return self.form_invalid(form)
        user_data = {}
        common_data = {}
        try:
            if self.request.FILES:
                CLIENT_ID = "cdadf801dc167ab"
                bencode = b64encode(self.request.FILES['file'].read())
                client = pyimgur.Imgur(CLIENT_ID)
                r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': bencode})
                file = r['link']
            else:
                file = "http://placehold.it/300x300"
        except (Exception,):
            file = "http://placehold.it/300x300"

        try:
            user_data['first_name'] = data['first_name']
            user_data['username'] = data['username']
            user_data['password'] = data['password']
            common_data['placa'] = str(data['placa']).upper()
            common_data['phone'] = data['phone']
            common_data['cpf'] = data['cpf']
            common_data['endereco'] = data['endereco']
            common_data['numero'] = data['numero']
            common_data['photo'] = file
            if data['username'] and data['password']:
                new_user = User.objects.create_user(**user_data)
                new_common_user = Motorista(user=new_user, **common_data)
                new_common_user.save()
                messages.success(self.request, 'Sua conta será analisada pelos nossos administradores. Aguarde o contato!')
            else:
                return self.form_invalid(form)
        except (Exception,):
            messages.error(self.request, "Houve algum erro. Tente Novamente.")
        return super(RegisterMotoristaView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(RegisterMotoristaView, self).form_invalid(form)

    def str_to_bool(self, s):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:
            raise ValueError


class EditarPerfilView(LoginRequiredMixin, FormView):
    template_name = 'entrega/pedidos/editar_perfil_loja.html'
    form_class = FormEditPerfil
    model = Estabelecimento
    login_url = '/login/'
    success_url = '/app/perfil/edit'

    def get_object(self, queryset=None):
        return self.request.user.estabelecimento

    def merge_two_dicts(self, x, y):
        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z

    def get_context_data(self, **kwargs):
        data = super(EditarPerfilView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['configurationform'] = FormConfiguration(self.request.POST, self.request.FILES, instance=self.request.user.estabelecimento.configuration)
        else:
            data['configurationform'] = FormConfiguration(instance=self.request.user.estabelecimento.configuration)
        return data

    def get_initial(self):
        estabel = Estabelecimento.objects.get(user=self.request.user)
        data = self.merge_two_dicts(estabel.__dict__, self.request.user.__dict__)
        data['first_name'] = self.request.user.first_name
        data['file'] = estabel.photo
        data['photo'] = estabel.photo
        return data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        configuration_set = context['configurationform']
        if configuration_set.is_valid():
            configuration_set.save()
        data = form.cleaned_data
        user = self.request.user
        estabel = Estabelecimento.objects.get(user=user)
        CLIENT_ID = "cdadf801dc167ab"
        if 'file' in self.request.FILES:
            bencode = b64encode(self.request.FILES['file'].read())
            client = pyimgur.Imgur(CLIENT_ID)
            r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': bencode})
            file = r['link']
            print(file)
            estabel.photo = file
        user.first_name = data['first_name']
        estabel.endereco = data['endereco']
        estabel.phone = data['phone']
        estabel.numero = data['numero']
        estabel.bairro = data['bairro']
        estabel.cnpj = data['cnpj']
        user.save()
        estabel.save()
        messages.success(self.request, 'Conta Alterada com sucesso!')
        return super(EditarPerfilView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Não foi possível alterar os dados.')
        return super(EditarPerfilView, self).form_invalid(form)


class SetOnlineMotoboyView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user:
            motorista = Motorista.objects.get(user=self.request.user)
            motorista.is_online = not motorista.is_online
            motorista.save()
            if motorista.configuration.plano == 'PREMIUM':
                return '/app/pedidos/motorista/premium/'
            return '/app/pedidos/motorista'
        else:
            return '/login/'


