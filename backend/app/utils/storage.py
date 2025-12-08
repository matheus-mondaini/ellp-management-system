"""Upload de arquivos para Supabase Storage."""
from __future__ import annotations

import logging
from typing import Any

from supabase import Client, create_client

from ..config import get_settings

logger = logging.getLogger(__name__)


def _get_supabase_client() -> Client:
    """Cria cliente Supabase com service role."""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def upload_pdf_certificado(
    pdf_bytes: bytes,
    filename: str,
    folder: str = "certificados",
) -> str:
    """
    Faz upload de PDF para Supabase Storage.
    
    Args:
        pdf_bytes: Conteúdo do PDF em bytes
        filename: Nome do arquivo (deve incluir .pdf)
        folder: Pasta no bucket (default: certificados)
    
    Returns:
        URL pública do arquivo
    
    Raises:
        Exception: Se o upload falhar
    """
    try:
        supabase = _get_supabase_client()
        bucket_name = "ellp-files"

        storage_path = f"{folder}/{filename}"

        response = supabase.storage.from_(bucket_name).upload(
            path=storage_path,
            file=pdf_bytes,
            file_options={
                "content-type": "application/pdf",
                "cache-control": "3600",
                "upsert": "true",
            },
        )

        public_url = supabase.storage.from_(bucket_name).get_public_url(storage_path)
        
        logger.info(f"PDF uploaded successfully: {storage_path}")
        return public_url
        
    except Exception as e:
        logger.error(f"Erro ao fazer upload do PDF: {e}")

        settings = get_settings()
        if settings.environment == "development":
            logger.warning("Usando URL mock devido a erro no upload (dev mode)")
            return f"https://storage.dev/certificados/{filename}"
        raise


def delete_pdf_certificado(filename: str, folder: str = "certificados") -> bool:
    """
    Remove PDF do Supabase Storage.
    
    Args:
        filename: Nome do arquivo
        folder: Pasta no bucket
    
    Returns:
        True se removido com sucesso, False caso contrário
    """
    try:
        supabase = _get_supabase_client()
        bucket_name = "ellp-files"
        storage_path = f"{folder}/{filename}"
        
        supabase.storage.from_(bucket_name).remove([storage_path])
        logger.info(f"PDF removed successfully: {storage_path}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao remover PDF: {e}")
        return False
