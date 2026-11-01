
## Business Problem
The CSV Auditor is a tool designed to validate and clean CSV files by detecting missing values, malformed email addresses, duplicate customer IDs, non-numeric or negative amount values, and missing required columns.

## Features
*   Validates CSV files for missing values, malformed email addresses, duplicate customer IDs, non-numeric or negative amount values, and missing required columns
*   Cleans CSV files by writing valid records to a separate file and invalid records to another file with a rejection reason
*   Generates a summary report with statistics on the total records, valid records, and invalid records

## Project Structure
The project is structured into the following files and directories:
*   `src/csv_auditor.py`: The main Python script that performs the CSV auditing and cleaning
*   `tests/test_csv_auditor.py`: The test file that contains unit tests for the CSV Auditor

## Installation
To install the CSV Auditor, simply clone the repository and run the following command:
```bash
pip install -r requirements.txt
```

## Usage Examples
To use the CSV Auditor, simply run the following command:
```bash
python src/csv_auditor.py input.csv output_dir
```
Replace `input.csv` with the path to your CSV file and `output_dir` with the path to the directory where you want to save the cleaned records and summary report.

## Input and Output Formats
The CSV Auditor expects the input CSV file to have the following structure:
*   `customer_id`: A unique identifier for each customer
*   `name`: The name of the customer
*   `email`: The email address of the customer
*   `amount`: The amount due for each customer

The output files are in CSV format with the following structure:
*   `cleaned_records.csv`: The cleaned records with valid values
*   `rejected_records.csv`: The invalid records with a rejection reason
*   `auditor_report.json`: A summary report with statistics on the total records, valid records, and invalid records

## Testing Instructions
To test the CSV Auditor, simply run the following command:
```bash
pytest tests/test_csv_auditor.py
```
## Limitations
The CSV Auditor has the following limitations:
*   It only works with CSV files
*   It only detects the specified issues and does not perform any additional data validation or cleaning
*   It assumes that the input CSV file has the correct structure and format

## Privacy Note
All demonstration data is synthetic and not based on any real client or project. The CSV Auditor is not production-ready and should not be used in any production environment without further testing and validation.


