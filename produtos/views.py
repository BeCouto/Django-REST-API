from rest_framework import viewsets
from .models import Produto, Categoria
from .serializers import ProdutoSerializer, CategoriaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Produto, Categoria
from .serializers import ProdutoSerializer, CategoriaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        # Equivalente a SELECT COUNT(*)
        total_produtos = Produto.objects.count()
        
        # Equivalente a SELECT AVG(preco)
        preco_medio = Produto.objects.aggregate(Avg('preco'))['preco__avg']
        
        # Equivalente a SELECT categoria, COUNT(id) GROUP BY categoria
        por_categoria = Produto.objects.values('categoria__nome').annotate(total=Count('id'))
        
        return Response({
            'resumo': {
                'total_produtos': total_produtos,
                'preco_medio_global': round(preco_medio, 2) if preco_medio else 0,
            },
            'distribuicao_por_categoria': por_categoria
        })