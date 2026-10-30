# SPDX-License-Identifier: MIT
"""Typed API request and response models derived from tool manifest."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .exceptions import PepkioAPIError


class RunOptions(BaseModel):
    """Optional fields for POST .../run."""

    idempotency_key: str | None = None
    label: str | None = None


class LabelData(BaseModel):
    """Reagent label metadata fields."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    concentration: str | None = None
    unit: str | None = None
    prep_date: str | None = None
    expiry: str | None = None
    lot: str | None = None
    hazards: list[str] = Field(default_factory=list)
    location: str | None = None
    color: str | None = None
    url: str | None = None


ActionType = Literal[
    "validate_label",
    "build_qr_content",
    "parse_csv",
    "generate_serial",
    "csv_template",
]


class ReagentQRLabelMakerInput(BaseModel):
    """Input payload for reagent-qr-label-maker tool."""

    model_config = ConfigDict(extra="allow")

    action: ActionType
    label: LabelData | dict[str, Any] | None = None
    csv_text: str | None = None
    serial_template: str | None = None
    serial_start: int | float | None = None
    serial_count: int | float | None = None


class RunResult(BaseModel):
    """Tool run response envelope."""

    model_config = ConfigDict(extra="allow")

    run_id: str
    status: str
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    result_url: str | None = None
    permalink: str | None = None
    duration_ms: int | None = None

    def raise_for_error(self) -> None:
        """Raise PepkioAPIError if the run response includes an error field."""
        if self.error is None:
            return
        err = self.error
        raise PepkioAPIError(
            err.get("message", "Tool run failed"),
            code=err.get("code"),
            details=err.get("details") if isinstance(err.get("details"), dict) else {},
            response_body={"run_id": self.run_id, "status": self.status, "error": self.error},
        )


def parse_run_response(data: dict[str, Any]) -> RunResult:
    """Parse a run API JSON body into RunResult."""
    return RunResult.model_validate(data)
