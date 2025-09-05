# 🚀 Guia de Deploy - EntregaXpress no Railway

Este guia fornece instruções passo a passo para fazer o deploy da aplicação EntregaXpress no Railway.

## 📋 Pré-requisitos

- [ ] Conta no GitHub (https://github.com)
- [ ] Conta no Railway (https://railway.app)
- [ ] Código da aplicação EntregaXpress

## 🔄 Passo 1: Preparar o Repositório GitHub

### 1.1 Criar Repositório no GitHub

1. Acesse https://github.com
2. Clique em "New repository"
3. Nome sugerido: `entregaxpress-api`
4. Marque como "Public" ou "Private"
5. Clique em "Create repository"

### 1.2 Fazer Upload do Código

**Opção A: Via Interface Web do GitHub**
1. No repositório criado, clique em "uploading an existing file"
2. Arraste todos os arquivos da pasta `entregaxpress/`
3. Commit message: "Initial commit - EntregaXpress API"
4. Clique em "Commit changes"

**Opção B: Via Git (se tiver Git instalado)**
```bash
# No diretório da aplicação
git remote add origin https://github.com/SEU_USUARIO/entregaxpress-api.git
git branch -M main
git push -u origin main
```

## 🚀 Passo 2: Deploy no Railway

### 2.1 Criar Projeto no Railway

1. Acesse https://railway.app
2. Faça login com sua conta GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Autorize o Railway a acessar seus repositórios
6. Selecione o repositório `entregaxpress-api`

### 2.2 Configuração Automática

O Railway detectará automaticamente:
- ✅ Linguagem: Python
- ✅ Framework: Flask
- ✅ Dependências: requirements.txt
- ✅ Comando de start: `python src/main.py`

### 2.3 Aguardar o Deploy

1. O Railway iniciará o build automaticamente
2. Você verá os logs de instalação das dependências
3. Aguarde até aparecer "Deploy successful"
4. Uma URL pública será gerada automaticamente

## 🔗 Passo 3: Testar a Aplicação

### 3.1 Acessar a URL Pública

1. No painel do Railway, clique na URL gerada
2. Exemplo: `https://entregaxpress-production-xxxx.up.railway.app`
3. Você deve ver a interface web da aplicação

### 3.2 Testar os Endpoints da API

**Teste de Registro de Entregador:**
```bash
curl -X POST https://SUA_URL_DO_RAILWAY.up.railway.app/api/users/register \
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

**Teste de Listagem:**
```bash
curl https://SUA_URL_DO_RAILWAY.up.railway.app/api/users
```

## 🔧 Passo 4: Configurações Opcionais

### 4.1 Configurar Domínio Personalizado (Opcional)

1. No painel do Railway, vá em "Settings"
2. Clique em "Domains"
3. Adicione seu domínio personalizado
4. Configure o DNS conforme instruções

### 4.2 Configurar Variáveis de Ambiente (Opcional)

1. No painel do Railway, vá em "Variables"
2. Adicione variáveis se necessário:
   - `FLASK_ENV=production`
   - `SECRET_KEY=sua-chave-super-secreta`

## 🔄 Passo 5: Atualizações Futuras

### Para atualizar a aplicação:

1. **Faça as alterações no código local**
2. **Commit e push para o GitHub:**
```bash
git add .
git commit -m "Descrição das alterações"
git push origin main
```
3. **O Railway fará o redeploy automaticamente**

## 📱 Passo 6: Configurar Postman para Testes

### 6.1 Criar Collection no Postman

1. Abra o Postman
2. Crie uma nova Collection: "EntregaXpress API"
3. Configure a base URL: `{{base_url}}`
4. Crie uma variável de ambiente:
   - Variable: `base_url`
   - Value: `https://SUA_URL_DO_RAILWAY.up.railway.app`

### 6.2 Requests Prontos para Importar

**POST - Registrar Entregador:**
- URL: `{{base_url}}/api/users/register`
- Method: POST
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
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

**GET - Listar Entregadores:**
- URL: `{{base_url}}/api/users`
- Method: GET

## ⚠️ Solução de Problemas

### Problema: Deploy falhou
**Solução:**
1. Verifique os logs no Railway
2. Confirme se o `requirements.txt` está correto
3. Verifique se não há erros de sintaxe no código

### Problema: API retorna erro 500
**Solução:**
1. Verifique os logs da aplicação no Railway
2. Teste localmente primeiro
3. Confirme se o banco de dados foi criado

### Problema: CORS error no frontend
**Solução:**
- O Flask-CORS já está configurado
- Verifique se as requisições estão usando a URL correta

## ✅ Checklist Final

- [ ] Código commitado no GitHub
- [ ] Deploy realizado no Railway
- [ ] URL pública funcionando
- [ ] Interface web carregando
- [ ] Endpoint de registro funcionando
- [ ] Endpoint de listagem funcionando
- [ ] Validações funcionando corretamente
- [ ] Postman configurado para testes

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs no painel do Railway
2. Teste a aplicação localmente
3. Confirme se seguiu todos os passos
4. Verifique se o repositório GitHub está atualizado

---

**🎉 Parabéns! Sua aplicação EntregaXpress está no ar!**

