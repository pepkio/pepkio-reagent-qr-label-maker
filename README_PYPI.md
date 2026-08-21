# Pepkio Reagent QR Label Maker

A Python interface for validating laboratory reagent metadata, generating scannable 2D QR code barcodes, and managing serialized aliquot inventories for cryogenic tube labeling.

# What It Does

The `pepkio-reagent-qr-label-maker` package provides Python and CLI tools to standardize reagent record-keeping in life science laboratories. It validates chemical metadata—including concentrations, units, preparation and expiration dates, lot numbers, storage locations, and GHS hazard codes—and formats structured 2D QR code payload strings compatible with thermal label printers, handheld barcode scanners, LIMS systems, and electronic lab notebooks (ELNs). It also supports bulk CSV spreadsheet parsing and sequential serial barcode generation for multi-tube aliquot batches.

# Features

- **Metadata Validation**: Validates chemical names, concentration values and units, ISO dates, lot identifiers, storage locations, and GHS hazard classes.
- **2D QR Payload Formatting**: Encodes multi-field reagent metadata into scannable 2D barcode payload strings optimized for small tube surfaces.
- **Batch CSV Ingestion**: Ingests and parses multi-reagent inventory spreadsheets into structured, validated label records.
- **Sequential Aliquot Serialization**: Generates parameterized serial number sequences (e.g., `Aliquot-001` through `Aliquot-100`) for batch tube labeling.
- **Python Client API**: Context-managed HTTP client (`PepkioClient`) built with `httpx` and `pydantic` for programmatic pipeline integration.
- **Command-Line Interface**: Terminal commands (`pepkio-reagent-qr-label-maker`) for shell-based validation, manifest inspection, and batch execution.

# Installation

Install the package from PyPI using `pip`:

```bash
pip install pepkio-reagent-qr-label-maker
```

Set your API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_api_key_here"
```

# Quick Example

```python
from pepkio_reagent_qr_label_maker import PepkioClient
from pepkio_reagent_qr_label_maker.models import LabelData

with PepkioClient() as client:
    # 1. Validate reagent label metadata
    label = LabelData(
        name="Tris-HCl Buffer",
        concentration="1.0",
        unit="M",
        prep_date="2026-08-21",
        expiry="2027-08-21",
        lot="LOT-TRIS-821",
        hazards=["Irritant"],
        location="Shelf-3B"
    )
    val_res = client.validate_label(label)
    print("Is Valid:", val_res.result.get("valid"))

    # 2. Format 2D QR code barcode payload
    qr_res = client.build_qr_content(label)
    print("QR Payload:", qr_res.result.get("qr_content"))

    # 3. Generate sequential serial labels for enzyme aliquots
    serial_res = client.generate_serial(
        serial_template="Taq-Polymerase-###",
        serial_start=1,
        serial_count=5
    )
    for row in serial_res.result.get("rows", []):
        print(f"ID: {row['id']} | Payload: {row['qr_content']}")
```

# Typical Use Cases

- **Cryovial & Biobank Sample Tracking**: Encoding patient lot numbers, extraction dates, and freezer box coordinates onto cryogenic labels for ultra-low temperature storage (-80°C or liquid nitrogen).
- **Serial Aliquot Management**: Generating sequential barcodes (e.g., `ENZ-LOT2026-001` through `050`) for single-use enzyme and antibody aliquots to track freeze-thaw cycles.
- **Secondary Container GHS Compliance**: Encoding chemical safety hazards (e.g., Flammable, Corrosive) and expiration dates on laboratory working solutions.
- **Compound Library Ingestion**: Converting 96-well or 384-well chemical stock spreadsheets into scannable barcodes for automated liquid handlers and plate readers.
- **LIMS & ELN Integration**: Formatting QR payloads containing permalinks or GUIDs that link physical tube labels to digital laboratory notebooks.

# Scientific Background

- **2D Matrix vs. 1D Barcodes**: Microcentrifuge caps (0.5–2.0 mL) have minimal surface area. 1D barcodes store only short identifiers, whereas 2D QR codes encode multi-field metadata (concentration, dates, GHS warnings) within a compact 6–10 mm footprint.
- **Reed-Solomon Error Correction**: Frost accumulation and physical abrasion in cryogenic storage (-196°C) can obscure tube surfaces. QR codes incorporate Reed-Solomon error correction algorithms (Levels Q and H), allowing accurate scanning even when up to 25–30% of the barcode is damaged.
- **Reagent Degradation Kinetics**: Chemical decomposition follows the Arrhenius model ($k = A e^{-E_a / RT}$). Standardized preparation and expiration date tagging ensures degraded reagents are retired prior to assay failure.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/reagent-qr-label-maker

The web application provides interactive label previews, custom color coding, bulk serial generation, printable worksheets, and instant barcode graphics export directly in the browser without local software installation.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-reagent-qr-label-maker

Web Application: https://www.pepkio.com/tools/reagent-qr-label-maker

Source code, issue tracking, and contribution guidelines are maintained on GitHub.

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

- pepkio-reagent-qr-label-maker
- reagent-qr-label-maker
- reagent qr label maker
- laboratory barcode generator
- chemical reagent label software
- cryovial barcode generator
- 2d qr code maker
- sample tracking software
- ghs hazard label generator
- aliquot serial barcode
- lims barcode generator
- microcentrifuge tube labeler
- cryogenic tube barcode
- reagent inventory tracking
- biobank sample tracking
- chemical lot number tracker
- reagent expiration date calculator
- 2d matrix barcode generator
- lab safety container tag
- pcr tube label maker
- secondary container labeling
- biobanking sample tagging
- antibody aliquot tracker
- buffer preparation label
- python lab barcode library
- how to generate qr code labels for laboratory tubes
- chemical reagent labeling software for cryovials
- generating sequential serial barcodes for aliquot tubes
- 2d matrix barcode vs 1d linear barcode on microcentrifuge tubes
- ghs chemical hazard secondary container labeling requirements
- converting excel reagent spreadsheet to scannable qr code labels
- reed solomon error correction for frost covered cryovials
- python library for lab sample barcode metadata validation
- lims sample tracking barcode payload structure
- calculating reagent shelf life and expiration kinetics
- automated batch serial aliquot barcode generation script
- cryo thermal transfer label printing for biobanks
- open source laboratory inventory barcode generator
- reagent metadata schema validation pydantic python
- pepkio reagent qr label maker web application
