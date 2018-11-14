from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView

from app.mixins.CustomContextMixin import CustomContextMixin
from app.models import Pedido, Estabelecimento


class AcompanharListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'entrega/acompanhar/list_acompanhar_loja.html'

    def get_queryset(self):
        return Pedido.objects.filter(estabelecimento__user=self.request.user, status=False, btn_finalizado=False).order_by('-created_at')


class AcompanharDetailView(LoginRequiredMixin, DetailView, CustomContextMixin):
    model = Pedido
    template_name = 'entrega/acompanhar/acompanhar_view.html'
    context_object_name = 'pedido'


class LojasMotoristaListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Estabelecimento
    context_object_name = 'lojas'
    template_name = 'entrega/pedidos/list_all_lojas_motorista.html'

    def get_queryset(self):
        return Estabelecimento.objects.all()
