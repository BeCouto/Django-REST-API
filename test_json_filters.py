#!/usr/bin/env python
"""
Script de teste para os filtros JSONField da AP2
Execute: python test_json_filters.py
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_response(title, response):
    """Formata e exibe a resposta da API"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_criar_produto_com_json():
    """Teste 1: Criar um produto com JSONField preenchido"""
    print_response(
        "TESTE 1: Criar Produto com JSONField",
        requests.post(f"{BASE_URL}/produtos/", json={
            "nome": "Notebook Dell XPS 15",
            "descricao": "Notebook de alta performance com i9",
            "preco": "2499.99",
            "categoria": 1,
            "atributos_extras": {
                "marca": "Dell",
                "ram_gb": 32,
                "cor": "cinza",
                "especificacoes": {
                    "cpu": "i9",
                    "armazenamento": "1TB SSD",
                    "gpu": "NVIDIA RTX 4090"
                }
            }
        })
    )

def test_criar_produto_samsung():
    """Teste 2: Criar outro produto (Samsung)"""
    print_response(
        "TESTE 2: Criar Produto Samsung",
        requests.post(f"{BASE_URL}/produtos/", json={
            "nome": "Samsung Galaxy Book 15",
            "descricao": "Notebook Samsung com processador AMD",
            "preco": "1799.99",
            "categoria": 1,
            "atributos_extras": {
                "marca": "Samsung",
                "ram_gb": 16,
                "cor": "preto",
                "especificacoes": {
                    "cpu": "Ryzen 7",
                    "armazenamento": "512GB SSD",
                    "gpu": "Radeon"
                }
            }
        })
    )

def test_filtro_por_marca():
    """Teste 3: Filtrar por marca"""
    print_response(
        "TESTE 3: Filtrar por Marca (Dell)",
        requests.get(f"{BASE_URL}/produtos/filtrar_por_json/?marca=Dell")
    )

def test_filtro_por_ram():
    """Teste 4: Filtrar por RAM"""
    print_response(
        "TESTE 4: Filtrar por RAM (16GB)",
        requests.get(f"{BASE_URL}/produtos/filtrar_por_json/?ram_gb=16")
    )

def test_filtro_por_cpu():
    """Teste 5: Filtrar por CPU"""
    print_response(
        "TESTE 5: Filtrar por CPU (i9)",
        requests.get(f"{BASE_URL}/produtos/filtrar_por_json/?cpu=i9")
    )

def test_filtro_multiplo():
    """Teste 6: Filtrar por marca E RAM (multiplo)"""
    print_response(
        "TESTE 6: Filtrar por Marca AND RAM",
        requests.get(f"{BASE_URL}/produtos/filtrar_por_json/?marca=Dell&ram_gb=32")
    )

def test_filtro_combinado():
    """Teste 7: Filtro combinado (categoria + preço + JSON)"""
    print_response(
        "TESTE 7: Filtro Combinado (Categoria 1 + Preço 1000-3000 + Marca Dell)",
        requests.get(f"{BASE_URL}/produtos/filtro_combinado/?categoria_id=1&marca=Dell&preco_min=1000&preco_max=3000")
    )

def test_busca_especificacoes():
    """Teste 8: Busca por especificações"""
    print_response(
        "TESTE 8: Buscar por Especificações (CPU i9 + Armazenamento 1TB)",
        requests.get(f"{BASE_URL}/produtos/buscar_por_especificacoes/?cpu=i9&armazenamento=1TB")
    )

def test_listar_todos_produtos():
    """Teste 9: Listar todos os produtos"""
    print_response(
        "TESTE 9: Listar Todos os Produtos",
        requests.get(f"{BASE_URL}/produtos/")
    )

def test_erro_ram_invalida():
    """Teste 10: Erro - RAM não é número"""
    print_response(
        "TESTE 10: Erro - RAM inválida (não é número)",
        requests.get(f"{BASE_URL}/produtos/filtrar_por_json/?ram_gb=abc")
    )

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("🧪 TESTES DE FILTROS JSONFIELD - AP2")
    print("="*60)
    
    testes = [
        ("Criar Produto Dell", test_criar_produto_com_json),
        ("Criar Produto Samsung", test_criar_produto_samsung),
        ("Filtrar por Marca", test_filtro_por_marca),
        ("Filtrar por RAM", test_filtro_por_ram),
        ("Filtrar por CPU", test_filtro_por_cpu),
        ("Filtro Múltiplo", test_filtro_multiplo),
        ("Filtro Combinado", test_filtro_combinado),
        ("Busca Especificações", test_busca_especificacoes),
        ("Listar Produtos", test_listar_todos_produtos),
        ("Erro - RAM Inválida", test_erro_ram_invalida),
    ]
    
    for i, (nome, teste) in enumerate(testes, 1):
        try:
            teste()
        except Exception as e:
            print(f"\n❌ Erro no teste {i} ({nome}): {e}")
    
    print("\n" + "="*60)
    print("✅ TESTES FINALIZADOS")
    print("="*60)
    print("\nNota: Certifique-se de que o servidor Django está rodando:")
    print("  python manage.py runserver")

if __name__ == "__main__":
    main()
