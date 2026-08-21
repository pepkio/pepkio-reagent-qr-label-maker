# Pepkio Reagent QR Label Maker

A scientific Python client, CLI, and REST API interface for validating chemical reagent metadata, generating scannable 2D QR code barcode payloads, parsing batch CSV inventories, and creating serialized laboratory tube labels.

# Overview

In molecular biology, biochemistry, analytical chemistry, and clinical research laboratories, unidentifiable or mislabeled samples lead to experimental failure, lost reagents, and regulatory non-compliance. Traditional handwritten labels on microcentrifuge tubes, PCR strip tubes, and cryovials frequently smudge or fade when exposed to organic solvents like ethanol, water baths, ice, or liquid nitrogen temperatures (-196°C). Furthermore, handwritten tubes lack structured metadata, making it impossible to capture concentration units, preparation dates, lot numbers, storage locations, Safety Data Sheets (SDS), and Globally Harmonized System (GHS) hazard classification data on small tube surfaces.

The **Pepkio Reagent QR Label Maker** (`pepkio-reagent-qr-label-maker`) solves these challenges by providing a standardized computational pipeline to validate laboratory reagent metadata and format high-density 2D Matrix and Quick Response (QR) code barcode payloads. Researchers use this tool to transform unstructured reagent lists into standardized, scannable barcode structures suitable for thermal label printing, Electronic Lab Notebook (ELN) tracking, and Laboratory Information Management System (LIMS) integration.

Whether managing biobank cryovials, serial aliquot collections of restriction enzymes, cell culture media additives, or high-throughput chemical screening libraries, `pepkio-reagent-qr-label-maker` ensures complete sample traceability across the entire experimental lifecycle. The tool can be accessed programmatically via Python, invoked via command-line scripts, or used interactively via the web application interface at https://www.pepkio.com/tools/reagent-qr-label-maker.

Alternative terminology and common search terms associated with this domain include chemical reagent labeling software, laboratory 2D matrix barcode generator, cryovial QR label maker, lab tube barcode tracking, GHS hazard reagent tagging, aliquot serial number generator, and LIMS sample barcode parser.

# Features

- **Reagent Metadata Validation (`validate_label`)**: Validates reagent schemas including chemical name, concentration, concentration units, preparation date, expiration date, lot numbers, storage location, GHS hazard classifications, and custom LIMS URLs.
- **Structured QR Code Payload Generation (`build_qr_content`)**: Formats scannable 2D barcode payload strings optimized for thermal tube label printers, handheld 2D barcode scanners, and optical camera readers.
- **Batch CSV Parsing (`parse_csv`)**: Automatically ingests and validates bulk CSV files containing multi-reagent inventory spreadsheets into structured reagent data records.
- **Sequential Serial Label Generation (`generate_serial`)**: Generates custom serialized label series (e.g., `Aliquot-001` through `Aliquot-100`) with parameterized numeric padding, initial offsets, and batch counts.
- **Standardized CSV Schema Import (`csv_template`)**: Programmatically retrieves standardized CSV headers and templates to ensure seamless bulk data entry.
- **Python Client API (`PepkioClient`)**: Context-managed HTTP client built on `httpx` and `pydantic` for integration into automated biobanking scripts, Jupyter notebooks, and computational pipelines.
- **Command-Line Interface (`cli`)**: Complete CLI tool (`pepkio-reagent-qr-label-maker`) allowing scientists to inspect manifests, execute batch processing, and fetch run logs directly from terminal shell environments.
- **REST API Integration**: Direct synchronization with Pepkio server endpoints with support for idempotency keys, run tracking, and permalink generation.

# Common Use Cases

### 1. Biospecimen and Cryovial Labeling for Biobanking
Biobanks and biorepositories storing clinical serum, genomic DNA, total RNA, and tissue biopsies in liquid nitrogen vapor (-150°C to -196°C) require scannable 2D barcodes. `pepkio-reagent-qr-label-maker` validates patient lot numbers, extraction dates, and storage box locations, encoding them into a compact QR payload printed on cryo-resistant labels.

