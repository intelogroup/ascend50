import urllib.request, urllib.parse, json
import sqlite3, sys

BASE = "https://ghoapi.azureedge.net/api"

INDICATORS = [
    ("WHOSIS_000001", "Life expectancy at birth", "years"),
    ("WHOSIS_000002", "Healthy life expectancy at birth", "years"),
    ("WHOSIS_000003", "Neonatal mortality rate", "per_1000"),
    ("WHOSIS_000004", "Adult mortality rate (15-60)", "per_1000"),
    ("MDG_0000000001", "Infant mortality rate", "per_1000"),
    ("MDG_0000000007", "Under-5 mortality rate", "per_1000"),
    ("MDG_0000000026", "Maternal mortality ratio", "per_100k"),
    ("MORTADO", "Adolescent mortality rate", "per_1000"),
    ("CHILDMORT5TO14", "Child mortality 5-14", "per_1000"),
    ("WHS2_131", "Age-standardized NCD mortality", "per_100k"),
    ("SDGWSHBOD", "WASH-attributed mortality", "per_100k"),
    ("SDGPOISON", "Unintentional poisoning mortality", "per_100k"),
    ("WHS6_102", "Hospital beds", "per_10k"),
    ("HWF_0006", "Nursing/midwifery personnel", "per_10k"),
    ("HWF_0024", "Community health workers", "number"),
    ("MALARIA_EST_INCIDENCE", "Malaria incidence", "per_1000"),
    ("NCD_HYP_DIAGNOSIS_A", "Hypertension diagnosis coverage", "percent"),
    ("GHED_CHEGDP_SHA2011", "Current health expenditure (% GDP)", "percent"),
    ("GHED_GGHE-DGDP_SHA2011", "Govt health expenditure (% GDP)", "percent"),
    ("GHED_OOPSCHE_SHA2011", "Out-of-pocket health expenditure (% CHE)", "percent"),
    ("GHED_EXTCHE_SHA2011", "External health expenditure (% CHE)", "percent"),
    ("GHED_CHE_pc_US_SHA2011", "Health expenditure per capita", "USD"),
]

def fetch_who(db):
    cur = db.execute("SELECT location_id FROM locations WHERE admin_level=0")
    row = cur.fetchone()
    if not row:
        print("  WHO: no national location found")
        return
    loc_id = row[0]

    inserted = 0
    for code, ind_name, unit in INDICATORS:
        q = "$filter=SpatialDim eq 'HTI'&$format=json".replace(" ", "%20")
        url = f"{BASE}/{code}?{q}"
        try:
            resp = urllib.request.urlopen(url, timeout=15)
            data = json.loads(resp.read())
        except:
            continue

        for obs in data.get("value", []):
            val = obs.get("NumericValue")
            if val is None:
                continue
            yr = obs.get("TimeDim")
            if not yr:
                continue
            period_id = db.execute(
                "SELECT period_id FROM time_periods WHERE year=?",
                (int(yr),)
            ).fetchone()
            if not period_id:
                db.execute("INSERT OR IGNORE INTO time_periods (period_type, year) VALUES ('year', ?)", (int(yr),))
                period_id = db.execute(
                    "SELECT period_id FROM time_periods WHERE year=?",
                    (int(yr),)
                ).fetchone()
            pid = period_id[0]

            disag = obs.get("Dim1", "") or obs.get("Dim2", "") or obs.get("Dim3", "")
            if disag == "SEX_BTSX" or disag == "":
                disag = "both"

            db.execute("""INSERT OR IGNORE INTO social_institutional_data
                (location_id, period_id, domain, indicator, value, unit, disaggregation, source)
                VALUES (?,?,?,?,?,?,?,?)""",
                (loc_id, pid, "health", ind_name, val, unit, disag, "WHO GHO"))
            inserted += 1

    db.commit()
    print(f"  WHO GHO: {inserted} health indicator rows inserted")

if __name__ == "__main__":
    from config import DB_PATH
    db = sqlite3.connect(DB_PATH)
    fetch_who(db)
    db.close()
