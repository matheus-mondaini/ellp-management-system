"""Geração de PDFs de certificados usando ReportLab."""
from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path
from typing import Literal

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


def _draw_border(c: canvas.Canvas, width: float, height: float) -> None:
    """Desenha borda decorativa no certificado."""
    c.setStrokeColor(colors.HexColor("#10b981"))
    c.setLineWidth(3)
    c.rect(1 * cm, 1 * cm, width - 2 * cm, height - 2 * cm)
    
    c.setStrokeColor(colors.HexColor("#059669"))
    c.setLineWidth(1)
    c.rect(1.2 * cm, 1.2 * cm, width - 2.4 * cm, height - 2.4 * cm)


def _draw_header(c: canvas.Canvas, width: float, y_position: float) -> float:
    """Desenha o cabeçalho do certificado."""
    c.setFillColor(colors.HexColor("#10b981"))
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(width / 2, y_position, "CERTIFICADO")
    
    return y_position - 1.5 * cm


def _draw_text_block(
    c: canvas.Canvas,
    text: str,
    width: float,
    y_position: float,
    font: str = "Helvetica",
    size: int = 12,
    color: str = "#1e293b",
    center: bool = True,
) -> float:
    """Desenha um bloco de texto no certificado."""
    c.setFont(font, size)
    c.setFillColor(colors.HexColor(color))
    
    if center:
        c.drawCentredString(width / 2, y_position, text)
    else:
        c.drawString(3 * cm, y_position, text)
    
    return y_position - (size / 72 * 2.54 * cm)  # Converte pontos para cm


def _draw_signature_block(c: canvas.Canvas, width: float, height: float) -> None:
    """Desenha o bloco de assinaturas."""
    y_position = 4 * cm
    
    # Linha de assinatura coordenador
    c.setStrokeColor(colors.HexColor("#64748b"))
    c.setLineWidth(1)
    line_start = width / 2 - 6 * cm
    line_end = width / 2 + 6 * cm
    c.line(line_start, y_position, line_end, y_position)
    
    # Nome e cargo
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawCentredString(width / 2, y_position - 0.5 * cm, "Coordenação do Projeto ELLP")
    c.drawCentredString(width / 2, y_position - 1 * cm, "Universidade Tecnológica Federal do Paraná")


def _draw_footer(c: canvas.Canvas, width: float, hash_validacao: str, codigo: str) -> None:
    """Desenha o rodapé com código de validação."""
    y_position = 2 * cm
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(width / 2, y_position, f"Código de validação: {codigo}")
    c.drawCentredString(width / 2, y_position - 0.4 * cm, f"Hash: {hash_validacao[:32]}...")
    c.drawCentredString(width / 2, y_position - 0.8 * cm, "Valide este certificado em: https://ellp.utfpr.edu.br/validar")


def gerar_certificado_aluno(
    nome_aluno: str,
    cpf_aluno: str,
    titulo_oficina: str,
    carga_horaria: int,
    periodo: str,
    percentual_presenca: float,
    hash_validacao: str,
    codigo_verificacao: str,
) -> bytes:
    """
    Gera certificado de conclusão para aluno.
    
    Args:
        nome_aluno: Nome completo do aluno
        cpf_aluno: CPF do aluno (formatado)
        titulo_oficina: Título da oficina concluída
        carga_horaria: Carga horária total em horas
        periodo: Período de realização (ex: "Janeiro a Março de 2025")
        percentual_presenca: Percentual de presença (0-100)
        hash_validacao: Hash único para validação
        codigo_verificacao: Código de 10 caracteres para validação
    
    Returns:
        Bytes do PDF gerado
    """
    buffer = io.BytesIO()
    width, height = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    
    # Desenhar elementos decorativos
    _draw_border(c, width, height)
    
    # Posição inicial
    y_pos = height - 3 * cm
    
    # Cabeçalho
    y_pos = _draw_header(c, width, y_pos)
    
    # Tipo de certificado
    y_pos = _draw_text_block(c, "de Conclusão", width, y_pos, "Helvetica-Oblique", 14, "#059669")
    y_pos -= 1 * cm
    
    # Texto principal
    y_pos = _draw_text_block(c, "Certificamos que", width, y_pos, "Helvetica", 14, "#475569")
    y_pos -= 0.3 * cm
    
    # Nome do aluno (destaque)
    y_pos = _draw_text_block(c, nome_aluno.upper(), width, y_pos, "Helvetica-Bold", 20, "#0f172a")
    y_pos -= 0.3 * cm
    
    # CPF
    y_pos = _draw_text_block(c, f"CPF: {cpf_aluno}", width, y_pos, "Helvetica", 10, "#64748b")
    y_pos -= 1 * cm
    
    # Texto da oficina
    texto_oficina = f"concluiu com êxito a oficina"
    y_pos = _draw_text_block(c, texto_oficina, width, y_pos, "Helvetica", 14, "#475569")
    y_pos -= 0.3 * cm
    
    # Título da oficina (destaque)
    y_pos = _draw_text_block(c, f'"{titulo_oficina}"', width, y_pos, "Helvetica-Bold", 16, "#0f172a")
    y_pos -= 1 * cm
    
    # Informações da oficina
    info_oficina = f"com carga horária de {carga_horaria} horas, realizada no período de {periodo},"
    y_pos = _draw_text_block(c, info_oficina, width, y_pos, "Helvetica", 12, "#475569")
    y_pos -= 0.3 * cm
    
    presenca_texto = f"obtendo {percentual_presenca:.1f}% de frequência."
    y_pos = _draw_text_block(c, presenca_texto, width, y_pos, "Helvetica", 12, "#475569")
    y_pos -= 1.5 * cm
    
    # Data de emissão
    data_emissao = datetime.now().strftime("%d de %B de %Y")
    meses_pt = {
        "January": "janeiro", "February": "fevereiro", "March": "março",
        "April": "abril", "May": "maio", "June": "junho",
        "July": "julho", "August": "agosto", "September": "setembro",
        "October": "outubro", "November": "novembro", "December": "dezembro"
    }
    for en, pt in meses_pt.items():
        data_emissao = data_emissao.replace(en, pt)
    
    y_pos = _draw_text_block(c, f"Emitido em {data_emissao}", width, y_pos, "Helvetica", 10, "#64748b")
    
    # Assinaturas
    _draw_signature_block(c, width, height)
    
    # Rodapé com validação
    _draw_footer(c, width, hash_validacao, codigo_verificacao)
    
    c.save()
    buffer.seek(0)
    return buffer.read()


