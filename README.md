# AP1 - Catálogo de Produtos e Categorias (Django REST API)

Este projeto foi desenvolvido para a disciplina de **Big Data e Computação em Nuvem** no curso de Ciência de Dados e Inteligência Artificial do **Ibmec Barra**. O objetivo principal é construir uma API robusta e escalável utilizando Django REST Framework, com deploy totalmente funcional na nuvem AWS.

## 🔗 Links do Projeto

  * **API em Produção (AWS):** http://catalogo-produtos-ap1-env-1.eba-qxbikzvf.us-east-1.elasticbeanstalk.com/
  * **Repositório GitHub:** [https://github.com/BeCouto/AP1_BigData.git]

-----

## 👨‍🎓 Autor e integrantes do grupo 

  * **Curso:** Ciência de Dados e Inteligência Artificial (5º Período) - Ibmec Barra
  * **Nome:** Gabriel Couto
  * **Nome:** Enzo Guedes Cardoso
  * **Nome:** bernardo ottan procopio
  * **Nome:** Daniel de Jesus Teixeira

-----

## 🛠️ Tecnologias e Arquitetura

Para garantir a escalabilidade e facilidade de migração futura, o projeto utiliza:

  * **Linguagem:** Python 3.13 (Local) / Python 3.12 (AWS)
  * **Framework:** Django 6.x com Django REST Framework (DRF)
  * **Banco de Dados:** SQLite (Base para futura migração para RDS)
  * **Cloud (PaaS):** AWS Elastic Beanstalk
  * **Servidor de Aplicação:** Gunicorn

-----

## 🚀 Funcionalidades Implementadas

### 1\. CRUD Completo de Produtos e Categorias

A API permite o gerenciamento total de itens e suas respectivas categorias através dos endpoints:

  * `GET /api/produtos/`
  * `GET /api/categorias/`

### 2\. Endpoint Analítico (Business Intelligence) - **Diferencial**

Implementei uma rota específica para análise de dados, processada diretamente via ORM do Django para garantir performance:

  * **Rota:** `/api/produtos/estatisticas/`
  * **Dados:** Retorna o total de itens, preço médio global e distribuição de produtos agrupados por categoria.

### 3\. Filtros e Busca Inteligente

  * **Filtro por Categoria:** `/api/produtos/?categoria=[ID]`
  * **Busca Textual:** `/api/produtos/?nome=[termo]` (Case-insensitive)

### 4\. Paginação Global

Configuração de paginação em todos os endpoints de lista para evitar sobrecarga no servidor e melhorar a experiência de consumo da API.

### 5\. Resolução de Problemas 

Durante os testes de deploy, identifiquei através da leitura dos logs (eb-engine.log) uma falha na instalação de dependências. O problema foi resolvido isolando e comentando a biblioteca psycopg2-binary no requirements.txt, que não é necessária para o escopo inicial com SQLite, garantindo assim que a instância EC2 da AWS finalizasse o provisionamento com sucesso

-----

## 📂 Documentação das Etapas (Relatório de Desenvolvimento)

Conforme os critérios da AP1, as etapas realizadas foram:

1.  **Modelagem de Dados:** Criação da classe `Categoria` e estabelecimento de relacionamento `ForeignKey` (Um-para-Muitos) com a classe `Produto`.
2.  **Lógica de Negócio e Validação:** Implementação de validações customizadas no `serializers.py` para garantir que campos críticos (como preço) não aceitem valores negativos.
3.  **Configuração de Ambiente:** Criação do arquivo `requirements.txt` e `Procfile` para detecção automática da AWS.
4.  **Deploy na Nuvem:** O deploy foi realizado via empacotamento `app.zip` (higienizado sem `venv` ou bancos locais) diretamente no console do **AWS Elastic Beanstalk**, utilizando as `.ebextensions` fornecidas no roteiro de aula.

-----

## 💻 Como Rodar Localmente

1.  **Clone o projeto:**
    ```bash
    git clone [https://github.com/BeCouto/AP1_BigData.git]
    ```
2.  **Crie o ambiente virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Rode as migrações e o servidor:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

-----

*Este projeto é parte integrante da avaliação AP1 da graduação do Ibmec Barra.*
