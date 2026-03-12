"""
Modelos Pydantic para requisições e respostas da API
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Requisição de chat"""
    message: str = Field(..., min_length=1, max_length=5000)
    use_rag: bool = True
    system_prompt: Optional[str] = None
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(2000, ge=100, le=4000)


class ChatResponse(BaseModel):
    """Resposta de chat"""
    response: str
    sources: List[Dict[str, Any]] = []
    model: str
    timestamp: datetime


class StreamChunk(BaseModel):
    """Chunk de resposta em streaming"""
    content: str
    is_final: bool = False


class DocumentUploadResponse(BaseModel):
    """Resposta de upload de documento"""
    document_id: str
    filename: str
    file_type: str
    file_size: int
    chunks_created: int
    status: str = "success"


class SearchRequest(BaseModel):
    """Requisição de busca"""
    query: str = Field(..., min_length=1, max_length=5000)
    top_k: Optional[int] = Field(5, ge=1, le=20)
    threshold: Optional[float] = Field(0.3, ge=0.0, le=1.0)


class SearchResult(BaseModel):
    """Resultado de busca"""
    document: str
    similarity: float
    metadata: Dict[str, Any]


class SearchResponse(BaseModel):
    """Resposta de busca"""
    results: List[SearchResult]
    query: str
    total_results: int


class CollectionStats(BaseModel):
    """Estatísticas da coleção"""
    total_documents: int
    collection_name: str


class HealthResponse(BaseModel):
    """Resposta de health check"""
    status: str = "healthy"
    version: str
    llm_provider: str
    rag_system: str = "chromadb"


class ErrorResponse(BaseModel):
    """Resposta de erro"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime
