import csv
import json
import logging
import pathlib
import argparse

class CSV_Auditor:
    def __init__(self, input_file, output_dir):
        self.input_file = pathlib.Path(input_file)
        self.output_dir = pathlib.Path(output_dir)

    def validate_columns(self):
        with self.input_file.open('r') as file:
            reader = csv.reader(file)
            columns = next(reader)
            required_columns = ['customer_id', 'name', 'email', 'order_total']
            if not all(column in columns for column in required_columns):
                raise ValueError('Missing required columns')

    def check_for_missing_values(self):
        with self.input_file.open('r') as file:
            reader = csv.reader(file)
            for row in reader:
                if not all(value for value in row if value):
                    raise ValueError('Missing required values')

    def check_for_malformed_emails(self):
        with self.input_file.open('r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                email = row[2]
                if '@' not in email:
                    raise ValueError('Malformed email address')

    def check_for_duplicates(self):
        with self.input_file.open('r') as file:
            reader = csv.reader(file)
            next(reader)
            customer_ids = set()
            for row in reader:
                if row[0] in customer_ids:
                    raise ValueError('Duplicate customer ID')
                customer_ids.add(row[0])

    def check_for_nonnumeric_amounts(self):
        with self.input_file.open('r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                try:
                    float(row[6])
                except ValueError:
                    raise ValueError('Non-numeric amount value')

    def check_for_negative_amounts(self):
        with self.input_file.open('r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                try:
                    amount = float(row[6])
                    if amount < 0:
                        raise ValueError('Negative amount value')
                except ValueError:
                    raise ValueError('Non-numeric amount value')

    def clean_records(self):
        valid_records = []
        with self.input_file.open('r') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    self.validate_columns()
                    self.check_for_missing_values()
                    self.check_for_malformed_emails()
                    self.check_for_duplicates()
                    self.check_for_nonnumeric_amounts()
                    self.check_for_negative_amounts()
                    valid_records.append(row)
                except ValueError as e:
                    logging.error(f'Invalid record: {e}')
        with self.input_file.open('r') as file:
            reader = csv.reader(file)
            invalid_records = []
            for row in reader:
                try:
                    self.validate_columns()
                    self.check_for_missing_values()
                    self.check_for_malformed_emails()
                    self.check_for_duplicates()
                    self.check_for_nonnumeric_amounts()
                    self.check_for_negative_amounts()
                except ValueError as e:
                    logging.error(f'Invalid record: {e}')
                    invalid_records.append(row)
        with open(self.output_dir / 'cleaned_records.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(valid_records)
        with open(self.output_dir / 'rejected_records.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in invalid_records:
                row.append('Error: Invalid record')
                writer.writerow(row)

    def write_summary(self):
        with self.input_file.open('r') as file:
            reader = csv.reader(file)
            total_records = sum(1 for row in reader)
            valid_records = sum(1 for row in reader if all(value for value in row if value))
            invalid_records = total_records - valid_records
            summary = {
                'total_records': total_records,
                'valid_records': valid_records,
                'invalid_records': invalid_records
            }
            with open(self.output_dir / 'auditor_report.json', 'w') as file:
                json.dump(summary, file)

    def run(self):
        self.validate_columns()
        self.check_for_missing_values()
        self.check_for_malformed_emails()
        self.check_for_duplicates()
        self.check_for_nonnumeric_amounts()
        self.check_for_negative_amounts()
        self.clean_records()
        self.write_summary()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CSV Auditor')
    parser.add_argument('input_file', help='Path to input CSV file')
    parser.add_argument('output_dir', help='Path to output directory')
    args = parser.parse_args()
    auditor = CSV_Auditor(args.input_file, args.output_dir)
    auditor.run()