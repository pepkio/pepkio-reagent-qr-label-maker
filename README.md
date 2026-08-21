# pepkio-reagent-qr-label-maker

Python client library and CLI for the Pepkio `reagent-qr-label-maker` tool.

## Installation

```bash
pip install pepkio-reagent-qr-label-maker
```

## Quickstart

```python
from pepkio_reagent_qr_label_maker import PepkioClient

client = PepkioClient(api_key="your-api-key")

# Validate a reagent label
res = client.validate_label({
    "name": "DMSO",
    "concentration": "100",
    "unit": "%",
    "prep_date": "2026-01-15",
    "expiry": "2027-01-15",
    "lot": "2401",
    "hazards": ["flammable"],
    "location": "-80°C Box 3",
    "color": "#0072b2"
})
print(res.result)

# Build QR code content
qr_res = client.build_qr_content({"name": "DMSO", "lot": "2401"})
print(qr_res.result["qr_content"])
```

## CLI Usage

```bash
# Fetch tool manifest
pepkio-reagent-qr-label-maker manifest

# List available manifest examples
pepkio-reagent-qr-label-maker list-examples

# Run tool using example
PEPKIO_API_KEY="your-api-key" pepkio-reagent-qr-label-maker run --example validate_label_ok

# Run tool with custom JSON
PEPKIO_API_KEY="your-api-key" pepkio-reagent-qr-label-maker run --input-json '{"action":"csv_template"}'
```