### 2. Serial Aliquot Tracking for Enzymes and Antibodies
High-value enzymes (e.g., reverse transcriptases, high-fidelity DNA polymerases, Cas9 ribonucleoproteins) and monoclonal antibodies undergo activity loss over repeated freeze-thaw cycles. Using `generate_serial`, researchers prepare 50 to 200 single-use aliquots tagged with sequential QR codes (`ENZ-LOT2026-001`), recording exact preparation dates and concentration values.

### 3. GHS Chemical Safety and Hazard Tagging
Secondary chemical containers (e.g., working solutions of 70% Ethanol, 1 M Tris-HCl, 10% SDS, Chloroform, β-Mercaptoethanol) prepared in the lab require compliance with OSHA and GHS labeling standards. The tool encodes specific GHS hazard codes (e.g., `Flammable`, `Corrosive`, `Toxic`) and expiry windows directly onto secondary container labels.

### 4. Compound Library Management for High-Throughput Screening
Bioinformaticians and assay developers preparing 96-well or 384-well compound stock plates use `parse_csv` to convert master chemical spreadsheets into scannable barcode records for automated liquid handling workstations and robotic plate readers.

### 5. LIMS and Electronic Lab Notebook (ELN) Synchronization
Researchers operating digital lab notebooks format QR code strings containing permalinks and GUIDs that link physical tube labels directly to digital experiment protocols, SDS documents, and analytical mass spectrometry data.

# Why This Tool Exists

Laboratory inventory management and reagent labeling are historically prone to human error and data loss due to reliance on manual record-keeping and basic spreadsheets:

1. **Physical Limitations of Handwritten Labels**: Microcentrifuge tubes (0.5 mL, 1.5 mL, 2.0 mL) have minimal printable surface area. Handwritten text frequently omits critical metadata such as lot numbers, buffer concentrations, or hazard warnings.
2. **Inconsistent Data Entry in Spreadsheets**: Traditional spreadsheet tools (Excel, CSV files) lack strict biological type enforcement. Date formats vary (`DD/MM/YYYY` vs `MM/DD/YYYY`), concentrations lack normalized units (`mM` vs `umol/L`), and missing values lead to silent downstream errors during assay setup.
3. **Unstandardized Barcode Encodings**: Off-the-shelf barcode software often generates non-standard QR payloads that cannot be parsed by standard LIMS barcode readers or smartphone cameras, causing workflow bottlenecks.
4. **Manual Serialization Overhead**: Manually numbering hundreds of aliquot tubes leads to duplicate serial numbers, skipped digits, and lost experimental traceability.

`pepkio-reagent-qr-label-maker` eliminates these manual failure points by standardizing data validation, barcode encoding, and batch serialization within a programmatic, reproducible architecture.

# Installation

Install the package from PyPI using `pip`:

```bash
pip install pepkio-reagent-qr-label-maker
```

The package is hosted on PyPI at https://pypi.org/project/pepkio-reagent-qr-label-maker/.

### Environment Configuration

To run operations against the Pepkio Tools API, set your API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_api_key_here"
```

Optionally override the API base URL for custom local development:

```bash
export PEPKIO_API_BASE_URL="https://tools.pepkio.com"
```

# Quick Start

### Python API Usage

The following example demonstrates initializing the client, validating reagent metadata, generating a scannable QR payload, and creating a serialized aliquot sequence:

```python
from pepkio_reagent_qr_label_maker import PepkioClient
from pepkio_reagent_qr_label_maker.models import LabelData, ReagentQRLabelMakerInput

