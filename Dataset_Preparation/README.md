# Dataset_Preparation Folder Structure

## Overview
This folder contains all scripts, data, and utilities for preparing, cleaning, and processing F1 strategy datasets. The structure is designed for clarity, maintainability, and separation of concerns.

## Structure
- `data_raw/` — Original, untouched CSVs.
- `data_processed/` — Cleaned, normalized, or feature-engineered CSVs.
- `data_cleaning/` — Data cleaning scripts and utilities.
- `data_visualization/` — Visualization scripts and utilities.
- `pipelines/` — End-to-end pipeline scripts.
- `normalization/` — Scripts for normalization and name mapping.
- `selection/` — Scripts for selection and filtering.
- `tests/` — All test scripts, notebooks, and test CSVs.
- `__pycache__/` — Python cache files (should be ignored in version control).
- `README.md` — This documentation file.
- `DEVLOG.md` — Development log and notes.

## Usage
- Place new raw data in `data_raw/`.
- Save processed outputs in `data_processed/`.
- Add new cleaning or visualization functions to their respective folders.
- Keep test scripts and data in `tests/`.

## Contact
For questions, contact the repository owner.
