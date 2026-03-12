# RAG System - Retrieval-Augmented Generation com LLM

Um sistema elegante e completo de Retrieval-Augmented Generation (RAG) que integra modelos de linguagem avançados com busca semântica em banco de dados vetorial. A aplicação oferece uma interface web refinada para interação com documentos através de chat inteligente, suporte a upload de múltiplos formatos de arquivo e processamento automático de conteúdo.

## 🎯 Visão Geral do Projeto

Este projeto foi desenvolvido como parte de um estágio em Engenharia de IA, cobrindo os seguintes pilares tecnológicos:

**Backend Python & LLM Integration:** Implementação de API REST em FastAPI com suporte a múltiplos provedores de LLM (OpenAI, Google Gemini, modelos locais) com streaming de respostas em tempo real.

**RAG & Banco Vetorial:** Sistema completo de Retrieval-Augmented Generation utilizando ChromaDB para armazenamento e busca semântica de embeddings, permitindo recuperação inteligente de contexto relevante.

**Processamento de Documentos:** Pipeline automático para upload e processamento de documentos em múltiplos formatos (PDF, TXT, Markdown) com chunking inteligente e indexação vetorial.

**DevOps & Containerização:** Configuração completa com Docker e docker-compose para ambiente isolado e reproduzível, com health checks e orquestração de serviços.

**CI/CD Pipeline:** Workflow automatizado com GitHub Actions incluindo testes, linting, type checking, build de imagens Docker e security scanning.

