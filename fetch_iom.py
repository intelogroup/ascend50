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
        total = row.get("numPresentIdpInd", 0)
        if not total or total == 0:
            continue

        year = int(row.get("yearReportingDate", 0))
        if not year:
            continue

        db.execute(
            "INSERT OR IGNORE INTO time_periods (period_type, year) VALUES ('year', ?)",
            (year,)
        )
        pid = db.execute(
            "SELECT period_id FROM time_periods WHERE year=?",
            (year,)
        ).fetchone()[0]

        import math
        def f(v):
            return int(v) if (v and not (isinstance(v, float) and math.isnan(v))) else 0
        round_n = f(row.get("roundNumber", 0))
        reason = str(row.get("displacementReason", "") or "")
        origin = str(row.get("idpOriginAdmin1Name", "") or "")
        male = f(row.get("numberMales", 0))
        female = f(row.get("numberFemales", 0))
        date = str(row.get("reportingDate", "") or "")

        db.execute("""INSERT OR IGNORE INTO displacement_data
            (location_id, period_id, total_idps, male_idps, female_idps,
             displacement_reason, origin_location, round_number, reporting_date, source)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (loc_id, pid, int(total), male, female,
             reason, origin, round_n, date, "IOM DTM"))
        inserted += 1

    db.commit()
    print(f"  IOM DTM: {inserted} displacement rows inserted")

if __name__ == "__main__":
    from config import DB_PATH
    db = sqlite3.connect(DB_PATH)
    fetch_iom(db)
    db.close()
