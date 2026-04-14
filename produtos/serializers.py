from rest_framework import serializers
from .models import Produto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'imagem', 'data_criacao', 'categoria']

    def validate_preco(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço de um produto deve ser estritamente maior que zero.")
        return value
        
    def validate_nome(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("O nome do produto deve ter pelo menos 3 caracteres.")
        return value