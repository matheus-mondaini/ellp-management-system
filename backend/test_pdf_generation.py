"""Script de teste para verificar geração de certificados PDF."""
from pathlib import Path

from app.utils.pdf_generator import (
    formatar_cpf,
    formatar_periodo,
    gerar_certificado_aluno,
    gerar_certificado_tutor,
)


def test_certificado_aluno():
    """Testa geração de certificado de aluno."""
    print("🎓 Gerando certificado de aluno...")
    
    pdf_bytes = gerar_certificado_aluno(
        nome_aluno="Maria Silva Santos",
        cpf_aluno=formatar_cpf("12345678901"),
        titulo_oficina="Introdução à Programação com Scratch",
        carga_horaria=40,
        periodo=formatar_periodo("2025-01-15", "2025-03-20"),
        percentual_presenca=92.5,
        hash_validacao="abc123def456789",
        codigo_verificacao="ABCD123456",
    )

    output_path = Path(__file__).parent / "test_certificado_aluno.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    print(f"✅ Certificado gerado com sucesso: {output_path}")
    print(f"📊 Tamanho: {len(pdf_bytes) / 1024:.2f} KB")


def test_certificado_tutor():
    """Testa geração de certificado de tutor."""
    print("\n👨‍🏫 Gerando certificado de tutor...")
    
    pdf_bytes = gerar_certificado_tutor(
        nome_tutor="João Pedro Oliveira",
        cpf_tutor=formatar_cpf("98765432100"),
        titulo_oficina="Robótica Educacional com LEGO Mindstorms",
        carga_horaria=30,
        periodo=formatar_periodo("2025-02-01", "2025-04-15"),
        hash_validacao="xyz789abc456def",
        codigo_verificacao="XYZ9876543",
    )

    output_path = Path(__file__).parent / "test_certificado_tutor.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    print(f"✅ Certificado gerado com sucesso: {output_path}")
    print(f"📊 Tamanho: {len(pdf_bytes) / 1024:.2f} KB")


if __name__ == "__main__":
    test_certificado_aluno()
    test_certificado_tutor()
    print("\n✨ Todos os testes concluídos!")