# Initialize client (uses PEPKIO_API_KEY environment variable)
with PepkioClient() as client:
    
    # 1. Validate a reagent label structure
    label = LabelData(
        name="Tris-HCl Buffer",
        concentration="1.0",
        unit="M",
        prep_date="2026-08-21",
        expiry="2027-08-21",
        lot="LOT-TRIS-821",
        hazards=["Irritant"],
        location="Shelf-3B",
        color="#3B82F6",
        url="https://example.org/lims/reagents/TRIS-1001"
    )
    
    val_res = client.validate_label(label)
    print("Label Validation Status:", val_res.status)
    print("Is Valid:", val_res.result.get("valid"))

    # 2. Build scannable QR code payload content
    qr_res = client.build_qr_content(label)
    print("Generated QR Payload:\n", qr_res.result.get("qr_content"))

    # 3. Generate a batch of serialized aliquot label records
    serial_res = client.generate_serial(
        serial_template="RNA-Extract-###",
        serial_start=1,
        serial_count=5
    )
    print("Generated Serialized Records Count:", serial_res.result.get("row_count"))
    for row in serial_res.result.get("rows", []):
        print(f"ID: {row['id']} | QR Payload: {row['qr_content']}")

    # 4. Parse bulk CSV inventory string
    csv_text = "name,concentration,unit,lot\nBuffer A,10,mM,L001\nBuffer B,50,mM,L002"
    csv_res = client.parse_csv(csv_text)
    print("Parsed CSV Rows:", csv_res.result.get("row_count"))
```

### Command-Line Interface (CLI)

The CLI tool allows quick shell-based validation and execution:

```bash
# View tool manifest
pepkio-reagent-qr-label-maker manifest

# List available example configurations
pepkio-reagent-qr-label-maker list-examples

# Run a predefined example from the manifest
pepkio-reagent-qr-label-maker run --example validate_label_ok

# Run using custom JSON input string
pepkio-reagent-qr-label-maker run --input-json '{"action":"validate_label","label":{"name":"DMSO","concentration":"100","unit":"%"}}'

