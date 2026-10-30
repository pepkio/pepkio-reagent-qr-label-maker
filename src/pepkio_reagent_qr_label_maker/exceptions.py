# SPDX-License-Identifier: MIT
"""Exceptions for Pepkio API client."""

from __future__ import annotations

from typing import Any


class PepkioAPIError(Exception):
    """Exception raised when a Pepkio API request fails or returns an error response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}
        self.response_body = response_body or {}

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code:
            parts.append(f"(HTTP status: {self.status_code})")
        if self.code:
            parts.append(f"(Code: {self.code})")
        return " ".join(parts)
