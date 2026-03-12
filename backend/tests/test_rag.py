"""
Testes para o sistema RAG
"""
import pytest
from app.rag import RAGSystem, DocumentChunker


class TestDocumentChunker:
    """Testes para o DocumentChunker"""
    
    def test_chunk_text_basic(self):
        """Testa divisão básica de texto"""
        text = "a" * 1000
        chunks = DocumentChunker.chunk_text(text, chunk_size=100, chunk_overlap=10)
        
        assert len(chunks) > 0
        assert all(len(chunk) <= 100 for chunk in chunks)
    
    def test_chunk_text_with_overlap(self):
        """Testa divisão com overlap"""
        text = "Hello world. " * 100
        chunks = DocumentChunker.chunk_text(text, chunk_size=50, chunk_overlap=10)
        
        # Verificar que há overlap entre chunks
        if len(chunks) > 1:
            # O final do primeiro chunk deve aparecer no início do segundo
            assert chunks[0][-10:] in chunks[1]
    
    def test_chunk_empty_text(self):
        """Testa divisão de texto vazio"""
        chunks = DocumentChunker.chunk_text("")
        assert len(chunks) == 1
        assert chunks[0] == ""


class TestRAGSystem:
    """Testes para o RAGSystem"""
    
    @pytest.fixture
    def rag(self):
        """Fixture para criar instância de RAG"""
        return RAGSystem()
    
    def test_add_documents(self, rag):
        """Testa adição de documentos"""
        docs = ["Document 1", "Document 2", "Document 3"]
        rag.add_documents(docs)
        
        stats = rag.get_collection_stats()
        assert stats["total_documents"] >= 3
    
    def test_search_documents(self, rag):
        """Testa busca de documentos"""
        docs = [
            "Python is a programming language",
            "JavaScript is used for web development",
            "Machine learning is a subset of AI",
        ]
        rag.add_documents(docs)
        
        results = rag.search("programming language", top_k=5)
        assert len(results) > 0
        assert results[0]["similarity"] > 0
    
    def test_search_with_threshold(self, rag):
        """Testa busca com threshold"""
        docs = ["Python programming", "JavaScript web"]
        rag.add_documents(docs)
        
        results = rag.search("Python", top_k=10, threshold=0.5)
        assert all(r["similarity"] >= 0.5 for r in results)
    
    def test_collection_stats(self, rag):
        """Testa estatísticas da coleção"""
        stats = rag.get_collection_stats()
        
        assert "total_documents" in stats
        assert "collection_name" in stats
        assert isinstance(stats["total_documents"], int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
