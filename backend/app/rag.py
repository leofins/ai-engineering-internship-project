"""
Módulo de RAG (Retrieval-Augmented Generation)
Implementa busca semântica e recuperação de documentos
"""
import os
from typing import List, Optional, Dict, Any
from config.settings import settings


class RAGSystem:
    """Sistema de RAG com ChromaDB"""
    
    def __init__(self):
        """Inicializa o sistema RAG"""
        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings
        except ImportError:
            raise ImportError("chromadb package not installed")
        
        # Criar diretório se não existir
        os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
        
        # Configurar ChromaDB
        self.client = chromadb.HttpClient() if os.getenv("CHROMA_HOST") else chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH
        )
        
        # Obter ou criar coleção
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
        """
        Adiciona documentos ao banco vetorial
        
        Args:
            documents: Lista de textos dos documentos
            metadatas: Lista de metadados para cada documento
            ids: Lista de IDs únicos para cada documento
        """
        if not documents:
            return
        
        # Gerar IDs se não fornecidos
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Adicionar à coleção
        self.collection.add(
            documents=documents,
            metadatas=metadatas or [{}] * len(documents),
            ids=ids,
        )
    
    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Busca documentos similares à query
        
        Args:
            query: Texto da busca
            top_k: Número de resultados (padrão: settings.TOP_K_RESULTS)
            threshold: Limiar de similaridade (padrão: settings.SIMILARITY_THRESHOLD)
        
        Returns:
            Lista de documentos com scores de similaridade
        """
        top_k = top_k or settings.TOP_K_RESULTS
        threshold = threshold or settings.SIMILARITY_THRESHOLD
        
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
        )
        
        # Formatar resultados
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                distance = results["distances"][0][i] if results["distances"] else 0
                # Converter distância para similaridade (1 - distância para cosine)
                similarity = 1 - distance
                
                if similarity >= threshold:
                    formatted_results.append({
                        "document": doc,
                        "similarity": similarity,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    })
        
        return formatted_results
    
    def delete_document(self, doc_id: str) -> None:
        """Remove um documento do banco vetorial"""
        self.collection.delete(ids=[doc_id])
    
    def clear_collection(self) -> None:
        """Limpa toda a coleção"""
        # Obter todos os IDs
        all_data = self.collection.get()
        if all_data["ids"]:
            self.collection.delete(ids=all_data["ids"])
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas da coleção"""
        all_data = self.collection.get()
        return {
            "total_documents": len(all_data["ids"]),
            "collection_name": settings.CHROMA_COLLECTION_NAME,
        }


class DocumentChunker:
    """Divide documentos em chunks para processamento"""
    
    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ) -> List[str]:
        """
        Divide texto em chunks com overlap
        
        Args:
            text: Texto a ser dividido
            chunk_size: Tamanho de cada chunk (padrão: settings.CHUNK_SIZE)
            chunk_overlap: Sobreposição entre chunks (padrão: settings.CHUNK_OVERLAP)
        
        Returns:
            Lista de chunks
        """
        chunk_size = chunk_size or settings.CHUNK_SIZE
        chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - chunk_overlap
        
        return chunks


# Instância global do RAG
_rag_system: Optional[RAGSystem] = None


def get_rag_system() -> RAGSystem:
    """Factory para obter instância do RAG"""
    global _rag_system
    if _rag_system is None:
        _rag_system = RAGSystem()
    return _rag_system
