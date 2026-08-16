# Operational Reporting Data Pipeline

## Project Overview

This project builds a simple operational reporting data pipeline using Python and CSV files.

The pipeline simulates a common business scenario where an operational team receives raw service desk ticket data that needs to be validated, cleaned, transformed, and turned into reporting-ready outputs.

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
Summary report generation
        ↓
Repeatable one-command execution