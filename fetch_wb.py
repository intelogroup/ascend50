import requests
from config import WB_BASE, WB_INDICATORS


def get_period_id(cur, year):
    row = cur.execute(
        "SELECT period_id FROM time_periods WHERE year=? AND period_type='year'",
        (year,)
    ).fetchone()
    return row[0] if row else None


def upsert_economic(cur, loc_id, period_id, code, name, val):
    cur.execute("""INSERT OR IGNORE INTO economic_data
        (location_id, period_id, indicator_code, indicator_name, value, unit, source)
        VALUES (?, ?, ?, ?, ?, 'current_USD', 'WorldBank')""",
        (loc_id, period_id, code, name, val))


def fetch_worldbank(db):
    print("\n--- World Bank API ---")
    loc_id = db.execute(
        "SELECT location_id FROM locations WHERE location_code='HTI' AND admin_level=0"
    ).fetchone()
    if not loc_id:
        print("  SKIP: Haiti admin0 location not found")
        return
    loc_id = loc_id[0]

    cur = db.cursor()
    total_inserted = 0
    total_skipped = 0

    for code, name in WB_INDICATORS.items():
        url = f"{WB_BASE}/{code}?format=json&per_page=10000"
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  FAIL {code}: {e}")
            continue

        if not data or len(data) < 2 or not data[1]:
            print(f"  EMPTY {code}: {name}")
            continue

        records = data[1]
        inserted = 0
        skipped = 0
        for rec in records:
            if rec.get("value") is None:
                skipped += 1
                continue
            year = rec.get("date")
            if not year or not year.isdigit():
                skipped += 1
                continue
            year = int(year)
            val = float(rec["value"])
            pid = get_period_id(cur, year)
            if not pid:
                skipped += 1
                continue
            upsert_economic(cur, loc_id, pid, code, name, val)
            inserted += 1

        db.commit()
        total_inserted += inserted
        total_skipped += skipped
        blank = " (all nulls)" if inserted == 0 else ""
        print(f"  {code}: {inserted} rows inserted, {skipped} skipped{blank}")

    print(f"  TOTAL: {total_inserted} economic_data rows, {total_skipped} nulls skipped")
