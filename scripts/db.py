"""SQLite storage for the bike rental app: schema, input validation and inserts.

Every insert validates its input first, so unchecked user data never reaches
the database. SQLite does not enforce VARCHAR lengths, so the limits below do.
"""
import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(REPO_ROOT, "brental1")

SCHEMA = """
CREATE TABLE IF NOT EXISTS bikestn (
    id VARCHAR(6),
    code VARCHAR(60),
    byear VARCHAR(6),
    city VARCHAR(60),
    state VARCHAR(60),
    country VARCHAR(40),
    ccmobile VARCHAR(15)
);
CREATE TABLE IF NOT EXISTS traffic (
    n VARCHAR(4), ne VARCHAR(4), e VARCHAR(4), se VARCHAR(4),
    s VARCHAR(4), sw VARCHAR(4), w VARCHAR(4), nw VARCHAR(4)
);
"""

TRAFFIC_DIRECTIONS = {
    "n": "North",
    "ne": "North East",
    "e": "East",
    "se": "South East",
    "s": "South",
    "sw": "South West",
    "w": "West",
    "nw": "North West",
}
TRAFFIC_COLUMNS = tuple(TRAFFIC_DIRECTIONS)

# Accepted spellings of a direction's traffic state, mapped to the stored marker.
TRAFFIC_MARKERS = {"N": "N", "NORMAL": "N", "A": "A", "ABNORMAL": "A"}

# column: (form label, pattern the trimmed value must fully match, hint shown on error)
STATION_FIELDS = {
    "id": ("Station ID", r"[A-Za-z0-9]{1,6}", "1-6 letters or digits"),
    "code": ("Name", r".{1,60}", "1-60 characters"),
    "byear": ("Built-in Year", r"\d{4}", "a 4-digit year"),
    "city": ("City", r".{1,60}", "1-60 characters"),
    "state": ("State", r".{1,60}", "1-60 characters"),
    "country": ("Country", r".{1,40}", "1-40 characters"),
    "ccmobile": ("Customer Care Mobile ID", r"\+?\d{7,14}", "7-14 digits, optionally starting with +"),
}
STATION_COLUMNS = tuple(STATION_FIELDS)
EARLIEST_BUILD_YEAR = 1900


def connect(db_path=DB_PATH):
    """Open the database, creating the tables if they do not exist yet."""
    con = sqlite3.connect(db_path)
    con.executescript(SCHEMA)
    return con


@contextmanager
def transaction(db_path=DB_PATH):
    """Yield a connection that commits on success, rolls back on error and always closes."""
    con = connect(db_path)
    try:
        with con:
            yield con
    finally:
        con.close()


def validate_traffic(values):
    """Normalise 8 traffic entries (in TRAFFIC_COLUMNS order) to 'N'/'A' markers.

    Raises ValueError naming every entry that is not Normal/Abnormal.
    """
    values = list(values)
    if len(values) != len(TRAFFIC_COLUMNS):
        raise ValueError(f"Expected {len(TRAFFIC_COLUMNS)} traffic values, got {len(values)}.")
    markers, errors = [], []
    for column, value in zip(TRAFFIC_COLUMNS, values):
        marker = TRAFFIC_MARKERS.get(str(value).strip().upper())
        if marker is None:
            errors.append(f"{TRAFFIC_DIRECTIONS[column]}: {value!r} is not N (Normal) or A (Abnormal).")
        markers.append(marker)
    if errors:
        raise ValueError("\n".join(errors))
    return tuple(markers)


def validate_station(fields):
    """Trim and check a {column: text} mapping of bike station details.

    Returns the values in STATION_COLUMNS order; raises ValueError naming every invalid field.
    """
    row, errors = [], []
    for column, (label, pattern, hint) in STATION_FIELDS.items():
        value = str(fields.get(column, "")).strip()
        if not re.fullmatch(pattern, value):
            errors.append(f"{label}: must be {hint}.")
        elif column == "byear" and not EARLIEST_BUILD_YEAR <= int(value) <= date.today().year:
            errors.append(f"{label}: must be between {EARLIEST_BUILD_YEAR} and {date.today().year}.")
        row.append(value)
    if errors:
        raise ValueError("\n".join(errors))
    return tuple(row)


def insert_traffic(values, db_path=DB_PATH):
    """Validate and store one traffic record; returns the stored row."""
    row = validate_traffic(values)
    with transaction(db_path) as con:
        con.execute("INSERT INTO traffic (n, ne, e, se, s, sw, w, nw) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row)
    return row


def insert_station(fields, db_path=DB_PATH):
    """Validate and store one bike station; returns the stored row.

    Raises ValueError if the input is invalid or the station ID is already taken.
    """
    row = validate_station(fields)
    with transaction(db_path) as con:
        if con.execute("SELECT 1 FROM bikestn WHERE id = ?", (row[0],)).fetchone():
            raise ValueError(f"Station ID: {row[0]!r} already exists.")
        con.execute(
            "INSERT INTO bikestn (id, code, byear, city, state, country, ccmobile) VALUES (?, ?, ?, ?, ?, ?, ?)",
            row,
        )
    return row


def fetch_traffic(db_path=DB_PATH):
    """Return every traffic row as a tuple in TRAFFIC_COLUMNS order."""
    with transaction(db_path) as con:
        return con.execute("SELECT n, ne, e, se, s, sw, w, nw FROM traffic").fetchall()


def fetch_stations(db_path=DB_PATH):
    """Return every bike station row as a tuple in STATION_COLUMNS order."""
    with transaction(db_path) as con:
        return con.execute("SELECT id, code, byear, city, state, country, ccmobile FROM bikestn").fetchall()
