"""Integration tests against live Pepkio API endpoints (Local and Production)."""

from __future__ import annotations

import pytest

from pepkio_reagent_qr_label_maker import PepkioClient
from pepkio_reagent_qr_label_maker.config import resolve_api_key, resolve_base_url


def get_integration_client() -> PepkioClient:
    base_url = resolve_base_url()
    api_key = resolve_api_key(base_url=base_url)
    if not api_key:
        pytest.skip(
            f"No API key available for {base_url} (set PEPKIO_API_KEY or LOCAL_PEPKIO_API_KEY)"
        )
    return PepkioClient(api_key=api_key, base_url=base_url)


def test_integration_manifest() -> None:
    base_url = resolve_base_url()
    client = PepkioClient(base_url=base_url)
    manifest = client.get_manifest()
    assert manifest["tool_id"] == "reagent-qr-label-maker"
    assert "execution_mode" in manifest
    assert len(manifest.get("examples", [])) > 0


def test_integration_run_validate_label() -> None:
    client = get_integration_client()
    example_input = client.get_example_input("validate_label_ok")
    res = client.run(example_input)

    assert res.run_id is not None
    assert res.status == "completed"
    assert res.result is not None
    assert res.result.get("valid") is True

    # Test get_run
    fetched = client.get_run(res.run_id)
    assert fetched.run_id == res.run_id
    assert fetched.status == "completed"


def test_integration_run_build_qr_content() -> None:
    client = get_integration_client()
    example_input = client.get_example_input("build_qr_content_json")
    res = client.run(example_input)

    assert res.status == "completed"
    assert res.result is not None
    assert "qr_content" in res.result


def test_integration_run_parse_csv() -> None:
    client = get_integration_client()
    example_input = client.get_example_input("parse_csv_ok")
    res = client.run(example_input)

    assert res.status == "completed"
    assert res.result is not None
    assert res.result.get("row_count") == 2


def test_integration_run_generate_serial() -> None:
    client = get_integration_client()
    example_input = client.get_example_input("generate_serial")
    res = client.run(example_input)

    assert res.status == "completed"
    assert res.result is not None
    assert res.result.get("row_count") == 3


def test_integration_run_csv_template() -> None:
    client = get_integration_client()
    example_input = client.get_example_input("csv_template")
    res = client.run(example_input)

    assert res.status == "completed"
    assert res.result is not None
    assert res.result.get("mime_type") == "text/csv"
