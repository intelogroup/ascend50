import sqlite3, os, math

IOM_API_KEY = os.getenv("IOM_DTM_API_KEY", "")

def f(v):
    return int(v) if (v and not (isinstance(v, float) and math.isnan(v))) else 0

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
    nat_id = row[0]

    inserted = 0

    # admin0 displacement
    try:
        data = api.get_idp_admin0_data(CountryName="Haiti")
    except Exception as e:
        print(f"  IOM DTM admin0 error: {e}")
        data = None

    if data is not None:
        for _, row in data.iterrows():
            total = row.get("numPresentIdpInd", 0)
            if not total or total == 0:
                continue
            year = int(row.get("yearReportingDate", 0))
            if not year:
                continue
            db.execute("INSERT OR IGNORE INTO time_periods (period_type, year) VALUES ('year', ?)", (year,))
            pid = db.execute("SELECT period_id FROM time_periods WHERE year=?", (year,)).fetchone()[0]
            db.execute("""INSERT OR IGNORE INTO displacement_data
                (location_id, period_id, total_idps, male_idps, female_idps,
                 displacement_reason, origin_location, round_number, reporting_date, source)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (nat_id, pid, int(total), f(row.get("numberMales", 0)), f(row.get("numberFemales", 0)),
                 str(row.get("displacementReason", "") or ""),
                 str(row.get("idpOriginAdmin1Name", "") or ""),
                 f(row.get("roundNumber", 0)),
                 str(row.get("reportingDate", "") or ""), "IOM DTM"))
            inserted += 1
        print(f"  IOM DTM admin0: {len(data)} rows")

    # admin1 displacement
    try:
        a1 = api.get_idp_admin1_data(CountryName="Haiti")
    except Exception as e:
        print(f"  IOM DTM admin1 error: {e}")
        a1 = None

    if a1 is not None and len(a1):
        for _, row in a1.iterrows():
            total = row.get("numPresentIdpInd", 0)
            if not total or total == 0:
                continue
            year = int(row.get("yearReportingDate", 0))
            if not year:
                continue
            loc = db.execute(
                "SELECT location_id FROM locations WHERE admin1_code=? AND admin_level=1",
                (row.get("admin1Pcode", ""),)
            ).fetchone()
            if not loc:
                loc = db.execute("SELECT location_id FROM locations WHERE admin_level=0").fetchone()
            lid = loc[0]
            db.execute("INSERT OR IGNORE INTO time_periods (period_type, year) VALUES ('year', ?)", (year,))
            pid = db.execute("SELECT period_id FROM time_periods WHERE year=?", (year,)).fetchone()[0]
            db.execute("""INSERT OR IGNORE INTO displacement_data
                (location_id, period_id, total_idps, male_idps, female_idps,
                 displacement_reason, origin_location, round_number, reporting_date, source)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (lid, pid, int(total), f(row.get("numberMales", 0)), f(row.get("numberFemales", 0)),
                 str(row.get("displacementReason", "") or ""),
                 str(row.get("idpOriginAdmin1Name", "") or ""),
                 f(row.get("roundNumber", 0)),
                 str(row.get("reportingDate", "") or ""), "IOM DTM admin1"))
            inserted += 1
        print(f"  IOM DTM admin1: {len(a1)} rows")

    db.commit()
    print(f"  IOM DTM: {inserted} displacement rows inserted total")

if __name__ == "__main__":
    from config import DB_PATH
    db = sqlite3.connect(DB_PATH)
    fetch_iom(db)
    db.close()