# Run using an input JSON file
pepkio-reagent-qr-label-maker run --input-file input_label.json
```

For interactive preview without writing code, access https://www.pepkio.com/tools/reagent-qr-label-maker.

# Example Output

### 1. `validate_label` Response
```json
{
  "run_id": "run-val-987654",
  "status": "completed",
  "result": {
    "valid": true,
    "errors": {},
    "warnings": {},
    "label": {
      "name": "Tris-HCl Buffer",
      "concentration": "1.0",
      "unit": "M",
      "prep_date": "2026-08-21",
      "expiry": "2027-08-21",
      "lot": "LOT-TRIS-821",
      "hazards": ["Irritant"],
      "location": "Shelf-3B",
      "color": "#3B82F6",
      "url": "https://example.org/lims/reagents/TRIS-1001"
    }
  },
  "error": null,
  "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run-val-987654",
  "permalink": "https://tools.pepkio.com/r/run-val-987654"
}
```

### 2. `generate_serial` Response
```json
{
  "run_id": "run-ser-123456",
  "status": "completed",
  "result": {
    "row_count": 3,
    "rows": [
      {
        "id": "RNA-Extract-001",
        "name": "RNA-Extract-001",
        "qr_content": "NAME:RNA-Extract-001|SER:001"
      },
      {
        "id": "RNA-Extract-002",
        "name": "RNA-Extract-002",
        "qr_content": "NAME:RNA-Extract-002|SER:002"
      },
      {
        "id": "RNA-Extract-003",
        "name": "RNA-Extract-003",
        "qr_content": "NAME:RNA-Extract-003|SER:003"
      }
    ]
  },
  "error": null,
  "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run-ser-123456",
  "permalink": "https://tools.pepkio.com/r/run-ser-123456"
}
```

# Scientific Background

### 1. Sample Traceability & Regulatory Compliance (GLP / GMP / ISO 17025)
In accredited life science testing and manufacturing environments operating under Good Laboratory Practice (GLP), Good Manufacturing Practice (GMP), or ISO/IEC 17025 standards, complete sample traceability is mandatory. Reagent identity, concentration, manufacturer lot number, preparation date, expiration date, and storage condition must be recorded for every assay component. Barcode tagging eliminates manual data transcription errors, fulfilling audit trail requirements.

### 2. 2D Barcode Encodings: QR Code vs. 1D Linear Barcodes
Traditional 1D linear barcodes (e.g., Code 128, Code 39) encode data horizontally only, requiring significant physical length to represent longer strings. On small laboratory containers such as 0.5 mL, 1.5 mL, and 2.0 mL microcentrifuge tubes or 1.0 mL cryovials, 1D barcodes are constrained to short alphanumeric identifiers (e.g., 6–8 characters).

In contrast, 2D Matrix symbologies (Quick Response / QR Code and Data Matrix) encode information both vertically and horizontally. This allows high data density within small footprints (e.g., 6 mm × 6 mm or 10 mm × 10 mm label areas).

$$\text{Data Density Ratio} = \frac{\text{Bytes Stored in 2D Matrix}}{\text{Print Area (mm}^2\text{)}} \gg \frac{\text{Bytes Stored in 1D Barcode}}{\text{Print Area (mm}^2\text{)}}$$

### 3. Reed-Solomon Error Correction for Harsh Storage Environments
Laboratory cryovials stored in ultra-low temperature (ULT) freezers (-80°C) or liquid nitrogen (-196°C) frequently accumulate ice frost, condensation, or physical abrasion. QR codes utilize **Reed-Solomon error correction** algorithms, enabling full data recovery even if a portion of the barcode is obscured or damaged.

Error correction capacity levels defined by ISO/IEC 18004 include:
- **Level L (Low)**: Recovers up to 7% damaged data.
- **Level M (Medium)**: Recovers up to 15% damaged data.
- **Level Q (Quartile)**: Recovers up to 25% damaged data.
- **Level H (High)**: Recovers up to 30% damaged data.

`pepkio-reagent-qr-label-maker` formats QR payload strings to balance text length and error correction overhead, ensuring robust scan performance under frost-covered conditions.

### 4. GHS Chemical Hazard Classification
Under the Globally Harmonized System of Classification and Labelling of Chemicals (GHS), secondary containers prepared in laboratories must display physical, health, and environmental hazards. Standard hazard classes encoded include:
- **Physical Hazards**: Flammable Liquids, Oxidizing Solvents, Corrosive Metals.
- **Health Hazards**: Acute Toxicity, Skin Corrosion/Irritation, Carcinogenicity, Specific Target Organ Toxicity.
- **Environmental Hazards**: Aquatic Toxicity.

### 5. Expiration and Stability Kinetics
Reagent stability in liquid solution depends on chemical kinetics modeled by the Arrhenius equation:

$$k = A \, e^{-\frac{E_a}{R T}}$$

Where:
- $k$ is the reaction rate constant of degradation.
- $A$ is the pre-exponential factor.
- $E_a$ is the activation energy of the decomposition reaction.
- $R$ is the universal gas constant ($8.314 \text{ J}/(\text{mol}\cdot\text{K})$).
- $T$ is absolute temperature in Kelvin.

Proper labeling of preparation date ($t_{\text{prep}}$) and expiration date ($t_{\text{exp}}$) ensures working reagents are discarded before kinetic breakdown leads to assay variability.

# Frequently Asked Questions

### What information should be included on a chemical reagent label?
A complete chemical reagent label should include the reagent name, concentration and units (e.g., 1.0 M, 50 mM), preparation date, expiration date, lot number, storage location, preparer initials, and relevant GHS hazard warnings (e.g., Corrosive, Flammable).

### Why use 2D QR codes instead of 1D linear barcodes on laboratory tubes?
2D QR codes store far more data in a much smaller physical footprint than 1D barcodes. A 10 mm × 10 mm QR code can store over 50 characters of structured metadata, whereas a 1D barcode of the same size can only store a few characters.

### How does QR code error correction work for frost-covered cryovials?
QR codes use Reed-Solomon error correction math to rebuild missing data modules. High error correction levels (Level Q or H) allow barcode scanners to read cryovial labels even when up to 25% to 30% of the surface is covered in frost or scratched.

### What is the standard GHS requirement for secondary container labeling?
GHS requires that secondary containers (such as diluted buffers or stock solutions transferred from manufacturer bottles) display the product identifier, signal word (Danger/Warning), hazard statements, and safety precautionary statements.

### How do I generate sequential serial QR code labels for batch aliquots?
Using `pepkio-reagent-qr-label-maker`, you can call the `generate_serial()` function with a template like `"ALIQUOT-###"`, setting `serial_start=1` and `serial_count=100` to produce 100 sequential scannable labels automatically.

### How does barcode scanning integrate with an Electronic Lab Notebook (ELN) or LIMS?
Scanning a scannable QR barcode payload transmits the encoded string or URL via HID keyboard emulation into an ELN or LIMS search bar, automatically opening the corresponding digital reagent entry.

### What size label is best for 1.5 mL microcentrifuge tubes and 2.0 mL cryovials?
Standard microcentrifuge tube cap labels are typically 9.5 mm or 11 mm in diameter. Side tube labels range from 0.9" × 0.5" (22.8 mm × 12.7 mm) to 1.5" × 0.75" (38.1 mm × 19.0 mm), designed for cryogenic adhesion.

### How can I convert a spreadsheet of chemical reagents into scannable QR code labels?
You can pass your CSV spreadsheet data into the `parse_csv()` method of `pepkio-reagent-qr-label-maker`, which parses and validates each row into structured label records ready for QR payload rendering.

### How does reagent degradation differ across freeze-thaw cycles?
Repeated freezing and thawing cause protein denaturation, aggregation, and pH shifts in buffer systems. Serial aliquot labeling helps track exact freeze-thaw counts and aliquot dates to maintain enzymatic activity.

### What is the difference between QR Code and Data Matrix 2D barcodes in lab automation?
Data Matrix barcodes are commonly used in industrial tube racks (e.g., 2D barcoded 96-well storage tubes), while QR codes offer broader compatibility with mobile devices, handheld camera scanners, and custom web links.

### How do I calculate reagent shelf life and expiration dates for working solutions?
Reagent shelf life depends on chemical stability at specific storage temperatures (-20°C, 4°C, room temperature). Expiration dates should be derived from vendor specifications or empirical stability testing and encoded directly into label metadata.

### What is the formula for calculating initial stock dilution C1V1 = C2V2 on reagent tags?
The dilution equation is $C_1 V_1 = C_2 V_2$, where $C_1$ is stock concentration, $V_1$ is stock volume to transfer, $C_2$ is target working concentration, and $V_2$ is final total volume.

### Can QR codes store direct URLs to Safety Data Sheets (SDS) and protocol documentation?
Yes. The `url` field in `LabelData` allows researchers to embed direct HTTP links to vendor Safety Data Sheets, standard operating procedures (SOPs), or LIMS record permalinks inside the QR code.

### How do I prevent label peeling and ink fading during liquid nitrogen storage (-196°C)?
Use cryo-specific polyester or vinyl label stock with solvent-resistant thermal transfer ribbon (resin ribbon) rather than direct thermal paper or standard inkjet printing.

### How does `pepkio-reagent-qr-label-maker` validate chemical metadata before printing?
The `validate_label()` function checks required fields, validates ISO date formats, verifies unit string structures, and flags potential missing safety information before label rendering.

### Is an API key required to run batch label generation with the Python library?
Yes, executing label validation and generation requests through `client.run()` requires a Pepkio API key set via `PEPKIO_API_KEY`. Inspecting the manifest schema (`get_manifest()`) does not require an API key.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/reagent-qr-label-maker

The web version provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools. It allows scientists to quickly preview labels, customize color coding, format batch serial numbers, and export barcode graphics directly from any web browser without local software installation.

# Related Resources

GitHub Repository: https://github.com/pepkio/pepkio-reagent-qr-label-maker

PyPI Package: https://pypi.org/project/pepkio-reagent-qr-label-maker/

Web Application: https://www.pepkio.com/tools/reagent-qr-label-maker

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

Scientific capabilities include:
- RNA-seq analysis
- Single-cell RNA-seq analysis
- Spatial transcriptomics analysis
- Functional enrichment analysis
- Custom bioinformatics workflows

Website: https://www.pepkio.com/

# Citation

If you use `pepkio-reagent-qr-label-maker` in your research, software pipelines, or laboratory workflows, please cite the software package as follows:

```bibtex
@software{pepkio_reagent_qr_label_maker_2026,
  author       = {{Pepkio Team}},
  title        = {Pepkio Reagent QR Label Maker: Python Client and API for Laboratory Reagent Metadata Validation and 2D Barcode Generation},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/pepkio/pepkio-reagent-qr-label-maker}},
  url          = {https://www.pepkio.com/tools/reagent-qr-label-maker}
}
```

Plain text:
Pepkio Team. (2026). *Pepkio Reagent QR Label Maker: Python Client and API for Laboratory Reagent Metadata Validation and 2D Barcode Generation*. Pepkio. https://github.com/pepkio/pepkio-reagent-qr-label-maker

# License

This project is licensed under the MIT License - see the LICENSE file for details.

# Keywords

- pepkio-reagent-qr-label-maker
- reagent-qr-label-maker
- reagent qr label maker
- lab tube qr code generator
- chemical reagent label software
- cryovial barcode generator
- 2d matrix barcode lab maker
- laboratory sample tracking
- ghs hazard label generator
- aliquot barcode generator
- lims barcode scanner payload
- microcentrifuge tube labeler
- cryogenic tube barcode
- reagent inventory management
- biobank sample tracking
- chemical lot number tracker
- reagent expiration date calculator
- 2d qr code thermal printing
- lab safety container tag
- pcr tube barcode generator
- chemical safety data sheet link qr
- reed-solomon error correction qr lab
- laboratory barcode generator python
- pipette reagent labeling
- sample traceability software
- secondary container ghs labeling
- biobanking cryovial qr tag
- antibody aliquot tracker
- restriction enzyme aliquot barcode
- cell culture media lot tracker
- buffer preparation label maker
- molarity concentration label
- lab inventory automation
- python lab barcode library
- pepkio tools api
- rest api reagent label
- pydantic reagent schema
- httpx lab client
- cli reagent label generator
- json qr payload maker
- how to generate qr code labels for lab tubes
- chemical reagent labeling best practices
- 2d matrix barcode vs 1d linear barcode on microcentrifuge tubes
- how to print cryogenic labels for liquid nitrogen storage
- generating sequential serial barcodes for aliquot tubes
- ghs chemical hazard secondary container labeling requirements
- converting excel reagent spreadsheet to scannable qr code labels
- how to store reagent lot numbers and expiration dates in qr code
- preventing label peeling and ink fading in -80 freeze
- integrating 2d barcode scanner with electronic lab notebook eln
- reed solomon error correction for frost covered cryovials
- python library for lab sample barcode metadata validation
- lims sample tracking barcode payload structure
- calculating reagent shelf life and expiration kinetics
- c1v1 c2v2 dilution formula on chemical reagent tags
- automated batch serial aliquot barcode generation script
- cryo thermal transfer label printing for biobanks
- open source laboratory inventory barcode generator
- reagent metadata schema validation pydantic python
- pepkio reagent qr label maker web application
