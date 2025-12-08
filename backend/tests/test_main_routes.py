"""Tests ensuring the FastAPI app wires every router."""
from fastapi.routing import APIRoute

from app.main import create_app


def test_create_app_registers_all_core_routes():
    app = create_app()
    paths = {route.path for route in app.routes if isinstance(route, APIRoute)}
    expected_paths = {
        "/health",
        "/auth/login",
        "/certificados",
        "/dashboard/metricas",
        "/historicos/alunos/{aluno_id}",
        "/auditorias",
        "/inscricoes/{inscricao_id}/status",
        "/oficinas",
        "/presencas/oficinas/{oficina_id}",
        "/professores",
        "/relatorios/certificados",
        "/temas",
        "/users/admins",
    }

    for path in expected_paths:
        assert path in paths, f"Rota esperada não registrada: {path}"
