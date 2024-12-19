# Case Study for Principal Software Engineer Role

This repository contains the solution for the case study provided by the National Community Investment Fund (NCIF). The goal was to design and implement a scalable backend architecture that integrates diverse datasets, supports advanced analytics, and provides secure, efficient data retrieval. The solution includes data integration, analysis, and machine learning components, leveraging AWS and NLP capabilities.

---

## Project Overview

The project aims to:
1. Develop a scalable backend architecture for integrating structured and unstructured datasets.
2. Compute meaningful analytics such as branch density and air quality correlations.
3. Build an API that supports dynamic querying and integrates with machine learning models for predictions.
4. Enable natural language processing (NLP) for intuitive query handling.
5. Flask-based scripts run indefinitely on EC2 instances, acting as APIs to access these different functionalities.

---

## Features

### 1. Backend Architecture
- **Scalable Design**: Architected for multi-source data integration using AWS best practices.
- **Distributed EC2 Instances**:
  - Machine Learning, NLP, Analysis, and Integration functionalities run on separate EC2 instances to optimize performance and modularity.
  - A central flask/script is provided for each instance to access these functionalities seamlessly.
- **Data Handling**: Supports structured and unstructured data, integrated using SQLite.
- **Authentication**: Secure access via user authentication.

### 2. Data Integration
- Loaded and processed datasets including:
  - EPA Air Quality Data
  - FFIEC Summary of Deposits (SOD)
  - NCUA Credit Union Data
- Connected datasets using `Census Tract` and `FDIC Certificate Numbers` as master keys.
- **Note**: The file `Daily_Census_Tract-Level_PM2.5_Concentrations__2016_-_2020.csv` was 8.5 GB and is excluded from this repository.

### 3. Business Case Analysis
- Computed branch density by Census Tract.
- Identified and visualized Census Tracts with:
  - PM2.5 > 10
  - More than 5 bank and credit union branches.
- Explored correlations between air quality (PM2.5) and branch density.

### 4. API Implementation
- Aggregates data dynamically for queries such as:
  - Branch density categorized by air quality levels.
- Supports user-specified conditions (e.g., "PM2.5 above 15 and more than 5 branches").
- Predicts air pollution likelihood based on branch density and historical data using machine learning.

### 5. NLP Interface
- Natural Language Processing interface for intuitive data querying (e.g., “Show me all tracts with above-average air pollution and a bank branch”).

### 6. Configuration for Security
- The `config.ini` file is used to manage sensitive information and access credentials for:
  - AWS S3 buckets
  - EC2 instances
  - SageMaker services

---

## Repository Structure

```
├── Analysis/
│   ├── branch_density_original.py       # Branch density calculation
│   ├── correlation_analysis.py          # Correlation analysis between variables
│   ├── visualization_generation.py      # Code to generate visualizations
├── Config/
│   ├── config.ini                       # Configuration file for API and DB
├── Data/
│   ├── *.csv                            # Raw datasets (excluding large files)
│   ├── *.xlsx                           # Processed data files
│   ├── integrated_data.db               # Integrated SQLite database
├── Integration/
│   ├── data_integration_scripts.py      # Scripts for data integration
├── ML/
│   ├── model_training.py                # Machine learning model implementation
│   ├── prediction_scripts.py            # Prediction generation based on input queries
├── NLP/
│   ├── nlp_interface.py                 # NLP-based query interface
├── README.md                            # Project documentation
```

## Assumptions Made
- Datasets are accurate and well-structured.
- Integration relies on Census Tract and FDIC Certificate Numbers as unique keys.
- AWS S3 is the primary data storage system.
- Machine learning models were trained on provided EPA data and branch density features.
- EC2 instances are configured for specific functionalities.
