from django.contrib import admin

from app.models import *

"""
admin.py: Definicao de classes para gerenciar no painel de admin do Django.
"""
__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, LES-UFCG"


class PontoInline(admin.TabularInline):
    model = Ponto


class MotoristaAdmin(admin.ModelAdmin):
    search_fields = (
        'user__first_name',
    )
    list_display = (
        'id', 'user', 'nome_completo', 'cpf', 'phone', 'is_online', 'placa', 'is_approved', 'creditos_expirados',
        'ocupado', 'photo', 'created_at')

    def nome_completo(self, obj):
        return obj.user.first_name


class EstabelecimentoAdmin(admin.ModelAdmin):
    search_fields = (
        'user__first_name',
    )
    list_display = ('user', 'nome_loja', 'phone', 'cnpj', 'id', 'full_address', 'photo', 'is_online', 'created_at')

    def nome_loja(self, obj):
        return obj.user.first_name


class PontoAdmin(admin.ModelAdmin):
    list_filter = ('bairro',)
    search_fields = (
        'telefone',
    )
    list_display = (
        'id', 'cliente', 'telefone', 'endereco', 'numero', 'bairro', 'created_at', 'status', 'duration', 'distance')


class FolhaPagamentoAdmin(admin.ModelAdmin):
    list_filter = ('estabelecimento', 'status_pagamento',)
    search_fields = (
        'estabelecimento__user__first_name',
    )
    list_display = ('id', 'loja', 'valor_total', 'valor_cobrar', 'link_pagamento', 'status_pagamento', 'created_at',)

    def loja(self, obj):
        return str(obj.estabelecimento)


class ItemPagamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'loja', 'request', 'folha', 'created_at',)

    def loja(self, obj):
        return str(obj.request.estabelecimento)


class PagamentoMotoristaAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor_total', 'motorista', 'link_pagamento', 'created_at')


class LoggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'what', 'id', 'created_at')


class PedidoAdmin(admin.ModelAdmin):
    search_fields = (
        'estabelecimento__user__first_name',
    )
    inlines = [
        PontoInline,
    ]
    list_display = ('estabelecimento',
                    'id', 'motorista', 'valor_total', 'status', 'is_complete', 'coletado', 'duration', 'distance',
                    'created_at')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'type_message', 'to', 'is_read')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'lat', 'lng', 'created_at')


class BairroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'valor_madrugada', 'valor_feriado', 'valor_madrugada_feriado', 'id')


class BairroGratisAdmin(admin.ModelAdmin):
    list_display = ('id', 'estabelecimento', 'bairro')


class ConfigAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_feriado',)


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('tema', 'id', 'plano',)


class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'nota', 'pedido')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('u_from', 'u_to', 'pedido', 'id', 'is_read', 'created_at')


admin.site.register(Motorista, MotoristaAdmin)
admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(Ponto, PontoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Bairro, BairroAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ConfigAdmin, ConfigAdminAdmin)
admin.site.register(Configuration, ConfigurationAdmin)

admin.site.register(FolhaPagamento, FolhaPagamentoAdmin)
admin.site.register(ItemPagamento, ItemPagamentoAdmin)
admin.site.register(PagamentoMotorista, PagamentoMotoristaAdmin)
admin.site.register(Logger, LoggerAdmin)

admin.site.register(BairroGratis, BairroGratisAdmin)


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido


class GrupoInline(admin.TabularInline):
    model = Grupo


class OpcionalInline(admin.TabularInline):
    model = Opcional


class EnderecoInline(admin.TabularInline):
    model = Endereco


class OpcionalChoiceInline(admin.TabularInline):
    model = OpcionalChoice


class OpcionalChoiceAdmin(admin.ModelAdmin):
    list_display = ('opcional', 'item_pedido', 'created_at', 'id')


class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'pedido', 'produto', 'quantidade', 'valor_total', 'cliente', 'estabelecimento',)
    inlines = [OpcionalChoiceInline, ]

    def cliente(self, obj):
        return obj.pedido.cliente

    def estabelecimento(self, obj):
        return obj.pedido.estabelecimento


class FotoProdutoInline(admin.TabularInline):
    model = FotoProduto