def gerar_certificado_tutor(
    nome_tutor: str,
    cpf_tutor: str,
    titulo_oficina: str,
    carga_horaria: int,
    periodo: str,
    hash_validacao: str,
    codigo_verificacao: str,
) -> bytes:
    """
    Gera certificado de participação para tutor/voluntário.
    
    Args:
        nome_tutor: Nome completo do tutor
        cpf_tutor: CPF do tutor (formatado)
        titulo_oficina: Título da oficina ministrada
        carga_horaria: Carga horária total em horas
        periodo: Período de realização
        hash_validacao: Hash único para validação
        codigo_verificacao: Código de 10 caracteres
    
    Returns:
        Bytes do PDF gerado
    """
    buffer = io.BytesIO()
    width, height = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    _draw_border(c, width, height)

    y_pos = height - 3 * cm

    y_pos = _draw_header(c, width, y_pos)

    y_pos = _draw_text_block(c, "de Participação como Tutor", width, y_pos, "Helvetica-Oblique", 14, "#059669")
    y_pos -= 1 * cm

    y_pos = _draw_text_block(c, "Certificamos que", width, y_pos, "Helvetica", 14, "#475569")
    y_pos -= 0.3 * cm

    y_pos = _draw_text_block(c, nome_tutor.upper(), width, y_pos, "Helvetica-Bold", 20, "#0f172a")
    y_pos -= 0.3 * cm

    y_pos = _draw_text_block(c, f"CPF: {cpf_tutor}", width, y_pos, "Helvetica", 10, "#64748b")
    y_pos -= 1 * cm
    
    texto_oficina = f"atuou como tutor voluntário na oficina"
    y_pos = _draw_text_block(c, texto_oficina, width, y_pos, "Helvetica", 14, "#475569")
    y_pos -= 0.3 * cm
    
    y_pos = _draw_text_block(c, f'"{titulo_oficina}"', width, y_pos, "Helvetica-Bold", 16, "#0f172a")
    y_pos -= 1 * cm
    
    info_oficina = f"com carga horária de {carga_horaria} horas, realizada no período de {periodo},"
    y_pos = _draw_text_block(c, info_oficina, width, y_pos, "Helvetica", 12, "#475569")
    y_pos -= 0.3 * cm

    contribuicao = "contribuindo para a formação educacional e tecnológica de crianças e jovens."
    y_pos = _draw_text_block(c, contribuicao, width, y_pos, "Helvetica", 12, "#475569")
    y_pos -= 1.5 * cm

    data_emissao = datetime.now().strftime("%d de %B de %Y")
    meses_pt = {
        "January": "janeiro", "February": "fevereiro", "March": "março",
        "April": "abril", "May": "maio", "June": "junho",
        "July": "julho", "August": "agosto", "September": "setembro",
        "October": "outubro", "November": "novembro", "December": "dezembro"
    }
    for en, pt in meses_pt.items():
        data_emissao = data_emissao.replace(en, pt)

    y_pos = _draw_text_block(c, f"Emitido em {data_emissao}", width, y_pos, "Helvetica", 10, "#64748b")

    _draw_signature_block(c, width, height)

    _draw_footer(c, width, hash_validacao, codigo_verificacao)

    c.save()
    buffer.seek(0)
    return buffer.read()


def formatar_cpf(cpf: str) -> str:
    """Formata CPF para exibição."""
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf


def formatar_periodo(data_inicio: str, data_fim: str) -> str:
    """Formata período para exibição."""
    from datetime import datetime
    
    try:
        inicio = datetime.fromisoformat(data_inicio.replace("Z", "+00:00"))
        fim = datetime.fromisoformat(data_fim.replace("Z", "+00:00"))
        
        meses_pt = {
            1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
            5: "maio", 6: "junho", 7: "julho", 8: "agosto",
            9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
        }
        
        if inicio.year == fim.year:
            if inicio.month == fim.month:
                return f"{meses_pt[inicio.month]} de {inicio.year}"
            else:
                return f"{meses_pt[inicio.month]} a {meses_pt[fim.month]} de {inicio.year}"
        else:
            return f"{meses_pt[inicio.month]}/{inicio.year} a {meses_pt[fim.month]}/{fim.year}"
    except Exception:
        return f"{data_inicio} a {data_fim}"
