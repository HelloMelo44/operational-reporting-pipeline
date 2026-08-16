# Operational Reporting Data Pipeline

## Project Overview

This project builds a simple operational reporting data pipeline using Python and CSV files.

The pipeline simulates a common business scenario where an operational team receives raw service desk ticket data that needs to be validated, cleaned, transformed, checked for quality, and turned into reporting-ready outputs.

The goal is to demonstrate practical data engineering skills in a clear, repeatable, and portfolio-friendly way.

## Business Problem

Operational teams often receive raw exports from systems such as service desks, workflow tools, customer portals, or enterprise applications.

Before the data can be used for reporting, it usually needs to be checked, cleaned, standardised, and transformed.

Manual reporting can lead to repeated work, inconsistent calculations, and reporting errors.

This project shows how a simple pipeline can make that process more reliable.

## Pipeline Flow

The pipeline follows this process:

```text
Raw service ticket data
        ↓
Column validation
        ↓
Data cleaning and standardisation
        ↓
Processed reporting dataset
        ↓
Data quality checks
        ↓
Summary report generation
        ↓
Repeatable one-command execution

## How to Run

Clone the repository:

```bash
git clone https://github.com/HelloMelo44/operational-reporting-pipeline.git
cd operational-reporting-pipeline
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the full pipeline:

```bash
python scripts/run_pipeline.py
```

This command runs the full pipeline:

1. Processes the raw service ticket dataset.
2. Saves the cleaned dataset to `data/processed`.
3. Generates a data quality report in `reports`.
4. Generates reporting summary files in `reports`.
5. Writes pipeline execution details to `logs/pipeline.log`.