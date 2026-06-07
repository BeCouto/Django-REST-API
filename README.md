# AP1 e AP2 - Catálogo de Produtos e E-commerce (Django REST API na AWS)

Este projeto foi desenvolvido para a disciplina de **Big Data e Computação em Nuvem** no curso de Ciência de Dados e Inteligência Artificial do **Ibmec Barra**. 

O objetivo da AP2 foi evoluir a aplicação monolítica da AP1, implementando um modelo de e-commerce e migrando a infraestrutura para uma **arquitetura de nuvem escalável, segura e voltada para produção**, utilizando bancos de dados gerenciados, armazenamento de objetos e regras de firewall restritas.

🔗 **Links do Projeto:**
* **API em Produção (AWS):** [http://ap2-becouto-env.eba-pvhunujs.us-east-1.elasticbeanstalk.com/]
* **Repositório GitHub:** https://github.com/BeCouto/Django-REST-API.git

---

## 👥 Autores e Integrantes do Grupo
* **Curso:** Ciência de Dados e Inteligência Artificial (5º Período) - Ibmec Barra
* Gabriel Couto
* Enzo Guedes Cardoso
* Bernardo Ottan Procopio
* Daniel de Jesus Teixeira

---

## 🏗️ Arquitetura da Solução (Evolução AP1 ➡️ AP2)

Na **AP1**, a aplicação era um monólito simples, utilizando banco de dados local (`SQLite`), mídias salvas no disco do servidor e configurações expostas.

Na **AP2**, o sistema foi inteiramente refatorado para operar nas melhores práticas de **Cloud Computing na AWS**:
1. **App Server (PaaS):** Hospedagem no **AWS Elastic Beanstalk** (Python 3.12 / Gunicorn / Nginx). Foi configurado um pipeline via `.ebextensions` para ativar o ambiente virtual e coletar arquivos estáticos dinamicamente em cada deploy.
2. **Database (RDS):** Migração para **PostgreSQL no AWS RDS**. O banco de dados foi isolado: o Security Group padrão (`0.0.0.0/0`) foi removido, aplicando o Princípio do Menor Privilégio, permitindo apenas tráfego vindo da instância EC2.
3. **Storage (S3):** Integração com `boto3` e `django-storages`. Arquivos de mídia e imagens de produtos são salvos em um bucket **AWS S3**. Para evitar o uso de chaves ou tokens expiráveis, o acesso foi concedido diretamente via **IAM Role** anexada à instância EC2.
4. **Segurança e Isolamento:** Senhas do banco, chaves da AWS (`SECRET_KEY`) e hosts permitidos foram isolados nas **Environment Properties** do Elastic Beanstalk, garantindo que nenhum dado sensível trafegue no código-fonte.

---

## ✨ Novas Funcionalidades (AP2)

### 1. Carrinho de Compras (Pedidos e Itens)
Foram criadas as entidades `Pedido` e `ItemPedido` no banco de dados, estabelecendo relação com `Produto`. A API permite criar pedidos, adicionar produtos a eles, calcular totais automaticamente e alterar status de entrega.
* `GET /api/pedidos/`
* `GET /api/itens-pedidos/`

### 2. 🌟 Ponto Bônus: JSONB com JSONField (PostgreSQL)
Implementamos um modelo híbrido relacional/documento utilizando o campo `JSONField` nativo do PostgreSQL.
O modelo `Produto` possui um campo `atributos_extras` que permite salvar dicionários de metadados dinâmicos. Foram criados endpoints avançados para busca dentro do JSON:
* **Filtro Direto:** `/api/produtos/filtrar_por_json/?marca=Dell&ram_gb=16`
* **Busca Aninhada (Especificações):** `/api/produtos/buscar_por_especificacoes/?cpu=i7&armazenamento=512GB`
* **Filtro Combinado (Relacional + JSON):** `/api/produtos/filtro_combinado/?categoria_id=1&marca=Dell&preco_max=3000`

**Quando usar Campo Relacional vs JSONField?**
* **Campo Relacional:** Ideal para dados fortemente estruturados, relacionamentos obrigatórios e integridade referencial (Ex: `Categoria`, `Pedido`).
* **JSONField:** Ideal para atributos opcionais e documentos semi-estruturados onde a flexibilidade é mais importante que a normalização estrita (Ex: especificações técnicas dinâmicas de hardware).

---

## 💻 Passo a Passo: Execução Local

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone [https://github.com/BeCouto/Django-REST-API.git]
   cd Django-REST-API

```

2. **Crie o ambiente virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

```


3. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


4. **Configure as Variáveis de Ambiente locais (Crie um arquivo .env ou exporte):**
```bash
DB_NAME=seu_banco_local
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
USE_S3=False # Para rodar estáticos localmente

```


5. **Rode as migrações e o servidor:**
```bash
python manage.py migrate
python manage.py runserver

```

---

## 🔐 Acesso ao Painel Administrativo (Django Admin)

Para facilitar a correção, o superusuário de produção é gerado automaticamente durante o processo de deploy no AWS Elastic Beanstalk, consumindo as credenciais seguras injetadas via *Environment Properties*.

**Acesso na Nuvem (AWS):**
* **URL:** `http://ap2-becouto-env.eba-pvhunujs.us-east-1.elasticbeanstalk.com/admin/`
* **Usuário:** Gabriel
* **Senha:** 12345678

**Criação Local (Ambiente de Desenvolvimento):**
Caso deseje rodar a aplicação localmente, o banco `db.sqlite3` virá vazio. Para criar o seu próprio administrador, execute o comando abaixo no terminal com o ambiente virtual ativado:
```bash
python manage.py createsuperuser
