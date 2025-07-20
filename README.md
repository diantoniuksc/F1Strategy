
# F1 Tyre Life Prediction Project

This project analyzes Formula 1 race data to predict tyre life using machine learning models such as LightGBM, Random Forest, and Linear Regression. It includes data pipelines for session extraction, feature engineering, and model training. The codebase supports data cleaning, feature selection, and model evaluation, with a focus on tyre compound analysis and stint strategies.

## Main Features
- Automated extraction of F1 session data using FastF1
- Data cleaning, normalization, and feature engineering scripts
- Model training with LightGBM, Random Forest, and Linear Regression
- Tools for encoding categorical features and handling outliers
- Visualization of feature importances and tyre compound statistics
- Utilities for filtering and transforming CSV datasets
- Modular pipeline for experimenting with different features and models

## Directory Structure
- `Dataset_Preparation/`: Scripts and CSVs for data cleaning and preparation
- `Model_Training/`: Model training scripts and baseline models
- `README.md`: Project instructions and overview

## Getting Started
# Allow running local scripts for this session (required for activation script)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Create a new virtual environment named 'venv'
python -m venv venv

# (Alternative) Activate the virtual environment (Command Prompt)
venv\Scripts\activate

# Install the fastf1 module inside the virtual environment
pip install fastf1
pip install scikit-learn
pip install seaborn

# --- Data Set Preparation ---
# To generate the all_years_sessions.csv file with all session data, run the batch pipeline script:
python batch_pipeline.py
# The generated file all_years_sessions.csv will be saved in the Dataset_Preparation directory.
