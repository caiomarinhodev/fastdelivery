# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from api.serializers import UserSerializer, BairroSerializer, ConfigurationSerializer, EstabelecimentoFullSerializer, \
    OpcionalChoiceSerializer, ItemPedidoSerializer, RequestSerializer, EnderecoSerializer, ClienteSerializer
from app.models import Bairro, Configuration, Estabelecimento, Request, ItemPedido, OpcionalChoice, Endereco, Cliente


from rest_framework.permissions import DjangoObjectPermissions


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class BairroViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bairro.objects.all().order_by('nome')
    serializer_class = BairroSerializer


class ConfigurationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer


class EstabelecimentoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Estabelecimento.objects.all().order_by('-created_at')
    serializer_class = EstabelecimentoFullSerializer


class EstabelecimentoList(generics.ListAPIView):
    queryset = Estabelecimento.objects.all()
    serializer_class = EstabelecimentoFullSerializer


class RequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class ItemPedidoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ItemPedido.objects.all().order_by('-created_at')
    serializer_class = ItemPedidoSerializer


class OpcionalChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = OpcionalChoice.objects.all().order_by('-created_at')
    serializer_class = OpcionalChoiceSerializer


class EnderecoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Endereco.objects.all().order_by('-created_at')
    serializer_class = EnderecoSerializer


@authentication_classes([])
@permission_classes([])
class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Cliente.objects.all().order_by('-created_at')
    serializer_class = ClienteSerializer


class ListMyRequests(APIView):
    """
    View to list all users in the system.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        return Request.objects.filter(endereco_entrega__isnull=False, forma_pagamento__isnull=False,
                                      cliente__usuario=self.request.user.id)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        requests = [RequestSerializer(request).data for request in
                    Request.objects.filter(endereco_entrega__isnull=False, forma_pagamento__isnull=False,
                                           cliente__usuario=request.user.id)]
        return Response(requests)


class ListMyAddress(APIView):
    """
    View to list all users in the system.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        return Endereco.objects.filter(cliente__usuario=self.request.user.id)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        enderecos = [EnderecoSerializer(endereco).data for endereco in
                     Endereco.objects.filter(cliente__usuario=self.request.user.id)]
        return Response(enderecos)