**Interface Web Elegante:** Frontend React com design refinado, tema escuro sofisticado, chat em tempo real com suporte a streaming e visualização de fontes.

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React 19)                      │
│  - Chat Interface com Streaming                             │
│  - Document Upload Manager                                 │
│  - Source Visualization                                    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/WebSocket
┌────────────────────▼────────────────────────────────────────┐
│              Backend API (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Endpoints:                                           │   │
│  │ - POST /api/chat          → Chat com RAG            │   │
│  │ - POST /api/chat/stream   → Chat com Streaming      │   │
│  │ - POST /api/upload        → Upload de Documentos    │   │
│  │ - POST /api/search        → Busca Semântica         │   │
│  │ - GET  /api/collection    → Estatísticas            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼───┐  ┌────▼────┐  ┌───▼──────┐
   │   LLM  │  │ RAG     │  │ Document │
   │Provider│  │ System  │  │Processor │
   └────┬───┘  └────┬────┘  └───┬──────┘
        │           │           │
   ┌────▼───────────▼───────────▼──────┐
   │      ChromaDB (Vector Store)       │
   │  - Embeddings                      │
   │  - Semantic Search                 │
   │  - Document Chunks                 │
   └────────────────────────────────────┘
```

## 📋 Funcionalidades Principais

### 1. Sistema de Chat Inteligente
- Chat em tempo real com suporte a streaming de respostas
- Integração automática com RAG para contexto relevante
- Visualização de fontes (documentos recuperados com scores de similaridade)
- Suporte a múltiplos provedores de LLM

### 2. Upload e Processamento de Documentos
- Suporte a múltiplos formatos: PDF, TXT, Markdown
- Processamento automático com chunking inteligente
- Indexação automática no banco vetorial
- Rastreamento de metadados do documento

### 3. Busca Semântica Avançada
- Busca por similaridade usando embeddings
- Configuração de threshold de relevância
- Retorno de top-K resultados mais similares
- Scores de similaridade para cada resultado

### 4. Integração com LLM
- Suporte a OpenAI (GPT-4, GPT-3.5)
- Suporte a Google Gemini
- Arquitetura extensível para modelos locais
- Controle de temperatura e max_tokens

### 5. DevOps & Deployment
- Containerização com Docker
- Orquestração com docker-compose
- CI/CD com GitHub Actions
- Health checks e monitoring

## 🚀 Começando

### Pré-requisitos
- Python 3.11+
- Node.js 22+
- Docker e Docker Compose
- API Key do OpenAI ou Google Gemini

### Instalação Local

**1. Clonar o repositório**
```bash
git clone <repository-url>
cd ai-engineering-internship-project
```

**2. Configurar variáveis de ambiente**
```bash
cp backend/.env.example backend/.env
# Editar backend/.env com suas credenciais
```

**3. Instalar dependências do backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**4. Instalar dependências do frontend**
```bash
cd ..
pnpm install
```

**5. Iniciar o backend**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**6. Iniciar o frontend (em outro terminal)**
```bash
pnpm dev
```

A aplicação estará disponível em `http://localhost:3000`

### Instalação com Docker

**1. Configurar variáveis de ambiente**
```bash
cp backend/.env.example backend/.env
# Editar backend/.env com suas credenciais
```

**2. Iniciar com docker-compose**
```bash
docker-compose up --build
```

A aplicação estará disponível em `http://localhost:3000`

## 📚 Estrutura do Projeto

```
ai-engineering-internship-project/
├── backend/
│   ├── app/
│   │   ├── llm.py              # Integração com provedores LLM
│   │   ├── rag.py              # Sistema RAG com ChromaDB
│   │   ├── document_processor.py # Processamento de documentos
│   │   ├── models.py           # Modelos Pydantic
│   │   └── __init__.py
│   ├── config/
│   │   ├── settings.py         # Configurações da aplicação
│   │   └── __init__.py
│   ├── tests/
│   │   ├── test_rag.py         # Testes do RAG
│   │   ├── test_document_processor.py # Testes de processamento
│   │   └── __init__.py
│   ├── main.py                 # Aplicação FastAPI
│   ├── requirements.txt        # Dependências Python
│   ├── Dockerfile              # Containerização
│   ├── .env.example            # Variáveis de ambiente
│   └── prompt_examples.md      # Exemplos de Prompt Engineering
├── client/
│   ├── src/
│   │   ├── pages/
│   │   │   └── Home.tsx        # Interface de chat
│   │   ├── components/         # Componentes React
│   │   ├── App.tsx             # Aplicação principal
│   │   └── index.css           # Estilos globais
│   └── public/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Pipeline CI/CD
├── docker-compose.yml          # Orquestração de containers
├── Dockerfile.frontend         # Build do frontend
├── todo.md                     # Rastreamento de tarefas
└── README.md                   # Este arquivo
```

## 🔌 API Endpoints

### Chat

**POST /api/chat**

Realiza uma requisição de chat com contexto RAG.

```json
{
  "message": "Qual é o tema principal do documento?",
  "use_rag": true,
  "system_prompt": "Você é um assistente especializado.",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

Resposta:
```json
{
  "response": "O tema principal é...",
  "sources": [
    {
      "document": "Trecho do documento...",
      "similarity": 0.95
    }
  ],
  "model": "gpt-4-turbo-preview",
  "timestamp": "2024-03-02T18:00:00Z"
}
```

**POST /api/chat/stream**

Chat com streaming de resposta em tempo real.

```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Sua pergunta"}'
```

### Upload de Documentos

**POST /api/upload**

Faz upload de um documento para indexação.

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@documento.pdf"
```

Resposta:
```json
{
  "document_id": "uuid-aqui",
  "filename": "documento.pdf",
  "file_type": "pdf",
  "file_size": 1024000,
  "chunks_created": 15,
  "status": "success"
}
```

### Busca Semântica

**POST /api/search**

Realiza busca semântica no banco vetorial.

```json
{
  "query": "Conceitos principais",
  "top_k": 5,
  "threshold": 0.3
}
```

Resposta:
```json
{
  "results": [
    {
      "document": "Trecho relevante...",
      "similarity": 0.92,
      "metadata": {"filename": "doc.pdf"}
    }
  ],
  "query": "Conceitos principais",
  "total_results": 3
}
```

### Estatísticas

**GET /api/collection/stats**

Retorna estatísticas da coleção de documentos.

**DELETE /api/collection/clear**

Limpa toda a coleção de documentos.

## 🧪 Testes

### Executar testes do backend

```bash
cd backend
pytest tests/ -v --cov=app
```

### Executar testes do frontend

```bash
pnpm test
```

### Cobertura de testes

```bash
cd backend
pytest tests/ --cov=app --cov-report=html
```

## 💡 Prompt Engineering

O projeto inclui exemplos extensivos de Prompt Engineering em `backend/prompt_examples.md`. Alguns padrões principais:

**Chain-of-Thought:** Instruir o modelo a pensar passo a passo

```python
system_prompt = "Pense passo a passo e explique seu raciocínio."
```

**Role-Playing:** Atribuir um papel específico ao modelo

```python
system_prompt = "Você é um especialista em machine learning com 10 anos de experiência."
```

**Few-Shot Learning:** Fornecer exemplos de entrada/saída

```python
system_prompt = """
Exemplo 1: [entrada] -> [saída]
Exemplo 2: [entrada] -> [saída]
Agora responda para: [nova entrada]
"""
```

## 🐳 Docker & Deployment

### Build de imagens

```bash
# Backend
docker build -t rag-backend:latest ./backend

# Frontend
docker build -t rag-frontend:latest -f Dockerfile.frontend .
```

### Executar com docker-compose

```bash
docker-compose up -d
docker-compose logs -f
```

### Health check

```bash
curl http://localhost:8000/health
```

## 🔄 CI/CD Pipeline

O projeto utiliza GitHub Actions para automação:

- **Testes:** Execução de pytest e vitest
- **Linting:** Validação com flake8 e prettier
- **Type Checking:** Verificação com mypy
- **Build:** Construção de imagens Docker
- **Security:** Scanning com Trivy

Ver `.github/workflows/ci-cd.yml` para detalhes.

## 🎨 Design & Interface

A interface segue um design elegante e refinado com:

- **Tema escuro sofisticado:** Cores OKLCH otimizadas para conforto visual
- **Chat inteligente:** Interface limpa com suporte a markdown
- **Sidebar de documentos:** Gerenciamento visual de uploads
- **Visualização de fontes:** Exibição de documentos recuperados com scores
- **Responsivo:** Funciona em desktop, tablet e mobile

## 🔐 Segurança

- Validação de entrada em todos os endpoints
- CORS configurável
- Suporte a HTTPS em produção
- Sanitização de uploads
- Rate limiting (implementar conforme necessário)

## 📊 Monitoramento & Logs

Os logs estão disponíveis em:

- Backend: `backend/logs/` (via uvicorn)
- Docker: `docker-compose logs -f`
- Frontend: Console do navegador

## 🚨 Troubleshooting

**Erro de conexão com LLM:**
- Verificar API key em `.env`
- Validar permissões da conta
- Testar com `curl` para diagnosticar

**ChromaDB não inicializa:**
- Verificar permissões da pasta `data/chroma_db`
- Limpar cache: `rm -rf backend/data/chroma_db`
- Reiniciar container

**Frontend não conecta ao backend:**
- Verificar CORS em `backend/main.py`
- Confirmar que backend está rodando em `http://localhost:8000`
- Verificar logs do navegador

## 📈 Próximos Passos

- Implementar autenticação e autorização
- Adicionar persistência de conversas
- Suporte a múltiplas conversas simultâneas
- Análise de performance e otimizações
- Integração com mais provedores de LLM
- Dashboard de analytics

## 📝 Licença

MIT License - Veja LICENSE para detalhes.

## 👥 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

**Desenvolvido como parte do programa de estágio em Engenharia de IA**

*Última atualização: Março de 2026*

