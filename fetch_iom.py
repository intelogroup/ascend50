import sqlite3, os

IOM_API_KEY = os.getenv("IOM_DTM_API_KEY", "")

def fetch_iom(db):
    if not IOM_API_KEY:
        print("  IOM DTM: no API key (set IOM_DTM_API_KEY in .env)")
        return

    try:
        from dtmapi import DTMApi
    except ImportError:
        print("  IOM DTM: dtmapi not installed (pip install dtmapi)")
        return

    api = DTMApi(subscription_key=IOM_API_KEY)

    cur = db.execute("SELECT location_id FROM locations WHERE admin_level=0")
    row = cur.fetchone()
    if not row:
        return
    loc_id = row[0]

    inserted = 0
    try:
        data = api.get_idp_admin0_data(CountryName="Haiti")
    except Exception as e:
        print(f"  IOM DTM API error: {e}")
        return

    for _, row in data.iterrows():
        total = row.get("IDPs", 0) or row.get("idps", 0) or row.get("total_idps", 0)
        if not total or total == 0:
            continue

        date = str(row.get("ReportingDate", "") or row.get("reporting_date", ""))
        year = date[:4] if len(date) >= 4 else ""
        if not year:
            continue

        db.execute(
            "INSERT OR IGNORE INTO time_periods (period_type, year) VALUES ('year', ?)",
            (int(year),)
        )
        pid = db.execute(
            "SELECT period_id FROM time_periods WHERE year=?",
            (int(year),)
        ).fetchone()[0]

        round_n = row.get("RoundNumber", 0) or row.get("round_number", 0)
        reason = row.get("DisplacementReason", "") or row.get("displacement_reason", "") or ""
        origin = row.get("OriginLocation", "") or row.get("origin", "") or ""
        male = row.get("Male", 0) or row.get("male_idps", 0) or 0
        female = row.get("Female", 0) or row.get("female_idps", 0) or 0

        db.execute("""INSERT OR IGNORE INTO displacement_data
            (location_id, period_id, total_idps, male_idps, female_idps,
             displacement_reason, origin_location, round_number, reporting_date, source)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (loc_id, pid, int(total), int(male), int(female),
             reason, origin, int(round_n), date, "IOM DTM"))
        inserted += 1

    db.commit()
    print(f"  IOM DTM: {inserted} displacement rows inserted")

if __name__ == "__main__":
    from config import DB_PATH
    db = sqlite3.connect(DB_PATH)
    fetch_iom(db)
    db.close()
