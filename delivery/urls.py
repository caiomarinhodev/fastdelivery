"""urls.py: Urls definidas."""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework import routers

from api import views as views_api
from api.views import UserViewSet, BairroViewSet, ConfigurationViewSet, ItemPedidoViewSet, \
    OpcionalChoiceViewSet, EnderecoViewSet, RequestViewSet, ListMyRequests, ClienteViewSet, ListMyAddress
from app.views.AcompanharView import AcompanharListView, AcompanharDetailView, LojasMotoristaListView
from app.views.ChatView import ListChatView, get_chat, ChatPedidoView, submit_message, ChatMotoristaPedidoView
from app.views.ClientesView import *
from app.views.HomeView import DashboardDataView, set_feriado_admin, ListMotoristasView, DashboardListPedidosView, \
    copy_catalogo, copy_group, delete_catalogo, delete_group
from app.views.LocationView import get_position_motorista, send_position_motorista
from app.views.LoginView import LoginView, LogoutView, RegisterView, AppView, EditarPerfilView, RegisterMotoristaView, \
    SetOnlineMotoboyView
from app.views.MotoristasAtivosView import MotoristasAtivosView
from app.views.NotificationView import notificar_novo_pedido_motorista, notificar_delete_loja_motorista, \
    notificar_accept_order_loja, notificar_enable_rota_motorista, NotificacoesListView, notificar_all_delivered_loja, \
    notificar_admin_message, notificar_order_delivered_loja, notify_new_message_for_motorista, \
    notify_new_message_for_loja, notificar_cozinha_message
from app.views.PagamentoMotoboyView import PagamentoMotoboyListView
from app.views.PedidoView import PedidosMotoristaListView, \
    PedidosLojaListView, PedidoCreateView, get_pedidos_motorista, accept_corrida, \
    EntregasMotoristaListView, get_entregas_motorista, delete_pedido, liberar_corrida, OrderMotoristaDetailView, \
    RouteMotoristaDetailView, MapRouteMotoristaView, finalizar_entrega, finalizar_pedido, PedidoUpdateView, \
    cancel_pedido, \
    PedidoDetailView, avaliar_motorista, get_pedidos, buscar_cliente, PedidosMotoristaPremiumListView, CozinhaListView, \
    set_to_prepared_pedido, liberar_corrida_cozinha, select_motoboy_fixo_cozinha, select_motoboy_fixo_painel
from app.views.RelatorioView import RelatorioTemplateView, DashboardReportViewUser, TimelineView, PromocaoListView
from app.views.loja.AvaliacaoView import AvaliacaoView, add_avaliacao
from app.views.loja.CarrinhoView import add_cart, FinalizaRequest, AcompanharRequest, submit_pedido, MeusRequests, \
    remove_cart, CarrinhoReqView
from app.views.loja.HomeView import HomeView, LojaProdutosListView, SetOnlineView, script, bootstrap, SobreView
from app.views.loja.LoginView import ClienteLoginView
from app.views.loja.LoginView import EscolheLoginView, RegistroCliente
from app.views.painel.bairro_gratis.BairroGratisView import BairroGratisCreateView, BairroGratisUpdateView, \
    BairroGratisListView, BairroGratisDeleteView
