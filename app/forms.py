#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base64 import b64encode

import pyimgur
from django import forms
from django.forms import ModelForm, inlineformset_factory, formset_factory

from app.models import *


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone'
            if field_name == 'numero' or field_name == 'number':
                field.widget.attrs['class'] = 'form-control numero'


class FormBaseAddress(BaseForm):
    cep = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'required': True,
                                                                       'maxlength': 200,
                                                                       'placeholder': 'CEP'
                                                                       }))
    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    bairro = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
                                                                          'maxlength': 200,
                                                                          'placeholder': 'Bairro'
                                                                          }))


class FormLogin(BaseForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))


class FormPedido(ModelForm, BaseForm):
    class Meta:
        model = Pedido
        fields = ['estabelecimento', 'is_draft']


class FormRequest(ModelForm, BaseForm):
    class Meta:
        model = Request
        fields = ['forma_pagamento', 'forma_entrega', 'troco', 'status_pedido', ]


class FormChamado(ModelForm, BaseForm):
    class Meta:
        model = Chamado
        fields = ['estabelecimento', 'titulo', 'texto']

    def __init__(self, *args, **kwargs):
        super(FormChamado, self).__init__(*args, **kwargs)
        self.fields['estabelecimento'].widget.attrs['class'] = 'hidden'
        self.fields['estabelecimento'].label = ''


class FormConfiguration(ModelForm, BaseForm):
    class Meta:
        model = Configuration
        fields = ['chamar_motoboy', 'tempo_de_entrega', 'status_entrega_gratis']


class FormItemPedido(ModelForm, BaseForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade', 'observacoes', 'valor_total']

    def __init__(self, *args, **kwargs):
        super(FormItemPedido, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = 'true'
            field.widget.attrs['class'] += ' disabled'


ItemPedidoFormSet = inlineformset_factory(Request, ItemPedido, form=FormItemPedido, extra=1)


class FormPonto(ModelForm, BaseForm):
    telefone = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'telefone',
                                                             'maxlength': 200,
                                                             'placeholder': 'Telefone do Cliente'}))
    cliente = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                            'maxlength': 200,
                                                            'placeholder': 'Nome do Cliente'}))

    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 6, 'class': 'numero',
                                                                         'placeholder': 'Número'
                                                                         }))
    complemento = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                                'maxlength': 200,
                                                                                'placeholder': 'Ponto de Referencia'
                                                                                }))
    observacoes = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'required': True,
                                                                                               'maxlength': 300,
                                                                                               'placeholder': 'Insira aqui as instrucoes de pagamento e o valor do pedido para ser coletado pelo motoboy'
                                                                                               }))

    itens = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'required': True,
                                                                                         'maxlength': 300,
                                                                                         'placeholder': 'Insira o Pedido para a Cozinha'
                                                                                         }))

    class Meta:
        model = Ponto
        fields = ['telefone', 'cliente', 'endereco', 'numero', 'bairro', 'complemento', 'observacoes', 'itens']


class FormEditPonto(ModelForm, BaseForm):
    telefone = forms.CharField(widget=forms.TextInput(attrs={'required': False, 'class': 'telefone',
                                                             'maxlength': 200,
                                                             'placeholder': 'Telefone do Cliente'}))
    cliente = forms.CharField(widget=forms.TextInput(attrs={'required': False,
                                                            'maxlength': 200,
                                                            'placeholder': 'Nome do Cliente'}))

    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': False,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': False,
                                                                         'maxlength': 200, 'class': 'numero',
                                                                         'placeholder': 'Número'
                                                                         }))
    complemento = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': False,
                                                                                'maxlength': 200,
                                                                                'placeholder': 'Ponto de Referencia'
                                                                                }))
    observacoes = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'required': False,
                                                                                               'maxlength': 300,
                                                                                               'placeholder': 'Observações'
                                                                                               }))

    itens = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'required': True,
                                                                                         'maxlength': 300,
                                                                                         'placeholder': 'Insira o Pedido para a Cozinha'
                                                                                         }))

    class Meta:
        model = Ponto
        fields = ['id', 'telefone', 'cliente', 'endereco', 'numero', 'bairro', 'complemento', 'observacoes', 'itens']


class FormRegister(ModelForm, BaseForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                               'maxlength': 200,
                                                               'placeholder': 'Nome Estabelecimento'}))
    cnpj = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                         'maxlength': 200,
                                                         'placeholder': 'CNPJ'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'maxlength': 200,
                                                          'placeholder': 'Telefone'}))
    endereco = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
                                                                            'maxlength': 200,
                                                                            'placeholder': 'Endereço'
                                                                            }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'required': True, 'placeholder': 'Logotipo do Estabelecimento'
                                                         }))

    class Meta:
        model = Estabelecimento
        fields = ['bairro', ]


class FormEditPerfil(ModelForm, BaseForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                               'maxlength': 200,
                                                               'placeholder': 'Nome Estabelecimento'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'maxlength': 200,
                                                          'placeholder': 'Telefone'}))
    endereco = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
                                                                            'maxlength': 200,
                                                                            'placeholder': 'Endereço'
                                                                            }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'required': True, 'placeholder': 'Logotipo do Estabelecimento'
                                                         }))

    class Meta:
        model = Estabelecimento
        fields = ['bairro', 'cnpj', ]


class FormMotoristaRegister(ModelForm, BaseForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                               'maxlength': 200,
                                                               'placeholder': 'Nome Completo'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))
    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'maxlength': 200,
                                                          'placeholder': 'Telefone'}))
    cpf = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'required': True,
                                                                                       'maxlength': 200,
                                                                                       'placeholder': 'CPF'
                                                                                       }))
    placa = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'required': True,
                                                                                         'maxlength': 200,
                                                                                         'placeholder': 'Placa do Veiculo'
                                                                                         }))
    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'required': False, 'placeholder': 'Logotipo do Estabelecimento'
                                                         }))

    class Meta:
        model = Motorista
        fields = []


