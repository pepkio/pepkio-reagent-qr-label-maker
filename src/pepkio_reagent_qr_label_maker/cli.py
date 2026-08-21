"""Click CLI for Pepkio reagent-qr-label-maker tool."""

from __future__ import annotations

import json
import sys
from typing import Any

import click

from .client import PepkioClient
from .config import DEFAULT_API_BASE_URL
from .exceptions import PepkioAPIError


@click.group()
@click.option("--base-url", default=None, help=f"API base URL (default: {DEFAULT_API_BASE_URL}).")
@click.option("--api-key", default=None, help="Pepkio API key (or set PEPKIO_API_KEY).")
@click.pass_context
def main(ctx: click.Context, base_url: str | None, api_key: str | None) -> None:
    """CLI for Pepkio reagent-qr-label-maker tool."""
    ctx.ensure_object(dict)
    ctx.obj["base_url"] = base_url
    ctx.obj["api_key"] = api_key


@main.command()
@click.option("--base-url", default=None, help=f"API base URL (default: {DEFAULT_API_BASE_URL}).")
@click.pass_context
def manifest(ctx: click.Context, base_url: str | None) -> None:
    """Fetch and output the tool manifest in JSON format."""
    resolved_base_url = base_url or ctx.obj.get("base_url")
    try:
        client = PepkioClient(base_url=resolved_base_url)
        data = client.get_manifest()
        click.echo(json.dumps(data, indent=2))
    except Exception as e:
        click.echo(f"Error fetching manifest: {e}", err=True)
        sys.exit(1)


@main.command(name="list-examples")
@click.option("--base-url", default=None, help=f"API base URL (default: {DEFAULT_API_BASE_URL}).")
@click.pass_context
def list_examples(ctx: click.Context, base_url: str | None) -> None:
    """List named examples available in the tool manifest."""
    resolved_base_url = base_url or ctx.obj.get("base_url")
    try:
        client = PepkioClient(base_url=resolved_base_url)
        examples = client.list_examples()
        if not examples:
            click.echo("No examples found in manifest.")
            return
        for ex in examples:
            click.echo(f"- {ex}")
    except Exception as e:
        click.echo(f"Error listing examples: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--example", "example_name", default=None, help="Name of manifest example to run.")
@click.option("--input-json", default=None, help="JSON string containing input parameters.")
@click.option(
    "--input-file", type=click.Path(exists=True), default=None, help="JSON file containing input."
)
@click.option("--base-url", default=None, help=f"API base URL (default: {DEFAULT_API_BASE_URL}).")
@click.option("--api-key", default=None, help="Pepkio API key (or set PEPKIO_API_KEY).")
@click.option("--idempotency-key", default=None, help="Optional idempotency key.")
@click.option("--label", default=None, help="Optional label for the run.")
@click.pass_context
def run(
    ctx: click.Context,
    example_name: str | None,
    input_json: str | None,
    input_file: str | None,
    base_url: str | None,
    api_key: str | None,
    idempotency_key: str | None,
    label: str | None,
) -> None:
    """Run the reagent-qr-label-maker tool."""
    resolved_base_url = base_url or ctx.obj.get("base_url")
    resolved_api_key = api_key or ctx.obj.get("api_key")
    client = PepkioClient(api_key=resolved_api_key, base_url=resolved_base_url)

    input_data: dict[str, Any] | None = None
    if example_name:
        try:
            input_data = client.get_example_input(example_name)
        except PepkioAPIError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
    elif input_json:
        try:
            input_data = json.loads(input_json)
        except json.JSONDecodeError as e:
            click.echo(f"Invalid JSON input: {e}", err=True)
            sys.exit(1)
    elif input_file:
        try:
            with open(input_file, encoding="utf-8") as f:
                input_data = json.load(f)
        except Exception as e:
            click.echo(f"Error reading input file: {e}", err=True)
            sys.exit(1)
    else:
        click.echo("Error: Must specify one of --example, --input-json, or --input-file.", err=True)
        sys.exit(1)

    try:
        result = client.run(
            input=input_data,
            idempotency_key=idempotency_key,
            label=label,
        )
        click.echo(json.dumps(result.model_dump(), indent=2))
    except Exception as e:
        click.echo(f"Run failed: {e}", err=True)
        sys.exit(1)


@main.command(name="get-run")
@click.argument("run_id")
@click.option("--base-url", default=None, help=f"API base URL (default: {DEFAULT_API_BASE_URL}).")
@click.option("--api-key", default=None, help="Pepkio API key (or set PEPKIO_API_KEY).")
@click.pass_context
def get_run(ctx: click.Context, run_id: str, base_url: str | None, api_key: str | None) -> None:
    """Fetch run result by ID."""
    resolved_base_url = base_url or ctx.obj.get("base_url")
    resolved_api_key = api_key or ctx.obj.get("api_key")
    client = PepkioClient(api_key=resolved_api_key, base_url=resolved_base_url)
    try:
        result = client.get_run(run_id)
        click.echo(json.dumps(result.model_dump(), indent=2))
    except Exception as e:
        click.echo(f"Failed to fetch run {run_id}: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
