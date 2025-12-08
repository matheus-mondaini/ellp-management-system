"""Contract tests for public FastAPI endpoints using Schemathesis."""
import pytest
from schemathesis import openapi

from app.main import create_app

app = create_app()
schema = openapi.from_dict(app.openapi())
PUBLIC_ENDPOINTS = {("/health", "GET")}


@schema.parametrize()
def test_health_contract(case):
    if (case.path, case.method.upper()) not in PUBLIC_ENDPOINTS:
        pytest.skip("endpoint exige autenticação")

    response = case.call_asgi(app)
    case.validate_response(response)
