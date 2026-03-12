"""
Testes para o processador de documentos
"""
import pytest
import os
import tempfile
from app.document_processor import DocumentProcessor, DocumentMetadata


class TestDocumentProcessor:
    """Testes para o DocumentProcessor"""
    
    @pytest.fixture
    def temp_txt_file(self):
        """Cria um arquivo TXT temporário"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("This is a test document.\nWith multiple lines.\n")
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    @pytest.fixture
    def temp_md_file(self):
        """Cria um arquivo Markdown temporário"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Title\n\nThis is a markdown document.\n")
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    def test_extract_text_from_txt(self, temp_txt_file):
        """Testa extração de texto de TXT"""
        text = DocumentProcessor.extract_text_from_txt(temp_txt_file)
        
        assert "test document" in text
        assert "multiple lines" in text
    
    def test_extract_text_from_md(self, temp_md_file):
        """Testa extração de texto de Markdown"""
        text = DocumentProcessor.extract_text_from_md(temp_md_file)
        
        assert "Title" in text
        assert "markdown document" in text
    
    def test_validate_file_allowed(self, temp_txt_file):
        """Testa validação de arquivo permitido"""
        is_valid = DocumentProcessor.validate_file(temp_txt_file)
        assert is_valid is True
    
    def test_validate_file_not_allowed(self):
        """Testa validação de arquivo não permitido"""
        is_valid = DocumentProcessor.validate_file("test.exe")
        assert is_valid is False
    
    def test_process_txt_file(self, temp_txt_file):
        """Testa processamento de arquivo TXT"""
        text, file_type = DocumentProcessor.process_file(temp_txt_file)
        
        assert "test document" in text
        assert file_type == "txt"


class TestDocumentMetadata:
    """Testes para o DocumentMetadata"""
    
    @pytest.fixture
    def temp_file(self):
        """Cria um arquivo temporário"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("test content")
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    def test_extract_metadata(self, temp_file):
        """Testa extração de metadados"""
        metadata = DocumentMetadata.extract_metadata(temp_file, "test.txt")
        
        assert "filename" in metadata
        assert "file_type" in metadata
        assert "file_size" in metadata
        assert metadata["filename"] == "test.txt"
        assert metadata["file_type"] == "txt"
        assert metadata["file_size"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
