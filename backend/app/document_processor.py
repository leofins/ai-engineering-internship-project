"""
Módulo de processamento de documentos
Suporta PDF, TXT e Markdown
"""
import os
from typing import List, Tuple, Optional
from pathlib import Path


class DocumentProcessor:
    """Processa diferentes tipos de documentos"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extrai texto de arquivo PDF"""
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ImportError("pypdf package not installed")
        
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        return text
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """Extrai texto de arquivo TXT"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    
    @staticmethod
    def extract_text_from_md(file_path: str) -> str:
        """Extrai texto de arquivo Markdown"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    
    @staticmethod
    def process_file(file_path: str) -> Tuple[str, str]:
        """
        Processa arquivo e extrai texto
        
        Args:
            file_path: Caminho do arquivo
        
        Returns:
            Tupla (texto, tipo_de_arquivo)
        """
        file_ext = Path(file_path).suffix.lower().lstrip(".")
        
        if file_ext == "pdf":
            text = DocumentProcessor.extract_text_from_pdf(file_path)
        elif file_ext == "txt":
            text = DocumentProcessor.extract_text_from_txt(file_path)
        elif file_ext == "md":
            text = DocumentProcessor.extract_text_from_md(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        return text, file_ext
    
    @staticmethod
    def validate_file(file_path: str, allowed_extensions: Optional[List[str]] = None) -> bool:
        """
        Valida se o arquivo é permitido
        
        Args:
            file_path: Caminho do arquivo
            allowed_extensions: Lista de extensões permitidas
        
        Returns:
            True se válido, False caso contrário
        """
        from config.settings import settings
        
        allowed_extensions = allowed_extensions or settings.ALLOWED_EXTENSIONS
        file_ext = Path(file_path).suffix.lower().lstrip(".")
        
        return file_ext in allowed_extensions


class DocumentMetadata:
    """Gerencia metadados de documentos"""
    
    @staticmethod
    def extract_metadata(file_path: str, original_filename: str) -> dict:
        """
        Extrai metadados do documento
        
        Args:
            file_path: Caminho do arquivo
            original_filename: Nome original do arquivo
        
        Returns:
            Dicionário com metadados
        """
        file_stat = os.stat(file_path)
        file_ext = Path(file_path).suffix.lower().lstrip(".")
        
        return {
            "filename": original_filename,
            "file_type": file_ext,
            "file_size": file_stat.st_size,
            "upload_path": file_path,
        }
