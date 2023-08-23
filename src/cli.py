import csv
import argparse

import delete
import secret

parser = argparse.ArgumentParser(
    prog="ampdelete",
    description="Deletes amplitude IDs from a Cohort CSV file"
)
parser.add_argument("csvfile")
args = parser.parse_args()

deleter = delete.Delete(secret.API_KEY, secret.SECRET_KEY)

amplitude_ids = []

with open(args.csvfile, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        amplitude_ids.append(row["amplitude_id"].strip())

expected_deletion_date = deleter.delete_amplitude_ids(amplitude_ids)
data = deleter.get_deletion_jobs(expected_deletion_date)
print(f"Registered deletion jobs for {expected_deletion_date}:", len(data["amplitude_ids"]))
print(f"Amplitude IDs in input CSV file", len(amplitude_ids))