from app.views.painel.categoria.CategoriaView import CategoriaCreateView
from app.views.painel.categoria.CategoriaView import CategoriaDeleteView
from app.views.painel.categoria.CategoriaView import CategoriaListView
from app.views.painel.categoria.CategoriaView import CategoriaUpdateView
from app.views.painel.chamado.ChamadoView import ChamadoCreateView
from app.views.painel.chamado.ChamadoView import ChamadoDeleteView
from app.views.painel.chamado.ChamadoView import ChamadoListView
from app.views.painel.chamado.ChamadoView import ChamadoUpdateView
from app.views.painel.classificacao.ClassificacaoView import ClassificacaoListView
from app.views.painel.dashboard.DashboardView import DashboardPedidosListView
from app.views.painel.forma_entrega.FormaEntregaView import FormaEntregaCreateView, FormaEntregaDeleteView
from app.views.painel.forma_entrega.FormaEntregaView import FormaEntregaListView
from app.views.painel.forma_entrega.FormaEntregaView import FormaEntregaUpdateView
from app.views.painel.forma_pagamento.FormaPagamentoView import FormaPagamentoCreateView
from app.views.painel.forma_pagamento.FormaPagamentoView import FormaPagamentoDeleteView
from app.views.painel.forma_pagamento.FormaPagamentoView import FormaPagamentoListView
from app.views.painel.forma_pagamento.FormaPagamentoView import FormaPagamentoUpdateView
from app.views.painel.foto_produto.FotoProdutoView import FotoProdutoCreateView, FotoProdutoDeleteView
from app.views.painel.foto_produto.FotoProdutoView import FotoProdutoListView
from app.views.painel.foto_produto.FotoProdutoView import FotoProdutoUpdateView
from app.views.painel.grupo.GrupoView import GrupoCreateView, GrupoDeleteView
from app.views.painel.grupo.GrupoView import GrupoListView
from app.views.painel.grupo.GrupoView import GrupoUpdateView
from app.views.painel.login.LoginView import LojaLoginView
from app.views.painel.login.LoginView import LojaLogoutView
from app.views.painel.notificacao.NotificacaoView import NotificacaoListView
from app.views.painel.opcional.OpcionalView import OpcionalCreateView, OpcionalListView, OpcionalDeleteView
from app.views.painel.opcional.OpcionalView import OpcionalUpdateView
from app.views.painel.pagamento.PagamentoView import PagamentoListView
from app.views.painel.pedido.PedidoView import aceitar_pedido, notificacao_pedido, RequestUpdateView, chamar_motoboy, \
    chamar_motoboy_cozinha, cancelar_request, RejeitarRequestView
from app.views.painel.produto.ProdutoView import ProdutoCreateView
from app.views.painel.produto.ProdutoView import ProdutoDeleteView
from app.views.painel.produto.ProdutoView import ProdutoListView
from app.views.painel.produto.ProdutoView import ProdutoUpdateView

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, LES-UFCG"

