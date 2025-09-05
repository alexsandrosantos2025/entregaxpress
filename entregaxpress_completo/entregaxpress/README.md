# EntregaXpress - Sistema de Entregas

Sistema completo de entregas com API para registro de entregadores e interface web para clientes.

## 🚀 Funcionalidades

### API de Usuários (Entregadores)
- ✅ Registro de entregadores com validação completa
- ✅ Validação de CPF e email
- ✅ Suporte a diferentes tipos de veículos (moto, bicicleta, carro)
- ✅ Gerenciamento completo de usuários (CRUD)
- ✅ Segurança com hash de senhas

### Interface Web
- ✅ Formulário de solicitação de entrega
- ✅ Interface responsiva e moderna
- ✅ Integração com API backend

## 📋 Estrutura do Projeto

```
entregaxpress/
├── src/
│   ├── models/
│   │   └── user.py          # Modelo de dados do usuário
│   ├── routes/
│   │   └── user.py          # Rotas da API de usuários
│   ├── static/
│   │   ├── index.html       # Interface do cliente
│   │   └── motoboy.html     # Interface do entregador
│   ├── database/
│   │   └── app.db           # Banco de dados SQLite
│   └── main.py              # Aplicação principal Flask
├── requirements.txt         # Dependências Python
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Esta documentação
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Autenticação**: Werkzeug Security
- **CORS**: Flask-CORS
- **ORM**: SQLAlchemy

## 📦 Instalação Local

### Pré-requisitos
- Python 3.11+
- pip

### Passos para Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd entregaxpress
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python src/main.py
```

5. **Acesse a aplicação**
- Interface Web: http://localhost:5000
- API Base: http://localhost:5000/api

## 🔌 Endpoints da API

### Usuários (Entregadores)

#### Registrar Novo Entregador
```http
POST /api/users/register
Content-Type: application/json

{
  "username": "motoboy_joao",
  "email": "joao@email.com",
  "password": "senha123",
  "full_name": "João da Silva",
  "phone": "(11) 99999-9999",
  "cpf": "12345678901",
  "vehicle_type": "moto",
  "vehicle_plate": "ABC-1234",
  "cnh": "12345678901"
}
```

**Resposta de Sucesso (201):**
```json
{
  "message": "Usuário registrado com sucesso",
  "user": {
    "id": 1,
    "username": "motoboy_joao",
    "email": "joao@email.com",
    "full_name": "João da Silva",
    "phone": "(11) 99999-9999",
    "cpf": "12345678901",
    "vehicle_type": "moto",
    "vehicle_plate": "ABC-1234",
    "cnh": "12345678901",
    "is_active": true,
    "created_at": "2025-09-04T03:39:41.407565"
  }
}
```

#### Listar Todos os Entregadores
```http
GET /api/users
```

#### Buscar Entregador por ID
```http
GET /api/users/{id}
```

#### Atualizar Entregador
```http
PUT /api/users/{id}
Content-Type: application/json

{
  "phone": "(11) 88888-8888",
  "vehicle_plate": "XYZ-5678"
}
```

#### Deletar Entregador
```http
DELETE /api/users/{id}
```

## ✅ Validações Implementadas

### Campos Obrigatórios
- username (nome de usuário único)
- email (formato válido)
- password (será criptografada)
- full_name (nome completo)
- phone (telefone)
- cpf (11 dígitos numéricos)
- vehicle_type (moto, bicicleta, carro)
- vehicle_plate (placa do veículo)

### Campos Opcionais
- cnh (CNH para motos/carros)

### Validações Automáticas
- ✅ Email deve ter formato válido
- ✅ CPF deve ter 11 dígitos numéricos
- ✅ Username deve ser único
- ✅ Email deve ser único
- ✅ CPF deve ser único
- ✅ Senha é automaticamente criptografada

## 🧪 Testando a API

### Usando curl

**Registrar um entregador:**
```bash
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "motoboy_teste",
    "email": "teste@email.com",
    "password": "senha123",
    "full_name": "João da Silva",
    "phone": "(11) 99999-9999",
    "cpf": "12345678901",
    "vehicle_type": "moto",
    "vehicle_plate": "ABC-1234",
    "cnh": "12345678901"
  }'
```

**Listar entregadores:**
```bash
curl http://localhost:5000/api/users
```

### Usando Postman

1. Importe a collection com os endpoints
2. Configure a base URL: `http://localhost:5000`
3. Use os exemplos de JSON fornecidos acima

## 🚀 Deploy no Railway

### Pré-requisitos
- Conta no Railway (https://railway.app)
- Código em repositório Git (GitHub, GitLab, etc.)

### Passos para Deploy

1. **Faça push do código para um repositório Git**
```bash
git add .
git commit -m "Preparar para deploy"
git push origin main
```

2. **No Railway:**
   - Acesse https://railway.app
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha o repositório da aplicação
   - Railway detectará automaticamente que é uma aplicação Flask

3. **Configurações Automáticas:**
   - Railway instalará as dependências do `requirements.txt`
   - A aplicação será executada automaticamente
   - Um domínio público será gerado

4. **Variáveis de Ambiente (se necessário):**
   - No painel do Railway, vá em "Variables"
   - Adicione variáveis como `FLASK_ENV=production`

5. **Acesse sua aplicação:**
   - Railway fornecerá uma URL pública
   - Exemplo: `https://entregaxpress-production-xxxx.up.railway.app`

### Comandos de Deploy Rápido

```bash
# 1. Certifique-se que está no diretório correto
cd entregaxpress

# 2. Atualize requirements.txt
pip freeze > requirements.txt

# 3. Commit e push
git add .
git commit -m "Update for deployment"
git push origin main

# 4. Railway fará o deploy automaticamente
```

## 🔧 Configurações de Produção

### Variáveis de Ambiente Recomendadas
```
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-super-segura
DATABASE_URL=sqlite:///app.db
```

### Segurança
- ✅ Senhas são criptografadas com Werkzeug
- ✅ CORS configurado para permitir requisições
- ✅ Validação de dados de entrada
- ✅ Tratamento de erros adequado

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs da aplicação
2. Confirme se todas as dependências estão instaladas
3. Teste localmente antes do deploy
4. Verifique se o banco de dados foi criado corretamente

## 📝 Changelog

### v1.0.0 (2025-09-04)
- ✅ Sistema de registro de entregadores completo
- ✅ API REST funcional
- ✅ Interface web responsiva
- ✅ Validações de segurança
- ✅ Preparado para deploy no Railway
- ✅ Documentação completa

