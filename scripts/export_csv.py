"""Export the traffic table from the SQLite database to data/traffic1.csv.

Run directly: python scripts/export_csv.py
"""
import csv
import os

import db

CSV_PATH = os.path.join(db.REPO_ROOT, "data", "traffic1.csv")


def export_traffic_csv(csv_path=CSV_PATH, db_path=db.DB_PATH):
    """Write every traffic row, under a header, to csv_path; returns the number of rows written."""
    rows = db.fetch_traffic(db_path)
    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(db.TRAFFIC_COLUMNS)
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    count = export_traffic_csv()
    print(f"Exported {count} traffic row(s) to {CSV_PATH}")