"""default URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'districts', BairroViewSet, base_name='districts')
router.register(r'configurations', ConfigurationViewSet, base_name='configurations')
router.register(r'requests', RequestViewSet, base_name='requests')
router.register(r'items', ItemPedidoViewSet, base_name='items')
router.register(r'optionals', OpcionalChoiceViewSet, base_name='optionals')
router.register(r'addresses', EnderecoViewSet, base_name='addresses')
router.register(r'clients', ClienteViewSet, base_name='clients')

url_api = [
    url(r'^stores/$', views_api.EstabelecimentoList.as_view()),
    url(r'my-requests/$', ListMyRequests.as_view()),
    url(r'my-addresses/$', ListMyAddress.as_view()),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/login/$', auth_views.login),
    url(r'^$', AppView.as_view(), name='home'),
    url(r'^app/dashboard/data/$', DashboardDataView.as_view(), name='dashboard-data'),
    url(r'^app/dashboard/$', DashboardListPedidosView.as_view(), name='dashboard-admin'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^app/registro/$', RegisterView.as_view(), name='registro'),
    url(r'^app/register-driver/$', RegisterMotoristaView.as_view(), name='register-driver'),

    url(r'^account/logout/$', LogoutView.as_view(), name='auth_logout_motorista'),

    url(r'^app/pedidos/motorista/$', PedidosMotoristaListView.as_view(), name='pedidos_motorista'),
    url(r'^app/pedidos/loja/$', PedidosLojaListView.as_view(), name='pedidos_estabelecimento'),
    url(r'^app/pedidos/add/$', PedidoCreateView.as_view(), name='add_pedido'),
    url(r'^app/pedidos/(?P<pk>[0-9]+)/delete/$', delete_pedido, name='delete_pedido'),
    url(r'^app/pedidos/(?P<pk>[0-9]+)/cancel/$', cancel_pedido, name='cancel_pedido'),
    url(r'^app/pedido/(?P<pk>[0-9]+)/edit/$', PedidoUpdateView.as_view(), name="edit_pedido_view"),
    url(r'^app/pedido/(?P<pk>[0-9]+)/view/$', PedidoDetailView.as_view(), name="view_pedido_view"),
    url(r'^app/pedido/(?P<pk>[0-9]+)/$', OrderMotoristaDetailView.as_view(), name="order_pedido_view"),
    url(r'^app/pedido/route/(?P<pk>[0-9]+)/$', RouteMotoristaDetailView.as_view(), name="route_pedido_view"),
    url(r'^app/pedido/map/route/(?P<pk>[0-9]+)/$', MapRouteMotoristaView.as_view(), name="map_route_pedido_view"),
    url(r'^app/pedidos/motoristas/loja/$', MotoristasAtivosView.as_view(), name='motoristas_ativos_view'),
    url(r'^app/chats/all/$', ListChatView.as_view(), name='list_all_chats'),
    url(r'^app/chat/(?P<pk>[0-9]+)/$', ChatPedidoView.as_view(), name='chat_view'),
    url(r'^app/chat/motorista/$', ChatMotoristaPedidoView.as_view(), name='chat_motorista_view'),
    url(r'^app/pedidos/motorista/premium/$', PedidosMotoristaPremiumListView.as_view(),
        name='pedidos_motorista_premium'),

    url(r'^app/cozinha/$', CozinhaListView.as_view(), name='cozinha_view'),
    url(r'^app/cozinha/prepared/(?P<id_ponto>[0-9]+)/$', set_to_prepared_pedido, name='set_prepared_entrega'),
    url(r'^app/liberar-corrida-cozinha/(?P<pk_pedido>[0-9]+)/', liberar_corrida_cozinha,
        name='liberar_corrida_cozinha'),

    url(r'^app/motorista/timeline/$', TimelineView.as_view(), name='timeline_motorista'),

    url(r'^app/motorista/promocoes/$', PromocaoListView.as_view(), name='promocoes'),

    url(r'^app/clientes/(?P<pk>[0-9]+)/edit/$', ClienteUpdateView.as_view(), name="edit_clientes"),
    url(r'^app/clientes/add/$', ClienteCreateView.as_view(), name="add_clientes"),
    url(r'^app/clientes/$', ClientesListView.as_view(), name="clientes"),

    url(r'^app/perfil/edit/$', EditarPerfilView.as_view(), name="edit_perfil_view"),

    url(r'^app/set-feriado/$', set_feriado_admin, name="set_feriado"),

    url(r'^app/relatorio/$', DashboardReportViewUser.as_view(), name="relatorio-user"),

    url(r'^app/relatorios/$', RelatorioTemplateView.as_view(), name="relatorios"),

    url(r'^app/acompanhar/(?P<pk>[0-9]+)/$', AcompanharDetailView.as_view(), name="acompanhar_pedido_view"),
    url(r'^app/acompanhar/$', AcompanharListView.as_view(), name='acompanhar_list'),
    url(r'^app/lojas/$', LojasMotoristaListView.as_view(), name='lojas_credenciadas'),

    url(r'^get-pedidos/$', get_pedidos_motorista, name="get_pedidos_motorista"),

    url(r'^accept-corrida/(?P<pk_pedido>[0-9]+)/$', accept_corrida, name="accept_corrida"),

    url(r'^app/entregas/motorista/$', EntregasMotoristaListView.as_view(), name='entregas_motorista'),

    url(r'^get-entregas/$', get_entregas_motorista, name="get_entregas_motorista"),

    url(r'liberar-corrida/(?P<pk_pedido>[0-9]+)/$', liberar_corrida, name="liberar_corrida"),

    url(r'finalizar-entrega/(?P<pk_ponto>[0-9]+)/(?P<pk_pedido>[0-9]+)/$', finalizar_entrega, name="finalizar_entrega"),

    url(r'finalizar-pedido/(?P<pk_pedido>[0-9]+)/$', finalizar_pedido, name="finalizar_pedido"),




    url(r'send-location/(-?\d+\.\d+)/(-?\d+\.\d+)/$', send_position_motorista, name="send_position_motorista"),

    url(r'get-location/(?P<pk_user>[0-9]+)/$', get_position_motorista, name=" get_position_motorista"),

    url(r'avaliar-motorista/(\d+)/(\d+)/$', avaliar_motorista, name="avaliar_motorista"),

    url(r'get-chat/(?P<pk_pedido>[0-9]+)/$', get_chat, name="get_chat"),

    url(r'get-pedidos-pendentes/$', get_pedidos, name="get_pedidos"),

    url(r'submit-message/(?P<pk_pedido>[0-9]+)/$', submit_message, name="submit_message"),

    url(r'^buscar-cliente/$', buscar_cliente, name='buscar-cliente'),

    url(r'^app/dashboard/list-motoristas/$', ListMotoristasView.as_view(), name='list-motoristas-view'),

    url(r'^app/notificacoes/$', NotificacoesListView.as_view(), name='notificacoes'),
    url(r'^notificacao/novo-pedido/motorista/$', notificar_novo_pedido_motorista, name="notify_novo_pedido_motorista"),
    url(r'^notificacao/delete-loja/motorista/$', notificar_delete_loja_motorista, name="notify_delete_loja_motorista"),
    url(r'^notificacao/accept-order/loja/$', notificar_accept_order_loja, name="notify_accept_order_loja"),
    url(r'^notificacao/all-delivered/loja/$', notificar_all_delivered_loja, name="notificar_all_delivered_loja"),
    url(r'^notificacao/order-delivered/loja/$', notificar_order_delivered_loja, name="notificar_order_delivered_loja"),
    url(r'^notificacao/adminmessage$', notificar_admin_message, name="notify_admin_message"),
    url(r'^notificacao/enable-rota/motorista/$', notificar_enable_rota_motorista, name="notify_enable_rota_motorista"),
    url(r'^notificacao/nova-mensagem/motorista/$', notify_new_message_for_motorista,
        name="notify_new_message_for_motorista"),
    url(r'^notificacao/nova-mensagem/loja/$', notify_new_message_for_loja, name="notify_new_message_for_loja"),

    url(r'^notificacao/cozinha/loja/$', notificar_cozinha_message, name="notificacao_cozinha"),

    url(r'^set-motoboy-online/$', SetOnlineMotoboyView.as_view(), name='set_online_motoboy'),

    url(r'^pagamentos/motoboy/$', PagamentoMotoboyListView.as_view(), name='pagamento_motoboy'),
    url(r'^script/$', script, name='script_bairro'),
    url(r'^bootstrap/$', bootstrap, name='bootstrap'),

    url(r'^chamar-motoboy/(?P<pk>[0-9]+)/$', chamar_motoboy, name='chamar_motoboy'),
    url(r'^chamar-motoboy-cozinha/(?P<pk>[0-9]+)/$', chamar_motoboy_cozinha, name='chamar_motoboy_cozinha'),

    # ---------------------------------------------------------------------------------------------------

    url(r'^loja/login/$', LojaLoginView.as_view(), name='loja_login'),
    url(r'^logout/$', LojaLogoutView.as_view(), name='auth_logout'),
    url(r'^dashboard/$', DashboardPedidosListView.as_view(), name='dashboard'),

    url(r'^categoria/add/$', CategoriaCreateView.as_view(), name='add_categoria'),
    url(r'^categoria/edit/(?P<pk>[0-9]+)/$', CategoriaUpdateView.as_view(), name='edit_categoria'),
    url(r'^categoria/list/$', CategoriaListView.as_view(), name='list_categoria'),
    url(r'^categoria/delete/(?P<pk>[0-9]+)/$', CategoriaDeleteView.as_view(), name='delete_categoria'),

    url(r'^produto/add/$', ProdutoCreateView.as_view(), name='add_produto'),
    url(r'^produto/edit/(?P<pk>[0-9]+)/$', ProdutoUpdateView.as_view(), name='edit_produto'),
    url(r'^produto/list/$', ProdutoListView.as_view(), name='list_produto'),
    url(r'^produto/delete/(?P<pk>[0-9]+)/$', ProdutoDeleteView.as_view(), name='delete_produto'),

    url(r'^grupo/add/$', GrupoCreateView.as_view(), name='add_grupo'),
    url(r'^grupo/edit/(?P<pk>[0-9]+)/$', GrupoUpdateView.as_view(), name='edit_grupo'),
    url(r'^grupo/list/$', GrupoListView.as_view(), name='list_grupo'),
    url(r'^grupo/delete/(?P<pk>[0-9]+)/$', GrupoDeleteView.as_view(), name='delete_grupo'),

    url(r'^opcional/add/$', OpcionalCreateView.as_view(), name='add_opcional'),
    url(r'^opcional/edit/(?P<pk>[0-9]+)/$', OpcionalUpdateView.as_view(), name='edit_opcional'),
    url(r'^opcional/list/$', OpcionalListView.as_view(), name='list_opcional'),
    url(r'^opcional/delete/(?P<pk>[0-9]+)/$', OpcionalDeleteView.as_view(), name='delete_opcional'),

    url(r'^foto/add/$', FotoProdutoCreateView.as_view(), name='add_foto'),
    url(r'^foto/edit/(?P<pk>[0-9]+)/$', FotoProdutoUpdateView.as_view(), name='edit_foto'),
    url(r'^foto/list/$', FotoProdutoListView.as_view(), name='list_foto'),
    url(r'^foto/delete/(?P<pk>[0-9]+)/$', FotoProdutoDeleteView.as_view(), name='delete_foto'),

    url(r'^pagamento/add/$', FormaPagamentoCreateView.as_view(), name='add_pagamento'),
    url(r'^pagamento/edit/(?P<pk>[0-9]+)/$', FormaPagamentoUpdateView.as_view(), name='edit_pagamento'),
    url(r'^pagamento/list/$', FormaPagamentoListView.as_view(), name='list_pagamento'),
    url(r'^pagamento/delete/(?P<pk>[0-9]+)/$', FormaPagamentoDeleteView.as_view(), name='delete_pagamento'),

    url(r'^entrega/add/$', FormaEntregaCreateView.as_view(), name='add_entrega'),
    url(r'^entrega/edit/(?P<pk>[0-9]+)/$', FormaEntregaUpdateView.as_view(), name='edit_entrega'),
    url(r'^entrega/list/$', FormaEntregaListView.as_view(), name='list_entrega'),
    url(r'^entrega/delete/(?P<pk>[0-9]+)/$', FormaEntregaDeleteView.as_view(), name='delete_entrega'),

    url(r'^classificacao/list/$', ClassificacaoListView.as_view(), name='list_classificacao'),

    url(r'^notificacao/list/$', NotificacaoListView.as_view(), name='list_notificacao'),

    url(r'^aceitar-pedido/(?P<pk>[0-9]+)/$', aceitar_pedido, name='aceitar_pedido'),
    url(r'^rejeitar-pedido/(?P<pk>[0-9]+)/$', RejeitarRequestView.as_view(), name='rejeitar_request'),
    # url(r'^rejeitar-pedido-cozinha/(?P<pk>[0-9]+)/$', RejeitarPedidoCozinhaView.as_view(),
    #     name='rejeitar_pedido_cozinha'),
    url(r'^cancelar-pedido/(?P<pk>[0-9]+)/$', cancelar_request, name='cancelar_request'),

    url(r'^loja/$', HomeView.as_view(), name='home'),

    url(r'^loja/(?P<pk>[0-9]+)/$', LojaProdutosListView.as_view(), name='view_loja'),

    url(r'^define/login/$', EscolheLoginView.as_view(), name='choose_login'),
    url(r'^login/cliente/$', ClienteLoginView.as_view(), name='login_cliente'),
    url(r'^registro/cliente', RegistroCliente.as_view(), name='registro_cliente'),

    url(r'^add-cart/(?P<id_loja>[0-9]+)/$', add_cart, name='add_cart'),
    url(r'finaliza-pedido/$', FinalizaRequest.as_view(), name='finaliza_pedido'),
    url(r'carrinho/$', CarrinhoReqView.as_view(), name="meu-carrinho"),
    url(r'acompanhar-pedido/(?P<pk>[0-9]+)/$', AcompanharRequest.as_view(), name='acompanhar_pedido'),
    url(r'submit-pedido/$', submit_pedido, name='submit_pedido'),
    url(r'^notificacao/pedido/$', notificacao_pedido, name="notificacao_pedido"),
    url(r'^delete-pedido/(?P<pk>[0-9]+)/$', remove_cart, name='delete_request'),
    url(r'meus-pedidos/$', MeusRequests.as_view(), name='meus_pedidos'),

    url(r'set-online/$', SetOnlineView.as_view(), name='set_online'),

    url(r'request/(?P<pk>[0-9]+)/$', RequestUpdateView.as_view(), name='edit_request'),
    url(r'folhapagamento/list/$', PagamentoListView.as_view(), name='list_folhapagamento'),

    url(r'^bairro/add/$', BairroGratisCreateView.as_view(), name='add_bairro_gratis'),
    url(r'^bairro/edit/(?P<pk>[0-9]+)/$', BairroGratisUpdateView.as_view(), name='edit_bairro_gratis'),
    url(r'^bairro/list/$', BairroGratisListView.as_view(), name='list_bairro_gratis'),
    url(r'^bairro/delete/(?P<pk>[0-9]+)/$', BairroGratisDeleteView.as_view(), name='delete_bairro_gratis'),

    url(r'^avaliacao/pedido/(?P<pk>[0-9]+)$', AvaliacaoView.as_view(), name='add_avaliacao'),
    url(r'^add-avaliacao/pedido/$', add_avaliacao, name='add_avaliacao_cliente'),

    url(r'^chamado/add/$', ChamadoCreateView.as_view(), name='add_chamado'),
    url(r'^chamado/edit/(?P<pk>[0-9]+)/$', ChamadoUpdateView.as_view(), name='edit_chamado'),
    url(r'^chamado/list/$', ChamadoListView.as_view(), name='list_chamados'),
    url(r'^chamado/delete/(?P<pk>[0-9]+)/$', ChamadoDeleteView.as_view(), name='delete_chamado'),

    url('', include('pwa.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^sobre/$', SobreView.as_view(), name='about'),

    url(r'^ativar-motoboy/(?P<pk>[0-9]+)/$', select_motoboy_fixo_cozinha, name='ativar_motoboy'),

    url(r'^ativar-motoboy-painel/(?P<pk>[0-9]+)/$', select_motoboy_fixo_painel, name='ativar_motoboy_painel'),

    url(r'^copiar-catalogo/$', copy_catalogo, name='copiar_catalogo'),
    url(r'^copiar-grupo/$', copy_group, name='copiar_grupo'),
    url(r'^deletar-catalogo/$', delete_catalogo, name='deletar_catalogo'),
    url(r'^deletar-grupo/$', delete_group, name='deletar_grupo'),
]

urlpatterns += router.urls

urlpatterns += url_api
