# coding=utf-8
from __future__ import unicode_literals

from base64 import b64encode
from datetime import datetime, time

import pyimgur
from django.contrib.auth.models import User
from django.db import models

from app.views.geocoding import geocode


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)


class Bairro(TimeStamped):
    nome = models.CharField(max_length=100, blank=True)
    valor = models.CharField(max_length=3, blank=True, null=True, default='6')
    valor_madrugada = models.CharField(max_length=3, default='8')
    valor_madrugada_feriado = models.CharField(max_length=3, default='11')
    valor_feriado = models.CharField(max_length=3, default='9')

    def __unicode__(self):
        return u'%s' % self.nome

    def __str__(self):
        return u'%s' % self.nome


class BaseAddress(models.Model):
    class Meta:
        abstract = True

    bairro = models.ForeignKey(Bairro, blank=True, null=True, verbose_name='Bairro')
    endereco = models.CharField(max_length=200, blank=True, null=True, verbose_name='Endereço')
    numero = models.CharField(max_length=5, blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=300, blank=True, null=True, verbose_name='Ponto de Referência')
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)


THEMES = (
    ('BLACK', 'skin-black'),
    ('BLUE', 'skin-blue'),
    ('RED', 'skin-red'),
    ('YELLOW', 'skin-yellow'),
    ('PURPLE', 'skin-purple'),
    ('GREEN', 'skin-green'),
    # 'skin-blue-light',
    # 'skin-black-light',
    # 'skin-red-light',
    # 'skin-yellow-light',
    # 'skin-purple-light',
    # 'skin-green-light'
)

PLANS = (
    ('BASIC', 'BASIC'),
    ('PREMIUM', 'PREMIUM'),
)


class Configuration(TimeStamped):
    class Meta:
        verbose_name = u'Configuração'
        verbose_name_plural = u'Configurações'

    tema = models.CharField(max_length=100, blank=True, null=True, choices=THEMES, default='skin-black')
    plano = models.CharField(max_length=100, choices=PLANS, default='BASIC')
    chamar_motoboy = models.BooleanField(default=True)
    tempo_de_entrega = models.CharField(max_length=2, default=50)
    has_loja_online = models.BooleanField(default=False)
    has_cozinha = models.BooleanField(default=True)
    status_entrega_gratis = models.BooleanField(default=False)
    blocked_cozinha = models.BooleanField(default=False)
    has_fixos = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.plano

    def __unicode__(self):
        return "%s" % self.plano


