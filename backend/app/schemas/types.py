"""Shared custom schema types."""
from __future__ import annotations

from typing import Any

from email_validator import EmailNotValidError, validate_email
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import PydanticCustomError, core_schema


class RelaxedEmailStr(str):
    """Email string that allows reserved/testing domains like `.test`."""

    @classmethod
    def _validate(cls, value: Any, _info: core_schema.ValidationInfo | None = None) -> str:
        if not isinstance(value, str):
            raise PydanticCustomError("string_type", "Input should be a valid string")
        try:
            info = validate_email(value, test_environment=True)
        except EmailNotValidError as exc:  # pragma: no cover - defensive path
            raise PydanticCustomError("value_error", str(exc)) from exc
        return info.normalized

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(cls._validate)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema_: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Returning a basic email schema avoids pydantic trying to introspect the
        # custom plain validator, which is not JSON-serializable by default.
        return {"type": "string", "format": "email"}
