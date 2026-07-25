#!/usr/bin/env python3
import sqlite3
from config import DB_PATH
from schema import create_schema
from seed_static import seed_all
from fetch_wb import fetch_worldbank
from fetch_hdx import fetch_hdx


def print_summary(db):
    tables = [
        "locations", "time_periods", "population_data", "food_security_data",
        "water_quality_data", "health_humanitarian_data", "economic_data",
        "hazards_data", "forest_data", "mineral_resources", "geothermal_data",
        "geological_data", "elevation_data", "satellite_imagery",
        "macroeconomic_data", "trade_data", "bilateral_trade_dr",
        "local_production", "plan_registry",
    ]
    print("\n=== DB Summary ===")
    total = 0
    for t in tables:
        row = db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()
        count = row[0] if row else 0
        total += count
        print(f"  {t}: {count}")
    print(f"  TOTAL: {total} rows")
    file_size = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    print(f"  DB file: {DB_PATH} ({file_size / 1024:.1f} KB)")


def main():
    print("=== Ascend50 - Haiti Data Hub ===")
    print(f"DB: {DB_PATH}")

    db = sqlite3.connect(str(DB_PATH))
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA journal_mode = WAL")

    print("\n--- Creating schema ---")
    create_schema(db)

    print("\n--- Seeding static data ---")
    seed_all(db)

    fetch_worldbank(db)
    fetch_hdx(db)

    print_summary(db)
    db.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