class Motorista(TimeStamped, BaseAddress):
    configuration = models.OneToOneField(Configuration, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    cpf = models.CharField(max_length=100, blank=True, null=True, default="")
    photo = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    ocupado = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    placa = models.CharField(max_length=30, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    creditos_expirados = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            address = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            pto = geocode(address)
            self.lat = pto['latitude']
            self.lng = pto['longitude']
        except (Exception,):
            pass
        super(Motorista, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name

    def __unicode__(self):
        return u'%s' % self.user.first_name


class ConfigAdmin(TimeStamped):
    class Meta:
        verbose_name = u'Configuração do Sistema'
        verbose_name_plural = u'Configuração do Sistema'

    is_feriado = models.BooleanField(default=False)
    is_promo = models.BooleanField(default=False)
    start_promo = models.DateField(blank=True, null=True)
    end_promo = models.DateField(blank=True, null=True)

    def __str__(self):
        return u'Configuração Sistema'

    def __unicode__(self):
        return u'Configuração Sistema'


class Estabelecimento(TimeStamped, BaseAddress):
    configuration = models.OneToOneField(Configuration, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    is_approved = models.BooleanField(default=False)
    photo = models.URLField(blank=True, null=True)
    cnpj = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    is_online = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    full_address = models.CharField(max_length=300, blank=True, null=True)
    motoboys = models.ManyToManyField(Motorista, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            self.numero = self.numero.replace("_", "")
            self.phone = self.phone.replace("_", "")
            address = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            self.full_address = address
            pto = geocode(address)
            self.lat = pto['latitude']
            self.lng = pto['longitude']
        except (Exception,):
            pass
        super(Estabelecimento, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.user.first_name

    def __str__(self):
        return u'%s' % self.user.first_name

    class Meta:
        permissions = (
            ("view_dashboard_1", "Loja pode ver o dashboard loja tipo 1"),
            ("view_dashboard_2", "Loja pode ver o dashboard loja tipo 2"),
            ("view_dashboard_3", "Loja pode ver o dashboard loja tipo 3"),
            ("view_chat", "Loja pode interagir no Chat"),
        )


class Pedido(TimeStamped):
    class Meta:
        verbose_name = u'Rota'
        verbose_name_plural = u'Rotas'

    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    coletado = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    status_cozinha = models.BooleanField(default=False)
    valor_total = models.TextField()
    btn_finalizado = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False, )
    motorista = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    distance = models.CharField(max_length=100, blank=True, null=True)
    chamar_motoboy = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s - %s' % (self.estabelecimento, self.valor_total)

    def __str__(self):
        return u'%s - %s' % (self.estabelecimento, self.valor_total)

    def save(self, *args, **kwargs):
        config = ConfigAdmin.objects.first()
        valor = 0
        for pto in self.ponto_set.all():
            # now = datetime.now()
            # now_time = now.time()
            now_time = pto.created_at.time()
            if config.is_feriado:
                if time(22, 59) <= now_time <= time(23, 59):
                    valor = valor + int(pto.bairro.valor_madrugada_feriado)
                elif time(0, 00) <= now_time <= time(5, 59):
                    valor = valor + int(pto.bairro.valor_madrugada_feriado)
                else:
                    valor = valor + int(pto.bairro.valor_feriado)
            else:
                if time(22, 59) <= now_time <= time(23, 59):
                    valor = valor + int(pto.bairro.valor_madrugada)
                elif time(0, 00) <= now_time <= time(5, 59):
                    valor = valor + int(pto.bairro.valor_madrugada)
                else:
                    valor = valor + int(pto.bairro.valor)
        self.valor_total = valor
        super(Pedido, self).save(*args, **kwargs)


class Ponto(BaseAddress, TimeStamped):
    class Meta:
        verbose_name = u'Ponto de Entrega'
        verbose_name_plural = u'Pontos de Entrega'

    cliente = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True, null=True)
    estabelecimento = models.ForeignKey(Estabelecimento, blank=True, null=True)
    full_address = models.CharField(max_length=300, blank=True, null=True)
    status = models.BooleanField(default=False)
    duration = models.CharField(max_length=100, blank=True, null=True)
    distance = models.CharField(max_length=100, blank=True, null=True)
    itens = models.TextField(blank=True, null=True)
    is_prepared = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            self.numero = self.numero.replace("_", "")
            self.telefone = self.telefone.replace("_", "")
            address = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            pto = geocode(address)
            self.lat = pto['latitude']
            self.lng = pto['longitude']
        except (Exception,):
            pass
        self.full_address = address
        super(Ponto, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.endereco

    def __str__(self):
        return self.endereco


type_notification = (
    ('NOTIFICACAO_COZINHA', 'NOTIFICACAO_COZINHA'),
    ('NOVO_PEDIDO', 'NOVO_PEDIDO'),
    ('DELETE_LOJA', 'DELETE_LOJA'),
    ('ACCEPT_ORDER', 'ACCEPT_ORDER'),
    ('CANCEL_ORDER', 'CANCEL_ORDER'),
    ('ENABLE_ROTA', 'ENABLE_ROTA'),
    ('ORDER_DELIVERED', 'ORDER_DELIVERED'),
    ('ADMIN_MESSAGE', 'ADMIN_MESSAGE'),
    ('ALL_DELIVERED', 'ALL_DELIVERED'),
    ('LOJA_MESSAGE', 'LOJA_MESSAGE'),
    ('MOTORISTA_MESSAGE', 'MOTORISTA_MESSAGE')
)


class Notification(TimeStamped):
    message = models.TextField()
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    type_message = models.CharField(choices=type_notification, max_length=100)
    is_read = models.BooleanField(default=False)


class Message(TimeStamped):
    u_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_from')
    u_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_to')
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)


class Location(TimeStamped):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)


class Classification(TimeStamped):
    class Meta:
        verbose_name = u'Avaliação Motorista'
        verbose_name_plural = u'Avaliações Motorista'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    nota = models.CharField(max_length=2)


class Cliente(TimeStamped, ):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    cpf = models.CharField(max_length=12, blank=True, null=True, default="")
    foto = models.URLField(blank=True, null=True, default="http://placehold.it/100x100")
    telefone = models.CharField(max_length=30, blank=True, null=True)
    is_online = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return u'%s %s' % (self.usuario.first_name, self.usuario.last_name)

    def __unicode__(self):
        return u'%s %s' % (self.usuario.first_name, self.usuario.last_name)


class Endereco(TimeStamped, BaseAddress):
    class Meta:
        verbose_name = u'Endereço de Cliente'
        verbose_name_plural = u'Endereços de Cliente'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    endereco_completo = models.CharField(max_length=300, blank=True, null=True)
    valor_entrega = models.TextField(blank=True, null=True, default='6')

    def save(self, *args, **kwargs):
        config = ConfigAdmin.objects.first()
        valor = 0
        now_time = datetime.now().time()
        if config.is_feriado:
            if time(22, 59) <= now_time <= time(23, 59):
                valor = valor + int(self.bairro.valor_madrugada_feriado)
            elif time(0, 00) <= now_time <= time(5, 59):
                valor = valor + int(self.bairro.valor_madrugada_feriado)
            else:
                valor = valor + int(self.bairro.valor_feriado)
        else:
            if time(22, 59) <= now_time <= time(23, 59):
                valor = valor + int(self.bairro.valor_madrugada)
            elif time(0, 00) <= now_time <= time(5, 59):
                valor = valor + int(self.bairro.valor_madrugada)
            else:
                valor = valor + int(self.bairro.valor)
        self.valor_entrega = valor
        try:
            endereco = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            self.endereco_completo = endereco
            pto = geocode(endereco)
            self.lat = pto['latitude']
            self.lng = pto['longitude']
        except (Exception,):
            endereco = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            self.endereco_completo = endereco
        super(Endereco, self).save(*args, **kwargs)

    def __str__(self):
        return u'%s' % self.endereco_completo

    def __unicode__(self):
        return u'%s' % self.endereco_completo


class Categoria(TimeStamped):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    disponibilidade = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.nome

    def __str__(self):
        return u'%s' % self.nome


class Produto(TimeStamped):
    nome = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(default="", blank=True, null=True)
    preco_base = models.CharField(max_length=10, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    disponivel = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.nome

    def __str__(self):
        return u'%s' % self.nome


class Grupo(TimeStamped):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    limitador = models.CharField(max_length=2, default='1')
    obrigatoriedade = models.BooleanField(default=False)
    tipo = models.CharField(max_length=100, default='radio')
    disponivel = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.identificador

    def __str__(self):
        return u'%s' % self.identificador

    def save(self, *args, **kwargs):
        try:
            if int(self.limitador) == 1:
                self.tipo = 'radio'
            else:
                self.tipo = 'checkbox'
        except (Exception,):
            self.tipo = ' '
        super(Grupo, self).save(*args, **kwargs)


class Opcional(TimeStamped):
    class Meta:
        verbose_name = u'Opcional'
        verbose_name_plural = u'Opcionais'

    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300, blank=True, null=True)
    grupo = models.ForeignKey(Grupo, blank=True, null=True, on_delete=models.CASCADE)
    valor = models.TextField()
    disponivel = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.nome

    def __str__(self):
        return u'%s' % self.nome

    def save(self, *args, **kwargs):
        self.valor = float(str(self.valor).replace(',', '.'))
        super(Opcional, self).save(*args, **kwargs)


class FotoProduto(TimeStamped):
    class Meta:
        verbose_name = u'Foto de Produto'
        verbose_name_plural = u'Foto de Produtos'

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    url = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.url

    def __str__(self):
        return u'%s' % self.url

    def save(self, *args, **kwargs):
        try:
            CLIENT_ID = "cdadf801dc167ab"
            bencode = b64encode(self.file.read())
            client = pyimgur.Imgur(CLIENT_ID)
            r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': bencode})
            file = r['link']
            self.url = file
        except (Exception,):
            pass
        return super(FotoProduto, self).save(*args, **kwargs)


TIPOS_PAGAMENTO = (
    ('CREDITO', 'CREDITO'),
    ('DEBITO', 'DEBITO'),
    ('DINHEIRO', 'DINHEIRO'),
    ('REFEICAO', 'REFEICAO'),
)

TIPOS_CARTAO = (
    ('MASTERCARD', 'MASTERCARD'),
    ('VISA', 'VISA'),
    ('ELO', 'ELO'),
    ('VR', 'VR'),
    ('HIPERCARD', 'HIPERCARD'),
    ('SODEXO', 'SODEXO'),
)


class FormaPagamento(TimeStamped):
    class Meta:
        verbose_name = u'Forma de Pagamento'
        verbose_name_plural = u'Formas de Pagamento'

    forma = models.CharField(max_length=100, choices=TIPOS_PAGAMENTO, blank=True, null=True, default="DINHEIRO")
    cartao = models.CharField(max_length=100, choices=TIPOS_CARTAO, blank=True, null=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.forma

    def __str__(self):
        return u'%s' % self.forma


TIPOS_ENTREGA = (
    ('VOU BUSCAR', 'VOU BUSCAR'),
    ('MOTOBOY', 'MOTOBOY'),
)


class FormaEntrega(TimeStamped):
    class Meta:
        verbose_name = u'Forma de Entrega'
        verbose_name_plural = u'Formas de Entrega'

    forma = models.CharField(max_length=100, choices=TIPOS_ENTREGA, blank=True, null=True, default="MOTOBOY")
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.forma

    def __str__(self):
        return u'%s' % self.forma


STATUS = (
    ('AGUARDANDO', 'AGUARDANDO'),
    ('ACEITO', 'ACEITO'),
    ('REJEITADO', 'REJEITADO'),
    ('PREPARANDO', 'PREPARANDO'),
    ('ENTREGANDO', 'ENTREGANDO'),
    ('ENTREGUE', 'ENTREGUE'),
)


class Request(TimeStamped):
    class Meta:
        verbose_name = u'Pedido Loja'
        verbose_name_plural = u'Pedidos Loja'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    status_pedido = models.CharField(max_length=100, choices=STATUS, blank=True, null=True, default='AGUARDANDO')
    subtotal = models.CharField(max_length=10, blank=True, null=True)
    valor_total = models.TextField(blank=True, null=True)
    troco = models.CharField(max_length=300, blank=True, null=True)
    resultado_troco = models.CharField(max_length=10, blank=True, null=True)
    forma_pagamento = models.ForeignKey(FormaPagamento, blank=True, null=True, on_delete=models.CASCADE)
    forma_entrega = models.ForeignKey(FormaEntrega, blank=True, null=True, on_delete=models.CASCADE)
    endereco_entrega = models.ForeignKey(Endereco, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s - %s - %s' % (self.id, self.cliente, self.estabelecimento, self.valor_total)

    def __str__(self):
        return u'%s - %s - %s - %s' % (self.id, self.cliente, self.estabelecimento, self.valor_total)

    def is_entrega_gratis(self, bairro, loja):
        try:
            if loja.configuration.status_entrega_gratis:
                qs = BairroGratis.objects.filter(estabelecimento=loja, bairro=bairro)
                if qs.count() > 0:
                    return True
            return False
        except (Exception,):
            return False

    def save(self, *args, **kwargs):
        subtotal = 0.0
        for item in self.itempedido_set.all():
            subtotal = float(subtotal) + float(str(item.valor_total).replace(',', '.'))
        self.subtotal = float(format(subtotal, '.2f'))
        if self.endereco_entrega:
            if not self.is_entrega_gratis(self.endereco_entrega.bairro, self.estabelecimento):
                total = float(self.subtotal) + float(str(self.endereco_entrega.valor_entrega).replace(',', '.'))
                self.valor_total = format(total, '.2f')
        else:
            self.valor_total = format(subtotal, '.2f')
        super(Request, self).save(*args, **kwargs)


class ItemPedido(TimeStamped):
    class Meta:
        verbose_name = u'Item de Pedido'
        verbose_name_plural = u'Itens de Pedido'

    pedido = models.ForeignKey(Request, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto)
    quantidade = models.CharField(max_length=10, blank=True, null=True, default="1")
    observacoes = models.TextField(blank=True, null=True)
    valor_total = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        valor_base = float(str(self.produto.preco_base).replace(',', '.').replace(" ", ""))
        valor_opcionais = 0.0
        if self.opcionalchoice_set.first():
            for opc in self.opcionalchoice_set.all():
                valor_opcionais = float(valor_opcionais) + float(str(opc.opcional.valor).replace(',', '.').replace(" ", ""))
        valor_unitario = float(valor_base) + float(valor_opcionais)
        self.valor_total = format(float(float(valor_unitario) * float(self.quantidade)), '.2f')
        super(ItemPedido, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s - %s - %s' % (self.pedido.id, self.produto, self.quantidade)

    def __str__(self):
        return u'%s - %s - %s' % (self.pedido.id, self.produto, self.quantidade)


class OpcionalChoice(TimeStamped):
    class Meta:
        verbose_name = u'Opcional Escolhido'
        verbose_name_plural = u'Opcionais Escolhidos'

    opcional = models.ForeignKey(Opcional, on_delete=models.CASCADE)
    item_pedido = models.ForeignKey(ItemPedido)

    def __unicode__(self):
        return u'%s' % self.opcional

    def __str__(self):
        return u'%s' % self.opcional


type_notification = (
    ('NOVO_PEDIDO', 'NOVO_PEDIDO'),
    ('ADMIN_MESSAGE', 'ADMIN_MESSAGE'),
)


class Notificacao(TimeStamped):
    class Meta:
        verbose_name = u'Notificação'
        verbose_name_plural = u'Notificações'

    message = models.TextField()
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    type_message = models.CharField(choices=type_notification, max_length=100)
    is_read = models.BooleanField(default=False)
    pedido = models.ForeignKey(Request, blank=True, null=True)

    def __unicode__(self):
        return u'Para: %s' % self.to

    def __str__(self):
        return u'Para: %s' % self.to


class Avaliacao(TimeStamped):
    class Meta:
        verbose_name = u'Avaliação'
        verbose_name_plural = u'Avaliações'

    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    comentario = models.CharField(max_length=300, blank=True, null=True)
    nota = models.CharField(max_length=2)

    def __unicode__(self):
        return u'Loja:%s Nota:%s' % (self.estabelecimento, self.nota)

    def __str__(self):
        return u'Loja:%s Nota:%s' % (self.estabelecimento, self.nota)


class FolhaPagamento(TimeStamped):
    class Meta:
        verbose_name = u'Pagamento'
        verbose_name_plural = u'Pagamentos'

    valor_total = models.TextField()
    valor_cobrar = models.TextField(blank=True, null=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, blank=True, null=True)
    link_pagamento = models.URLField(blank=True, null=True, default="#")
    status_pagamento = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        valor = 0.0
        for it in self.itempagamento_set.all():
            valor = float(valor) + float(it.request.valor_total)
        self.valor_total = valor
        self.valor_cobrar = float(0.07 * valor)
        return super(FolhaPagamento, self).save(*args, **kwargs)


class ItemPagamento(TimeStamped):
    class Meta:
        verbose_name = u'Item de Pagamento'
        verbose_name_plural = u'Itens de Pagamento'

    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    folha = models.ForeignKey(FolhaPagamento, on_delete=models.CASCADE)


class PagamentoMotorista(TimeStamped):
    class Meta:
        verbose_name = u'Pagamento de Motoboy'
        verbose_name_plural = u'Pagamentos de Motoboys'

    valor_total = models.TextField(default="15.00")
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE, blank=True, null=True)
    link_pagamento = models.URLField(default="#")
    status_pagamento = models.BooleanField(default=False)


class BairroGratis(TimeStamped):
    class Meta:
        verbose_name = u'Bairro Gratis'
        verbose_name_plural = u'Bairros Gratis'

    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, blank=True, null=True)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.bairro.nome)

    def __unicode__(self):
        return str(self.bairro.nome)


class Logger(TimeStamped):
    user = models.ForeignKey(User)
    what = models.CharField(max_length=300)


class Chamado(TimeStamped):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    texto = models.TextField()
