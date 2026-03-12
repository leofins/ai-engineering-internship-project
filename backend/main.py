"""
Aplicação principal FastAPI para RAG System
"""
import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from config.settings import settings
from app import (
    get_llm_provider,
    get_rag_system,
    DocumentProcessor,
    DocumentMetadata,
    DocumentChunker,
    ChatRequest,
    ChatResponse,
    DocumentUploadResponse,
    SearchRequest,
    SearchResponse,
    HealthResponse,
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    logger.info("Starting RAG System...")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
    
    try:
        rag_system = get_rag_system()
        stats = rag_system.get_collection_stats()
        logger.info(f"RAG System initialized with {stats['total_documents']} documents")
    except Exception as e:
        logger.error(f"Failed to initialize RAG System: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down RAG System...")


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas de Health Check
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check da aplicação"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        llm_provider=settings.LLM_PROVIDER,
    )


# Rotas de Chat
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint de chat com RAG
    
    - **message**: Mensagem do usuário
    - **use_rag**: Usar RAG para contexto (padrão: true)
    - **system_prompt**: Prompt do sistema customizado
    - **temperature**: Temperatura do modelo (0.0-2.0)
    - **max_tokens**: Máximo de tokens na resposta
    """
    try:
        llm = get_llm_provider()
        rag = get_rag_system()
        
        # Buscar contexto do RAG se habilitado
        context = ""
        sources = []
        
        if request.use_rag:
            search_results = rag.search(request.message)
            sources = [
                {
                    "document": result["document"][:200],
                    "similarity": result["similarity"],
                }
                for result in search_results
            ]
            
            context = "\n\n".join([result["document"] for result in search_results])
        
        # Construir prompt com contexto
        system_prompt = request.system_prompt or "You are a helpful assistant."
        if context:
            system_prompt += f"\n\nContext:\n{context}"
        
        # Gerar resposta
        response = await llm.generate(
            prompt=request.message,
            system_prompt=system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        return ChatResponse(
            response=response,
            sources=sources,
            model=settings.OPENAI_MODEL if settings.LLM_PROVIDER == "openai" else settings.GEMINI_MODEL,
            timestamp=datetime.now(),
        )
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Endpoint de chat com streaming
    """
    async def generate():
        try:
            llm = get_llm_provider()
            rag = get_rag_system()
            
            # Buscar contexto do RAG se habilitado
            context = ""
            if request.use_rag:
                search_results = rag.search(request.message)
                context = "\n\n".join([result["document"] for result in search_results])
            
            # Construir prompt com contexto
            system_prompt = request.system_prompt or "You are a helpful assistant."
            if context:
                system_prompt += f"\n\nContext:\n{context}"
            
            # Gerar resposta em streaming
            async for chunk in llm.generate_stream(
                prompt=request.message,
                system_prompt=system_prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ):
                yield f"data: {chunk}\n\n"
        
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"data: ERROR: {str(e)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


# Rotas de Upload
@app.post("/api/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint de upload de documentos
    Suporta PDF, TXT e Markdown
    """
    try:
        # Validar arquivo
        if not DocumentProcessor.validate_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Salvar arquivo
        file_id = str(uuid.uuid4())
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}_{file.filename}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Processar documento
        text, file_type = DocumentProcessor.process_file(file_path)
        
        # Dividir em chunks
        chunks = DocumentChunker.chunk_text(text)
        
        # Adicionar ao RAG
        rag = get_rag_system()
        metadata = DocumentMetadata.extract_metadata(file_path, file.filename)
        
        doc_ids = [f"{file_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [metadata] * len(chunks)
        
        rag.add_documents(chunks, metadatas, doc_ids)
        
        return DocumentUploadResponse(
            document_id=file_id,
            filename=file.filename,
            file_type=file_type,
            file_size=len(content),
            chunks_created=len(chunks),
        )
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Rotas de Busca
@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Endpoint de busca semântica
    """
    try:
        rag = get_rag_system()
        
        results = rag.search(
            query=request.query,
            top_k=request.top_k,
            threshold=request.threshold,
        )
        
        return SearchResponse(
            results=results,
            query=request.query,
            total_results=len(results),
        )
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Rotas de Coleção
@app.get("/api/collection/stats")
async def get_collection_stats():
    """Retorna estatísticas da coleção"""
    try:
        rag = get_rag_system()
        return rag.get_collection_stats()
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/collection/clear")
async def clear_collection():
    """Limpa toda a coleção"""
    try:
        rag = get_rag_system()
        rag.clear_collection()
        return {"status": "success", "message": "Collection cleared"}
    except Exception as e:
        logger.error(f"Clear error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
