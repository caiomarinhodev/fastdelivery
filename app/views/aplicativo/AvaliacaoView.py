from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView

from app.models import Request, Avaliacao


class AvaliacaoView(LoginRequiredMixin, DetailView):
    template_name = 'loja/avaliacao_cliente.html'
    login_url = '/define/login/'
    model = Request
    context_object_name = 'pedido_obj'

    def get(self, request, *args, **kwargs):
        return super(AvaliacaoView, self).get(request, *args, **kwargs)


def add_avaliacao(request):
    data = request.POST
    pedido = Request.objects.get(id=data['pedido'])
    if 'comentario' and 'nota' in data:
        aval = Avaliacao(cliente=pedido.cliente, estabelecimento=pedido.estabelecimento, nota=data['nota'],
                         comentario=data['comentario'])
        aval.save()
    else:
        messages.error(request, 'Insira uma nota e um comentario')
        return redirect('/avaliacao/pedido/' + str(data['pedido']))
    messages.success(request, 'Avaliacao Realizada com Sucesso')
    return redirect('/acompanhar-pedido/' + str(data['pedido']))
