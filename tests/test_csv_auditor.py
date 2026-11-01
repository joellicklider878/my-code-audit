import pytest
from pathlib import Path
import csv
from csv_auditor import CSV_Auditor

# Test valid row
def test_valid_row(tmp_path):
    input_file = tmp_path / 'input.csv'
    with input_file.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'email', 'amount'])
        writer.writerow(['123', 'John Doe', 'john@example.com', '10.99'])
    auditor = CSV_Auditor(str(input_file), str(tmp_path))
    auditor.run()
    with open(tmp_path / 'cleaned_records.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        assert rows == [['123', 'John Doe', 'john@example.com', '10.99']]

# Test missing email
def test_missing_email(tmp_path):
    input_file = tmp_path / 'input.csv'
    with input_file.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'email', 'amount'])
        writer.writerow(['123', 'John Doe', '', '10.99'])
    auditor = CSV_Auditor(str(input_file), str(tmp_path))
    with pytest.raises(ValueError):
        auditor.run()

# Test malformed email
def test_malformed_email(tmp_path):
    input_file = tmp_path / 'input.csv'
    with input_file.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'email', 'amount'])
        writer.writerow(['123', 'John Doe', 'john', '10.99'])
    auditor = CSV_Auditor(str(input_file), str(tmp_path))
    with pytest.raises(ValueError):
        auditor.run()

# Test duplicate customer ID
def test_duplicate_customer_id(tmp_path):
    input_file = tmp_path / 'input.csv'
    with input_file.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'email', 'amount'])
        writer.writerow(['123', 'John Doe', 'john@example.com', '10.99'])
        writer.writerow(['123', 'Jane Doe', 'jane@example.com', '5.99'])
    auditor = CSV_Auditor(str(input_file), str(tmp_path))
    with pytest.raises(ValueError):
        auditor.run()

# Test negative amount
def test_negative_amount(tmp_path):
    input_file = tmp_path / 'input.csv'
    with input_file.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'email', 'amount'])
        writer.writerow(['123', 'John Doe', 'john@example.com', '-10.99'])
    auditor = CSV_Auditor(str(input_file), str(tmp_path))
    with pytest.raises(ValueError):
        auditor.run()

# Test nonnumeric amount
def test_nonnumeric_amount(tmp_path):
    input_file = tmp_path / 'input.csv'
    with input_file.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'email', 'amount'])
        writer.writerow(['123', 'John Doe', 'john@example.com', 'ten.99'])
    auditor = CSV_Auditor(str(input_file), str(tmp_path))
    with pytest.raises(ValueError):
        auditor.run()

# Test missing required column
def test_missing_required_column(tmp_path):
    input_file = tmp_path / 'input.csv'
    with input_file.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'amount'])
        writer.writerow(['123', 'John Doe', '10.99'])
    auditor = CSV_Auditor(str(input_file), str(tmp_path))
    with pytest.raises(ValueError):
        auditor.run()

# Test preservation of the original input
def test_preservation_of_original_input(tmp_path):
    input_file = tmp_path / 'input.csv'
    with input_file.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'email', 'amount'])
        writer.writerow(['123', 'John Doe', 'john@example.com', '10.99'])
    original_input = input_file.read_text()
    auditor = CSV_Auditor(str(input_file), str(tmp_path))
    auditor.run()
    with open(input_file, 'r') as file:
        assert file.read() == original_input

# Test report counts
def test_report_counts(tmp_path):
    input_file = tmp_path / 'input.csv'
    with input_file.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'email', 'amount'])
        writer.writerow(['123', 'John Doe', 'john@example.com', '10.99'])
        writer.writerow(['123', 'Jane Doe', 'jane@example.com', '5.99'])
        writer.writerow(['456', 'Bob Smith', 'bob@example.com', '20.00'])
    auditor = CSV_Auditor(str(input_file), str(tmp_path))
    auditor.run()
    with open(tmp_path / 'cleaned_records.csv', 'r') as file:
        reader = csv.reader(file)
        cleaned_rows = list(reader)
        assert cleaned_rows == [['123', 'John Doe', 'john@example.com', '10.99'], ['456', 'Bob Smith', 'bob@example.com', '20.00']]
    with open(tmp_path / 'auditor_report.json', 'r') as file:
        report = json.load(file)
        assert report == {'total_records': 3, 'valid_records': 2, 'invalid_records': 1}