class FotoProdutoAdmin(admin.ModelAdmin):
    list_display = ('url', 'produto', 'id', 'estabelecimento', 'created_at')

    def estabelecimento(self, obj):
        return obj.produto.categoria.estabelecimento


class ClienteAdmin(admin.ModelAdmin):
    search_fields = (
        'telefone',
    )
    inlines = [EnderecoInline, ]
    list_display = (
        'id', 'usuario', 'qtd_pedidos', 'nome_cliente', 'telefone', 'email_cliente', 'is_online',
        'created_at')

    def email_cliente(self, obj):
        return obj.usuario.email

    def qtd_pedidos(self, obj):
        return obj.request_set.all()

    def nome_cliente(self, obj):
        return obj.usuario.first_name


class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'endereco', 'numero', 'bairro', 'complemento')


class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'nome_loja', 'cnpj', 'usuario', 'telefone', 'endereco_completo', 'is_online', 'created_at',
        'esta_aprovada')

    def nome_loja(self, obj):
        return obj.usuario.first_name


class RequestAdmin(admin.ModelAdmin):
    list_filter = ('status_pedido', 'endereco_entrega__bairro')
    search_fields = (
        'cliente__usuario__first_name',
    )
    inlines = [
        ItemPedidoInline,
    ]
    list_display = (
        'cliente', 'estabelecimento', 'status_pedido', 'subtotal', 'valor_total', 'troco', 'id', 'endereco_entrega',
        'forma_pagamento', 'forma_entrega', 'created_at')


class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'type_message', 'to', 'is_read')


class BairroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'valor_madrugada', 'valor_feriado', 'valor_madrugada_feriado', 'id')


class GrupoAdmin(admin.ModelAdmin):
    list_filter = ('produto__categoria__estabelecimento', 'obrigatoriedade')
    search_fields = (
        'identificador',
    )
    list_display = (
        'identificador', 'id', 'titulo', 'produto', 'limitador', 'created_at', 'obrigatoriedade',
        'disponivel')
    inlines = [OpcionalInline, ]


class ProdutoInline(admin.TabularInline):
    model = Produto


class CategoriaAdmin(admin.ModelAdmin):
    list_filter = ('estabelecimento', 'disponibilidade')
    search_fields = (
        'nome',
    )
    inlines = [
        ProdutoInline,
    ]
    list_display = ('nome', 'produtos_relacionados', 'id', 'estabelecimento', 'created_at',)

    def produtos_relacionados(self, obj):
        return obj.produto_set.count()


class ProdutoAdmin(admin.ModelAdmin):
    list_filter = ('categoria__estabelecimento', 'disponivel')
    search_fields = (
        'nome',
    )
    inlines = [
        FotoProdutoInline,
        GrupoInline,
    ]
    list_display = ('nome', 'id', 'preco_base', 'categoria', 'created_at', 'estabelecimento', 'disponivel')

    def estabelecimento(self, obj):
        try:
            return obj.categoria.estabelecimento
        except (Exception,):
            return None


class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'comentario', 'nota', 'cliente', 'estabelecimento', 'created_at')


class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('forma', 'cartao', 'id', 'estabelecimento', 'created_at',)


class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estabelecimento', 'titulo', 'texto', 'created_at')


class FormaEntregaAdmin(admin.ModelAdmin):
    list_display = ('forma', 'id', 'estabelecimento', 'created_at',)


class OpcionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'id', 'produto', 'valor', 'estabelecimento', 'created_at', 'disponivel')

    def estabelecimento(self, obj):
        return obj.grupo.produto.categoria.estabelecimento

    def produto(self, obj):
        return obj.grupo.produto


admin.site.register(Avaliacao, AvaliacaoAdmin)
admin.site.register(ItemPedido, ItemPedidoAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Notificacao, NotificacaoAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(FotoProduto, FotoProdutoAdmin)
admin.site.register(FormaPagamento, FormaPagamentoAdmin)
admin.site.register(FormaEntrega, FormaEntregaAdmin)
admin.site.register(OpcionalChoice, OpcionalChoiceAdmin)
admin.site.register(Opcional, OpcionalAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Endereco, EnderecoAdmin)

admin.site.register(Chamado, ChamadoAdmin)
