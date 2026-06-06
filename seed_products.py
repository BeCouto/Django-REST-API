#!/usr/bin/env python
"""
Script para preparar dados de teste e demonstrar os filtros JSONField
"""

import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo.settings')
sys.path.insert(0, '/c/Users/gcout/Downloads/Django-REST-API')

django.setup()

from produtos.models import Categoria, Produto

# Limpar dados anteriores
Categoria.objects.all().delete()
Produto.objects.all().delete()

# Criar categoria
categoria = Categoria.objects.create(
    nome="Notebooks",
    descricao="Computadores portáteis de alta performance"
)

# Criar produtos com JSONField preenchido
produtos = [
    {
        "nome": "Notebook Dell XPS 15",
        "descricao": "Notebook de alta performance com i9",
        "preco": "2499.99",
        "categoria": categoria,
        "atributos_extras": {
            "marca": "Dell",
            "ram_gb": 32,
            "cor": "cinza",
            "especificacoes": {
                "cpu": "Intel i9",
                "armazenamento": "1TB SSD",
                "gpu": "NVIDIA RTX 4090"
            }
        }
    },
    {
        "nome": "Notebook Samsung Galaxy Book 15",
        "descricao": "Notebook Samsung com processador AMD Ryzen",
        "preco": "1799.99",
        "categoria": categoria,
        "atributos_extras": {
            "marca": "Samsung",
            "ram_gb": 16,
            "cor": "preto",
            "especificacoes": {
                "cpu": "AMD Ryzen 7",
                "armazenamento": "512GB SSD",
                "gpu": "Radeon Graphics"
            }
        }
    },
    {
        "nome": "Notebook Dell Inspiron 15",
        "descricao": "Notebook Dell com i7 de boa custo-benefício",
        "preco": "1299.99",
        "categoria": categoria,
        "atributos_extras": {
            "marca": "Dell",
            "ram_gb": 16,
            "cor": "preto",
            "especificacoes": {
                "cpu": "Intel i7",
                "armazenamento": "512GB SSD",
                "gpu": "Intel Iris Graphics"
            }
        }
    },
    {
        "nome": "Notebook HP Pavilion 14",
        "descricao": "Notebook compacto e portátil HP",
        "preco": "999.99",
        "categoria": categoria,
        "atributos_extras": {
            "marca": "HP",
            "ram_gb": 8,
            "cor": "prata",
            "especificacoes": {
                "cpu": "Intel i5",
                "armazenamento": "256GB SSD",
                "gpu": "Intel UHD Graphics"
            }
        }
    },
    {
        "nome": "MacBook Pro 16",
        "descricao": "Notebook Apple para profissionais",
        "preco": "3999.99",
        "categoria": categoria,
        "atributos_extras": {
            "marca": "Apple",
            "ram_gb": 32,
            "cor": "cinza-espacial",
            "especificacoes": {
                "cpu": "Apple M3 Pro",
                "armazenamento": "1TB SSD",
                "gpu": "Apple GPU integrada"
            }
        }
    }
]

for prod_data in produtos:
    produto = Produto.objects.create(**prod_data)
    print(f"✓ Criado: {produto.nome} ({produto.atributos_extras['marca']})")

print("\n" + "="*60)
print("✅ Dados de teste criados com sucesso!")
print("="*60)
print("\nAgora você pode testar os filtros:")
print("\n1. Filtrar por marca Dell:")
print("   http://localhost:8000/api/produtos/filtrar_por_json/?marca=Dell")
print("\n2. Filtrar por RAM 16GB:")
print("   http://localhost:8000/api/produtos/filtrar_por_json/?ram_gb=16")
print("\n3. Filtrar por CPU i9:")
print("   http://localhost:8000/api/produtos/filtrar_por_json/?cpu=i9")
print("\n4. Filtro combinado (Dell + 16GB de RAM):")
print("   http://localhost:8000/api/produtos/filtrar_por_json/?marca=Dell&ram_gb=16")
print("\n5. Filtro combinado com preço (1000-2000):")
print("   http://localhost:8000/api/produtos/filtro_combinado/?preco_min=1000&preco_max=2000&marca=Dell")
print("\n6. Buscar por especificações (CPU i7 + 512GB):")
print("   http://localhost:8000/api/produtos/buscar_por_especificacoes/?cpu=i7&armazenamento=512GB")
