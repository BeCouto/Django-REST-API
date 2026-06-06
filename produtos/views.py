from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from .models import Produto, Categoria, Pedido, ItemPedido
from .serializers import (ProdutoSerializer, CategoriaSerializer, 
                          PedidoSerializer, ItemPedidoSerializer)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas gerais de produtos"""
        total_produtos = Produto.objects.count()
        preco_medio = Produto.objects.aggregate(Avg('preco'))['preco__avg']
        por_categoria = Produto.objects.values('categoria__nome').annotate(total=Count('id'))
        
        return Response({
            'resumo': {
                'total_produtos': total_produtos,
                'preco_medio_global': round(preco_medio, 2) if preco_medio else 0,
            },
            'distribuicao_por_categoria': por_categoria
        })

    @action(detail=False, methods=['get'])
    def filtrar_por_json(self, request):
        """
        Filtra produtos por atributos JSON (marca, ram_gb, cor, cpu, armazenamento, etc.)
        
        Exemplos:
        - ?marca=Dell
        - ?ram_gb=16
        - ?cor=preto
        - ?cpu=i7
        - ?armazenamento=512GB SSD
        - ?marca=Dell&ram_gb=16  (múltiplos filtros)
        """
        marca = request.query_params.get('marca')
        ram_gb = request.query_params.get('ram_gb')
        cor = request.query_params.get('cor')
        cpu = request.query_params.get('cpu')
        armazenamento = request.query_params.get('armazenamento')
        
        queryset = Produto.objects.all()
        filtros_aplicados = {}
        
        # Filtrar por marca (ex: ?marca=Dell)
        if marca:
            queryset = queryset.filter(atributos_extras__marca__icontains=marca)
            filtros_aplicados['marca'] = marca
        
        # Filtrar por RAM (ex: ?ram_gb=16)
        if ram_gb:
            try:
                ram_valor = int(ram_gb)
                queryset = queryset.filter(atributos_extras__ram_gb=ram_valor)
                filtros_aplicados['ram_gb'] = ram_gb
            except ValueError:
                return Response(
                    {'erro': 'ram_gb deve ser um número inteiro'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Filtrar por cor (ex: ?cor=preto)
        if cor:
            queryset = queryset.filter(atributos_extras__cor__icontains=cor)
            filtros_aplicados['cor'] = cor
        
        # Filtrar por CPU (ex: ?cpu=i7)
        if cpu:
            queryset = queryset.filter(atributos_extras__especificacoes__cpu__icontains=cpu)
            filtros_aplicados['cpu'] = cpu
        
        # Filtrar por armazenamento (ex: ?armazenamento=512GB SSD)
        if armazenamento:
            queryset = queryset.filter(atributos_extras__especificacoes__armazenamento__icontains=armazenamento)
            filtros_aplicados['armazenamento'] = armazenamento
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'filtros_aplicados': filtros_aplicados,
            'total_resultados': queryset.count(),
            'resultados': serializer.data
        })

    @action(detail=False, methods=['get'])
    def filtro_combinado(self, request):
        """
        Filtro combinado: categoria + preço + atributos JSON
        
        Exemplos:
        - ?categoria_id=1&marca=Dell&preco_min=1000&preco_max=3000
        - ?categoria_id=2&ram_gb=8&preco_min=500
        - ?marca=Samsung&cor=preto&preco_max=2000
        """
        categoria_id = request.query_params.get('categoria_id')
        marca = request.query_params.get('marca')
        preco_min = request.query_params.get('preco_min')
        preco_max = request.query_params.get('preco_max')
        ram_gb = request.query_params.get('ram_gb')
        cpu = request.query_params.get('cpu')
        
        queryset = Produto.objects.all()
        filtros_aplicados = {}
        
        # Filtrar por categoria (ex: ?categoria_id=1)
        if categoria_id:
            try:
                cat_id = int(categoria_id)
                queryset = queryset.filter(categoria__id=cat_id)
                filtros_aplicados['categoria_id'] = categoria_id
            except ValueError:
                return Response(
                    {'erro': 'categoria_id deve ser um número inteiro'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Filtrar por marca no JSON
        if marca:
            queryset = queryset.filter(atributos_extras__marca__icontains=marca)
            filtros_aplicados['marca'] = marca
        
        # Filtrar por RAM
        if ram_gb:
            try:
                ram_valor = int(ram_gb)
                queryset = queryset.filter(atributos_extras__ram_gb=ram_valor)
                filtros_aplicados['ram_gb'] = ram_gb
            except ValueError:
                return Response(
                    {'erro': 'ram_gb deve ser um número inteiro'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Filtrar por CPU
        if cpu:
            queryset = queryset.filter(atributos_extras__especificacoes__cpu__icontains=cpu)
            filtros_aplicados['cpu'] = cpu
        
        # Filtrar por faixa de preço
        if preco_min:
            try:
                preco_minimo = float(preco_min)
                queryset = queryset.filter(preco__gte=preco_minimo)
                filtros_aplicados['preco_min'] = preco_min
            except ValueError:
                return Response(
                    {'erro': 'preco_min deve ser um número'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if preco_max:
            try:
                preco_maximo = float(preco_max)
                queryset = queryset.filter(preco__lte=preco_maximo)
                filtros_aplicados['preco_max'] = preco_max
            except ValueError:
                return Response(
                    {'erro': 'preco_max deve ser um número'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'filtros_aplicados': filtros_aplicados,
            'total_resultados': queryset.count(),
            'resultados': serializer.data
        })

    @action(detail=False, methods=['get'])
    def buscar_por_especificacoes(self, request):
        """
        Busca avançada em atributos JSON aninhados (especificações técnicas)
        
        Exemplos:
        - ?cpu=i7&armazenamento=512GB  (CPU i7 E armazenamento 512GB)
        - ?cpu=i9  (apenas CPU i9)
        """
        cpu = request.query_params.get('cpu')
        armazenamento = request.query_params.get('armazenamento')
        gpu = request.query_params.get('gpu')
        
        queryset = Produto.objects.all()
        filtros_aplicados = {}
        
        if cpu:
            queryset = queryset.filter(atributos_extras__especificacoes__cpu__icontains=cpu)
            filtros_aplicados['cpu'] = cpu
        
        if armazenamento:
            queryset = queryset.filter(atributos_extras__especificacoes__armazenamento__icontains=armazenamento)
            filtros_aplicados['armazenamento'] = armazenamento
        
        if gpu:
            queryset = queryset.filter(atributos_extras__especificacoes__gpu__icontains=gpu)
            filtros_aplicados['gpu'] = gpu
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'titulo': 'Busca por Especificações Técnicas',
            'filtros_aplicados': filtros_aplicados if filtros_aplicados else {'aviso': 'Nenhum filtro aplicado'},
            'total_resultados': queryset.count(),
            'resultados': serializer.data
        })

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    @action(detail=False, methods=['get'])
    def por_status(self, request):
        """Retorna pedidos filtrados por status"""
        status_filtro = request.query_params.get('status', 'Pendente')
        pedidos = Pedido.objects.filter(status=status_filtro)
        serializer = self.get_serializer(pedidos, many=True)
        return Response({
            'status_filtrado': status_filtro,
            'total_pedidos': pedidos.count(),
            'pedidos': serializer.data
        })

    @action(detail=True, methods=['patch'])
    def atualizar_status(self, request, pk=None):
        """Atualiza o status de um pedido específico"""
        pedido = self.get_object()
        novo_status = request.data.get('status')
        
        if novo_status:
            pedido.status = novo_status
            pedido.save()
            serializer = self.get_serializer(pedido)
            return Response({
                'mensagem': f'Pedido {pedido.id} atualizado para {novo_status}',
                'pedido': serializer.data
            })
        
        return Response(
            {'erro': 'Campo status é obrigatório'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def resumo(self, request):
        """Retorna resumo dos pedidos (total, média, quantidade)"""
        total_pedidos = Pedido.objects.count()
        pedidos_pendentes = Pedido.objects.filter(status='Pendente').count()
        pedidos_confirmados = Pedido.objects.filter(status='Confirmado').count()
        pedidos_entregues = Pedido.objects.filter(status='Entregue').count()
        
        return Response({
            'total_pedidos': total_pedidos,
            'por_status': {
                'Pendente': pedidos_pendentes,
                'Confirmado': pedidos_confirmados,
                'Entregue': pedidos_entregues
            }
        })

class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer

    @action(detail=False, methods=['get'])
    def por_pedido(self, request):
        """Retorna itens de um pedido específico"""
        pedido_id = request.query_params.get('pedido_id')
        
        if not pedido_id:
            return Response(
                {'erro': 'Parâmetro pedido_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        itens = ItemPedido.objects.filter(pedido__id=pedido_id)
        serializer = self.get_serializer(itens, many=True)
        
        return Response({
            'pedido_id': pedido_id,
            'total_itens': itens.count(),
            'itens': serializer.data
        })

    @action(detail=False, methods=['get'])
    def produtos_mais_vendidos(self, request):
        """Retorna os produtos mais vendidos (por quantidade de itens)"""
        itens = ItemPedido.objects.values('produto__nome', 'produto__id').annotate(
            quantidade_total=Count('id'),
            total_vendas=Count('quantidade')
        ).order_by('-quantidade_total')[:10]
        
        return Response({
            'titulo': 'Top 10 Produtos Mais Vendidos',
            'produtos': list(itens)
        })