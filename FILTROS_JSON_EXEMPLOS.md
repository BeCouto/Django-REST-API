# Exemplos de Filtros JSONField - AP2

## Estrutura do JSONField esperada

```json
{
    "marca": "Dell",
    "ram_gb": 16,
    "cor": "preto",
    "especificacoes": {
        "cpu": "i7",
        "armazenamento": "512GB SSD",
        "gpu": "NVIDIA RTX 3060"
    }
}
```

---

## 1. Filtros Básicos por Atributos JSON

### Exemplo: Filtrar por Marca
```
GET http://localhost:8000/api/produtos/filtrar_por_json/?marca=Dell
```

**Resposta esperada:**
```json
{
    "filtros_aplicados": {
        "marca": "Dell"
    },
    "total_resultados": 3,
    "resultados": [
        {
            "id": 1,
            "nome": "Notebook Dell XPS 13",
            "preco": "1999.99",
            "atributos_extras": {
                "marca": "Dell",
                "ram_gb": 16,
                "cor": "preto"
            }
        },
        ...
    ]
}
```

---

### Exemplo: Filtrar por Quantidade de RAM
```
GET http://localhost:8000/api/produtos/filtrar_por_json/?ram_gb=16
```

---

### Exemplo: Filtrar por Cor
```
GET http://localhost:8000/api/produtos/filtrar_por_json/?cor=preto
```

---

### Exemplo: Múltiplos Filtros Simples (AND)
```
GET http://localhost:8000/api/produtos/filtrar_por_json/?marca=Dell&ram_gb=16&cor=preto
```

Retorna apenas produtos que têm:
- Marca = Dell
- RAM = 16 GB
- Cor = Preto

---

## 2. Filtros em Atributos Aninhados (Especificações)

### Exemplo: Filtrar por CPU
```
GET http://localhost:8000/api/produtos/filtrar_por_json/?cpu=i7
```

---

### Exemplo: Filtrar por Armazenamento
```
GET http://localhost:8000/api/produtos/filtrar_por_json/?armazenamento=512GB%20SSD
```

---

## 3. Filtros Combinados (Categoria + Preço + JSON)

### Exemplo: Notebooks Dell entre R$ 1000 e R$ 3000
```
GET http://localhost:8000/api/produtos/filtro_combinado/?categoria_id=1&marca=Dell&preco_min=1000&preco_max=3000
```

**Resposta:**
```json
{
    "filtros_aplicados": {
        "categoria_id": "1",
        "marca": "Dell",
        "preco_min": "1000",
        "preco_max": "3000"
    },
    "total_resultados": 2,
    "resultados": [...]
}
```

---

### Exemplo: Notebooks com RAM 16GB e CPU i7, até R$ 2500
```
GET http://localhost:8000/api/produtos/filtro_combinado/?categoria_id=1&ram_gb=16&cpu=i7&preco_max=2500
```

---

## 4. Busca por Especificações Técnicas

### Exemplo: Produtos com CPU i9
```
GET http://localhost:8000/api/produtos/buscar_por_especificacoes/?cpu=i9
```

---

### Exemplo: Produtos com Armazenamento 512GB SSD
```
GET http://localhost:8000/api/produtos/buscar_por_especificacoes/?armazenamento=512GB%20SSD
```

---

### Exemplo: Produtos com CPU i7 E Armazenamento 512GB
```
GET http://localhost:8000/api/produtos/buscar_por_especificacoes/?cpu=i7&armazenamento=512GB
```

---

## 5. Testando com cURL

### Criar um produto com JSONField preenchido:
```bash
curl -X POST http://localhost:8000/api/produtos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Notebook Dell XPS 15",
    "descricao": "Notebook de alta performance",
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
}'
```

---

### Testar filtro por marca:
```bash
curl "http://localhost:8000/api/produtos/filtrar_por_json/?marca=Dell"
```

---

### Testar filtro combinado:
```bash
curl "http://localhost:8000/api/produtos/filtro_combinado/?categoria_id=1&marca=Dell&ram_gb=32&preco_min=2000&preco_max=3000"
```

---

### Testar busca por especificações:
```bash
curl "http://localhost:8000/api/produtos/buscar_por_especificacoes/?cpu=i9&armazenamento=1TB"
```

---

## 6. Erros Possíveis

### Erro: RAM não é número
```
GET http://localhost:8000/api/produtos/filtrar_por_json/?ram_gb=abc
```

**Resposta (400):**
```json
{
    "erro": "ram_gb deve ser um número inteiro"
}
```

---

### Erro: Categoria inválida
```
GET http://localhost:8000/api/produtos/filtro_combinado/?categoria_id=xyz
```

**Resposta (400):**
```json
{
    "erro": "categoria_id deve ser um número inteiro"
}
```

---

## 7. Resumo dos Endpoints JSONField

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/produtos/filtrar_por_json/` | GET | Filtro por marca, RAM, cor, CPU, armazenamento |
| `/api/produtos/filtro_combinado/` | GET | Filtro combinado: categoria + preço + JSON |
| `/api/produtos/buscar_por_especificacoes/` | GET | Busca em especificações aninhadas (CPU, GPU, armazenamento) |
| `/api/produtos/estatisticas/` | GET | Estatísticas gerais |

---

## 8. Campos Suportados nos Filtros

### Nível 1 (Direto):
- `marca` (string)
- `ram_gb` (inteiro)
- `cor` (string)

### Nível 2 (Aninhado em `especificacoes`):
- `cpu` (string)
- `armazenamento` (string)
- `gpu` (string)

---

## 9. Quando usar JSONField vs Campo Relacional

### Use JSONField quando:
- Os atributos são **opcionais** e variam entre produtos
- Você quer **flexibilidade** sem criar novas tabelas
- Os dados são **metadados** ou **especificações técnicas**
- Você precisa de **documentos semi-estruturados**

**Exemplo:** marca, cor, especificações técnicas de um notebook

### Use Campo Relacional quando:
- O relacionamento é **obrigatório** e **estruturado**
- Você precisa de **integridade referencial**
- Os dados são **compartilhados** entre múltiplas entidades
- Você quer **normalizar** o banco de dados

**Exemplo:** Categoria, Usuário, Pedido

---

## Conclusão

Os filtros JSONField implementados permitem:

✅ Busca por atributos individuais
✅ Combinação de múltiplos atributos (AND)
✅ Busca em dados aninhados (especificações técnicas)
✅ Filtro combinado (categoria + preço + atributos)
✅ Validação de entrada e tratamento de erros
✅ Escalabilidade sem necessidade de alterar schema