PontoFormSet = inlineformset_factory(Pedido, Ponto, form=FormPonto, extra=1)

PontoFormUpdateSet = inlineformset_factory(Pedido, Ponto, form=FormEditPonto, extra=0)


class FormBairroGratis(ModelForm, BaseForm):
    class Meta:
        model = BairroGratis
        fields = ['bairro', 'estabelecimento']

    def __init__(self, *args, **kwargs):
        super(FormBairroGratis, self).__init__(*args, **kwargs)
        self.fields['estabelecimento'].widget.attrs['class'] = 'hidden'
        self.fields['estabelecimento'].label = ''


# BairroGratisFormSet = inlineformset_factory(Estabelecimento, BairroGratis, form=FormBairroGratis, extra=1)


class FormPontoCliente(ModelForm, BaseForm):
    class Meta:
        model = Ponto
        fields = ['cliente', 'telefone', 'endereco', 'numero', 'bairro', 'complemento']


# -------------------------------------

class FormCategoria(ModelForm, BaseForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'estabelecimento', ]

    def __init__(self, *args, **kwargs):
        super(FormCategoria, self).__init__(*args, **kwargs)
        self.fields['estabelecimento'].widget.attrs['class'] = 'hidden'
        self.fields['estabelecimento'].label = ''


class FormEndereco(ModelForm, BaseForm):
    class Meta:
        model = Endereco
        fields = ['endereco', 'numero', 'bairro', 'complemento', 'cliente']

    def __init__(self, *args, **kwargs):
        super(FormEndereco, self).__init__(*args, **kwargs)
        self.fields['cliente'].widget.attrs['class'] = 'hidden'
        self.fields['cliente'].label = ''


class FormGrupo(ModelForm, BaseForm):
    class Meta:
        model = Grupo
        fields = ['identificador', 'titulo', 'produto', 'limitador', 'obrigatoriedade', 'disponivel']

    def __init__(self, *args, **kwargs):
        super(FormGrupo, self).__init__(*args, **kwargs)
        self.fields['produto'].widget.attrs['class'] = 'hidden'
        self.fields['produto'].label = ''


class FormGrupoInline(ModelForm, BaseForm):
    class Meta:
        model = Grupo
        fields = ['identificador', 'titulo', 'limitador', 'obrigatoriedade', 'disponivel']


class FormProduto(ModelForm, BaseForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco_base', 'disponivel']


class FormFotoProdutoInline(ModelForm, BaseForm):
    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'required': True, 'placeholder': 'Foto do Produto'
                                                         }))

    class Meta:
        model = FotoProduto
        fields = ['url', 'file']

    def __init__(self, *args, **kwargs):
        super(FormFotoProdutoInline, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['class'] = 'hidden'
        self.fields['url'].label = ''


class FormFotoProduto(ModelForm, BaseForm):
    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'required': True, 'placeholder': 'Logotipo do Estabelecimento'
                                                         }))

    class Meta:
        model = FotoProduto
        fields = ['produto', 'file']


class FormOpcionalInline(ModelForm, BaseForm):
    class Meta:
        model = Opcional
        fields = ['nome', 'descricao', 'valor', 'disponivel']


class FormOpcional(ModelForm, BaseForm):
    class Meta:
        model = Opcional
        fields = ['nome', 'descricao', 'valor', 'disponivel']


ProdutoFormSet = inlineformset_factory(Categoria, Produto, form=FormProduto, extra=1)
FotoProdutoFormSet = inlineformset_factory(Produto, FotoProduto, form=FormFotoProdutoInline, extra=1)
FotoProdutoUpdateFormSet = inlineformset_factory(Produto, FotoProduto, form=FormFotoProdutoInline, extra=1)
GrupoFormSet = inlineformset_factory(Produto, Grupo, form=FormGrupoInline, extra=1)
GrupoUpdateFormSet = inlineformset_factory(Produto, Grupo, form=FormGrupoInline, extra=1)
OpcionalFormSet = inlineformset_factory(Grupo, Opcional, form=FormOpcionalInline, extra=1)
OpcionalUpdateFormSet = inlineformset_factory(Grupo, Opcional, form=FormOpcionalInline, extra=1)


class FormFormaPagamento(ModelForm, BaseForm):
    class Meta:
        model = FormaPagamento
        fields = ['forma', 'cartao', 'estabelecimento']

    def __init__(self, *args, **kwargs):
        super(FormFormaPagamento, self).__init__(*args, **kwargs)
        self.fields['estabelecimento'].widget.attrs['class'] = 'hidden'
        self.fields['estabelecimento'].label = ''


class FormFormaEntrega(ModelForm, BaseForm):
    class Meta:
        model = FormaEntrega
        fields = ['forma', 'estabelecimento', ]

    def __init__(self, *args, **kwargs):
        super(FormFormaEntrega, self).__init__(*args, **kwargs)
        self.fields['estabelecimento'].widget.attrs['class'] = 'hidden'
        self.fields['estabelecimento'].label = ''


class FormRegisterCliente(BaseForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                         'maxlength': 100,
                                                         'placeholder': 'Nome'}))
    sobrenome = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                              'maxlength': 100,
                                                              'placeholder': 'Sobrenome'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 15,
                                                             'placeholder': 'Numero Telefone'}))

    # cpf = forms.CharField(widget=forms.TextInput(attrs={'required': True,
    #                                                     'maxlength': 12,
    #                                                     'placeholder': 'CPF'}))


class FormLoginCliente(BaseForm):
    telefone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                        'maxlength': 12,
                                                        'placeholder': 'Numero Telefone'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))
