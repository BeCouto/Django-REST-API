from django.contrib import admin
from .models import Categoria, Produto, Pedido, ItemPedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'data_criacao']
    list_filter = ['categoria', 'data_criacao']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['data_criacao']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'data_pedido', 'status']
    list_filter = ['status', 'data_pedido']
    readonly_fields = ['data_pedido']

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'produto', 'quantidade', 'preco_unitario']
    list_filter = ['pedido']
    search_fields = ['produto__nome']
