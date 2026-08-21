"""Unit tests for PepkioClient with mocked HTTP responses."""

from __future__ import annotations

import json

import httpx
import pytest

from pepkio_reagent_qr_label_maker import PepkioAPIError, PepkioClient
from pepkio_reagent_qr_label_maker.models import LabelData, ReagentQRLabelMakerInput

MOCK_MANIFEST = {
    "schema_version": "1.0",
    "tool_id": "reagent-qr-label-maker",
    "title": "Reagent QR Label Maker",
    "execution_mode": "sync",
    "examples": [
        {
            "name": "validate_label_ok",
            "input": {
                "action": "validate_label",
                "label": {"name": "DMSO", "concentration": "100", "unit": "%"},
            },
        },
        {
            "name": "csv_template",
            "input": {"action": "csv_template"},
        },
    ],
}

MOCK_RUN_SUCCESS = {
    "run_id": "test-run-123",
    "status": "completed",
    "result": {"valid": True, "errors": {}, "warnings": {}},
    "error": None,
    "result_url": "https://tools.pepkio.com/api/tools/v1/runs/test-run-123",
    "permalink": "https://tools.pepkio.com/r/test-run-123",
}

MOCK_RUN_ERROR = {
    "run_id": "test-run-456",
    "status": "failed",
    "result": None,
    "error": {"code": "INVALID_INPUT", "message": "Missing required field action"},
}


def make_mock_client(handler) -> PepkioClient:
    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(
        transport=transport,
        base_url="https://tools.pepkio.com",
        headers={"Authorization": "Bearer test-key"},
    )
    return client


def test_get_manifest() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/reagent-qr-label-maker/manifest"
        return httpx.Response(200, json=MOCK_MANIFEST)

    client = make_mock_client(handler)
    manifest = client.get_manifest()
    assert manifest["tool_id"] == "reagent-qr-label-maker"
    assert len(client.list_examples()) == 2
    assert client.get_example_input("validate_label_ok")["action"] == "validate_label"


def test_run_success() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/reagent-qr-label-maker/run"
        body = json.loads(request.content)
        assert body["input"]["action"] == "validate_label"
        assert request.headers["Authorization"] == "Bearer test-key"
        return httpx.Response(200, json=MOCK_RUN_SUCCESS)

    client = make_mock_client(handler)
    res = client.run({"action": "validate_label", "label": {"name": "DMSO"}})
    assert res.run_id == "test-run-123"
    assert res.status == "completed"
    assert res.result == {"valid": True, "errors": {}, "warnings": {}}


def test_run_with_pydantic_input() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["input"]["action"] == "validate_label"
        assert body["input"]["label"]["name"] == "Ethanol"
        return httpx.Response(200, json=MOCK_RUN_SUCCESS)

    client = make_mock_client(handler)
    inp = ReagentQRLabelMakerInput(
        action="validate_label",
        label=LabelData(name="Ethanol", concentration="70", unit="%"),
    )
    res = client.run(inp)
    assert res.status == "completed"


def test_run_with_options() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["options"]["idempotency_key"] == "idem-1"
        assert body["options"]["label"] == "my-label"
        return httpx.Response(200, json=MOCK_RUN_SUCCESS)

    client = make_mock_client(handler)
    res = client.run(
        {"action": "validate_label"},
        idempotency_key="idem-1",
        label="my-label",
    )
    assert res.status == "completed"


def test_run_error_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=MOCK_RUN_ERROR)

    client = make_mock_client(handler)
    with pytest.raises(PepkioAPIError) as exc_info:
        client.run({"action": "invalid"})
    assert "Missing required field action" in str(exc_info.value)
    assert exc_info.value.code == "INVALID_INPUT"


def test_http_4xx_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            401, json={"error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}}
        )

    client = make_mock_client(handler)
    with pytest.raises(PepkioAPIError) as exc_info:
        client.run({"action": "validate_label"})
    assert exc_info.value.status_code == 401
    assert "Invalid API key" in str(exc_info.value)


def test_get_run() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/runs/test-run-123"
        return httpx.Response(200, json=MOCK_RUN_SUCCESS)

    client = make_mock_client(handler)
    res = client.get_run("test-run-123")
    assert res.run_id == "test-run-123"
    assert res.status == "completed"


def test_missing_api_key_raises() -> None:
    client = PepkioClient(api_key="")
    client._api_key = None
    with pytest.raises(ValueError, match="API key required"):
        client.run({"action": "validate_label"})


def test_convenience_methods() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        action = body["input"]["action"]
        if action == "validate_label":
            return httpx.Response(200, json={**MOCK_RUN_SUCCESS, "result": {"valid": True}})
        if action == "build_qr_content":
            return httpx.Response(200, json={**MOCK_RUN_SUCCESS, "result": {"qr_content": "DMSO"}})
        if action == "parse_csv":
            return httpx.Response(200, json={**MOCK_RUN_SUCCESS, "result": {"row_count": 1}})
        if action == "generate_serial":
            return httpx.Response(200, json={**MOCK_RUN_SUCCESS, "result": {"row_count": 5}})
        if action == "csv_template":
            return httpx.Response(
                200, json={**MOCK_RUN_SUCCESS, "result": {"mime_type": "text/csv"}}
            )
        return httpx.Response(400, json={"error": {"message": "Unknown action"}})

    client = make_mock_client(handler)

    v_res = client.validate_label({"name": "DMSO"})
    assert v_res.result["valid"] is True

    qr_res = client.build_qr_content({"name": "DMSO"})
    assert qr_res.result["qr_content"] == "DMSO"

    csv_res = client.parse_csv("name\nDMSO\n")
    assert csv_res.result["row_count"] == 1

    gen_res = client.generate_serial("Aliquot-###", 1, 5)
    assert gen_res.result["row_count"] == 5

    tmpl_res = client.get_csv_template()
    assert tmpl_res.result["mime_type"] == "text/csv"
