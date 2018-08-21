from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Bairro, Estabelecimento, Pedido, Configuration, Categoria, Request, \
    Produto, Grupo, Opcional, ItemPedido, OpcionalChoice, Endereco, BairroGratis, FormaPagamento, Motorista, Cliente


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')


class MotoristaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Motorista
        fields = ('id', 'configuration', 'cpf', 'photo', 'phone', 'ocupado', 'is_online', 'place', 'is_approved',
                  'creditos_expirados')


class UserMotoristaSerializer(serializers.HyperlinkedModelSerializer):
    motorista = MotoristaSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'motorista')


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ('tema', 'plano', 'has_cozinha', 'tempo_de_entrega',)


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = ('id', 'nome', 'valor', 'valor_madrugada', 'valor_madrugada_feriado', 'valor_feriado')


class BairroGratisSerializer(serializers.ModelSerializer):
    bairro = BairroSerializer()

    class Meta:
        model = BairroGratis
        fields = ('id', 'bairro',)


class FormaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPagamento
        fields = ('id', 'forma', 'cartao')


class EstabelecimentoQuickSerializer(serializers.ModelSerializer):
    configuration = ConfigurationSerializer()
    bairro = BairroSerializer()
    bairrogratis_set = BairroGratisSerializer(many=True, read_only=True)
    formapagamento_set = FormaPagamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Estabelecimento
        fields = ('id', 'user', 'configuration', 'phone', 'photo', 'is_online', 'cnpj', 'full_address', 'is_approved',
                  'bairro', 'endereco', 'numero', 'complemento', 'lat', 'lng', 'bairrogratis_set',
                  'formapagamento_set')


class CategoriaQuickSerializer(serializers.ModelSerializer):
    estabelecimento = EstabelecimentoQuickSerializer()

    class Meta:
        model = Categoria
        fields = ('id', 'nome', 'estabelecimento')


class ProdutoQuickSerializer(serializers.ModelSerializer):
    categoria = CategoriaQuickSerializer()

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'categoria', 'preco_base', 'disponivel')


class GrupoQuickSerializer(serializers.ModelSerializer):
    produto = ProdutoQuickSerializer()

    class Meta:
        model = Grupo
        fields = ('id', 'identificador', 'titulo', 'limitador', 'produto', 'obrigatoriedade', 'tipo', 'disponivel')


class OpcionalFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcional
        fields = ('id', 'nome', 'descricao', 'grupo', 'valor', 'disponivel',)


class GrupoFullSerializer(serializers.ModelSerializer):
    opcional_set = OpcionalFullSerializer(many=True, read_only=True)

    class Meta:
        model = Grupo
        fields = ('id', 'identificador', 'titulo', 'limitador', 'obrigatoriedade', 'tipo', 'disponivel',
                  'opcional_set')


class ProdutoFullSerializer(serializers.ModelSerializer):
    grupo_set = GrupoFullSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'preco_base', 'disponivel', 'grupo_set')


class CategoriaFullSerializer(serializers.ModelSerializer):
    produto_set = ProdutoFullSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ('id', 'nome', 'produto_set',)


class EstabelecimentoFullSerializer(serializers.ModelSerializer):
    configuration = ConfigurationSerializer()
    bairro = BairroSerializer()
    user = UserSerializer()
    categoria_set = CategoriaFullSerializer(many=True, read_only=True)
    bairrogratis_set = BairroGratisSerializer(many=True, read_only=True)
    formapagamento_set = FormaPagamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Estabelecimento
        fields = ('id', 'user', 'configuration', 'phone', 'photo', 'is_online', 'cnpj', 'full_address', 'is_approved',
                  'bairro', 'endereco', 'numero', 'complemento', 'lat', 'lng', 'categoria_set', 'bairrogratis_set',
                  'formapagamento_set'
                  )


class PedidoSerializer(serializers.ModelSerializer):
    estabelecimento = EstabelecimentoQuickSerializer()
    motorista = UserMotoristaSerializer()

    class Meta:
        model = Pedido
        fields = ('id',
                  'status', 'estabelecimento', 'coletado', 'is_complete', 'status_cozinha', 'valor_total',
                  'btn_finalizado',
                  'is_draft', 'motorista', 'duration', 'distance')


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            'id',
            'cliente',
            'estabelecimento',
            'status_pedido',
            'subtotal',
            'valor_total',
            'troco',
            'resultado_troco',
            'forma_pagamento',
            'endereco_entrega',
            'pedido'
        )


class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ('id', 'pedido', 'produto', 'observacoes')


class OpcionalChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionalChoice
        fields = ('id', 'opcional', 'item_pedido',)


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('id', 'cliente', 'endereco_completo', 'valor_entrega', 'endereco', 'numero', 'bairro', 'complemento')


class ClienteSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(required=True)

    class Meta:
        model = Cliente
        fields = ('id', 'usuario', 'cpf', 'foto', 'telefone', 'is_online',)

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('usuario')
        user = User.objects.create_user(**user_data)
        client, created = Cliente.objects.update_or_create(usuario=user, cpf=validated_data.pop('cpf'),
                                                           telefone=validated_data.pop('telefone'))
        return client
