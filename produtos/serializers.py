from rest_framework import serializers
from .models import Produto, Categoria, Pedido, ItemPedido

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'imagem', 'atributos_extras', 
                  'data_criacao', 'categoria', 'categoria_nome']

    def validate_preco(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço de um produto deve ser estritamente maior que zero.")
        return value
        
    def validate_nome(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("O nome do produto deve ter pelo menos 3 caracteres.")
        return value

class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    
    class Meta:
        model = ItemPedido
        fields = ['id', 'pedido', 'produto', 'produto_nome', 'quantidade', 'preco_unitario']

    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value

    def validate_preco_unitario(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço unitário deve ser maior que zero.")
        return value

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(read_only=True, many=True, source='itens')
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Pedido
        fields = ['id', 'data_pedido', 'status', 'itens', 'total']
        read_only_fields = ['data_pedido']

    def get_total(self, obj):
        """Calcula o total do pedido somando (quantidade * preco_unitario)"""
        return sum(item.quantidade * item.preco_unitario for item in obj.itens.all())