import requests
from config import HDX_BASE, HDX_APP_ID

SRC = "HDX HAPI"


def _lid(cur, admin1, admin2):
    if admin2:
        r = cur.execute(
            "SELECT location_id FROM locations WHERE admin2_code=?", (admin2,)
        ).fetchone()
        if r: return r[0]
    if admin1 and admin1 != "HTI":
        r = cur.execute(
            "SELECT location_id FROM locations WHERE admin1_code=? AND admin_level=1", (admin1,)
        ).fetchone()
        if r: return r[0]
    r = cur.execute(
        "SELECT location_id FROM locations WHERE location_code='HTI' AND admin_level=0"
    ).fetchone()
    return r[0] if r else None


def _pid(cur, year):
    r = cur.execute(
        "SELECT period_id FROM time_periods WHERE year=? AND period_type='year'", (year,)
    ).fetchone()
    return r[0] if r else None


def fetch_hdx(db):
    print("\n--- HDX HAPI ---")
    if not HDX_APP_ID:
        print("  SKIP: set HDX_APP_IDENTIFIER in .env or environment")
        return
    headers = {"X-HDX-HAPI-APP-IDENTIFIER": HDX_APP_ID}
    cur = db.cursor()

    def fetch_all(endpoint, extra=None, limit=500):
        params = {"location_code": "HTI", "output_format": "json", "limit": 500}
        if extra: params.update(extra)
        rows, offset = [], 0
        while True:
            params["offset"] = offset
            try:
                resp = requests.get(f"{HDX_BASE}/{endpoint}", headers=headers, params=params, timeout=60)
                if resp.status_code == 403: return None
                resp.raise_for_status()
                data = resp.json().get("data", [])
            except Exception as e:
                print(f"  FAIL {endpoint}: {e}"); return None
            if not data: break
            rows.extend(data); offset += len(data)
            if len(rows) >= limit: break
        return rows

    rows = fetch_all("geography-infrastructure/baseline-population")
    if rows is not None:
        n = 0
        for r in rows:
            lid = _lid(cur, r.get("admin1_code"), r.get("admin2_code"))
            pid = _pid(cur, int(r["reference_period_start"][:4]))
            if lid is None or pid is None: continue
            cur.execute(
                "INSERT OR IGNORE INTO population_data "
                "(location_id,period_id,source,total_population,age_range_code,age_range_min,age_range_max) "
                "VALUES (?,?,?,?,?,?,?)",
                (lid, pid, SRC, r["population"], r.get("age_range"), r.get("min_age"), r.get("max_age")),
            )
            n += cur.rowcount
        print(f"  baseline pop: {len(rows)} fetched, {n} inserted")

    rows = fetch_all("food-security-nutrition-poverty/food-security")
    if rows is not None:
        n = 0
        for r in rows:
            lid = _lid(cur, r.get("admin1_code"), r.get("admin2_code"))
            pid = _pid(cur, int(r["reference_period_start"][:4]))
            if lid is None or pid is None: continue
            cur.execute(
                "INSERT OR IGNORE INTO food_security_data "
                "(location_id,period_id,source,ipc_phase,ipc_phase_name,population_in_phase,percent_population) "
                "VALUES (?,?,?,?,?,?,?)",
                (lid, pid, SRC, r["ipc_phase"], r.get("ipc_type"),
                 r.get("population_in_phase"), r.get("population_fraction_in_phase")),
            )
            n += cur.rowcount
        print(f"  food security: {len(rows)} fetched, {n} inserted")

    rows = fetch_all("affected-people/refugees-persons-of-concern")
    if rows is not None:
        n = 0
        for r in rows:
            lid = _lid(cur, "HTI", None)
            pid = _pid(cur, int(r["reference_period_start"][:4]))
            if lid is None or pid is None: continue
            disag = f"group={r.get('population_group','')} gender={r.get('gender','')} age={r.get('age_range','')}"
            cur.execute(
                "INSERT OR IGNORE INTO health_humanitarian_data "
                "(location_id,period_id,source,indicator_type,indicator_value,disaggregation) "
                "VALUES (?,?,?,?,?,?)",
                (lid, pid, SRC, "refugees", r.get("population"), disag),
            )
            n += cur.rowcount
        print(f"  refugees: {len(rows)} fetched, {n} inserted")

    rows = fetch_all("affected-people/humanitarian-needs")
    if rows is not None:
        n = 0
        for r in rows:
            lid = _lid(cur, r.get("admin1_code"), r.get("admin2_code"))
            pid = _pid(cur, int(r["reference_period_start"][:4]))
            if lid is None or pid is None: continue
            disag = f"{r.get('sector_code','')} {r.get('category','')} {r.get('population_status','')}"
            cur.execute(
                "INSERT OR IGNORE INTO health_humanitarian_data "
                "(location_id,period_id,source,indicator_type,indicator_value,disaggregation) "
                "VALUES (?,?,?,?,?,?)",
                (lid, pid, SRC, "humanitarian_needs", r.get("population"), disag),
            )
            n += cur.rowcount
        print(f"  humanitarian needs: {len(rows)} fetched, {n} inserted")

    rows = fetch_all("climate/rainfall")
    if rows is not None:
        n = 0
        for r in rows:
            lid = _lid(cur, r.get("admin1_code"), r.get("admin2_code"))
            pid = _pid(cur, int(r["reference_period_start"][:4]))
            if lid is None or pid is None: continue
            severity = f"rainfall={r.get('rainfall')} anomaly={r.get('rainfall_anomaly_pct','')}pct"
            cur.execute(
                "INSERT OR IGNORE INTO hazards_data "
                "(location_id,period_id,hazard_type,severity,source) "
                "VALUES (?,?,?,?,?)",
                (lid, pid, "rainfall", severity, SRC),
            )
            n += cur.rowcount
        print(f"  rainfall: {len(rows)} fetched, {n} inserted")

    rows = fetch_all("coordination-context/operational-presence")
    if rows is not None:
        n = 0
        for r in rows:
            lid = _lid(cur, r.get("admin1_code"), r.get("admin2_code"))
            pid = _pid(cur, int(r["reference_period_start"][:4]))
            if lid is None or pid is None: continue
            disag = f"sector={r.get('sector_code','')} org={r.get('org_name','')}"
            cur.execute(
                "INSERT OR IGNORE INTO health_humanitarian_data "
                "(location_id,period_id,source,indicator_type,indicator_value,disaggregation) "
                "VALUES (?,?,?,?,?,?)",
                (lid, pid, SRC, "operational_presence", None, disag),
            )
            n += cur.rowcount
        print(f"  operational presence: {len(rows)} fetched, {n} inserted")

    rows = fetch_all("food-security-nutrition-poverty/poverty-rate")
    if rows is not None:
        n = 0
        for r in rows:
            lid = _lid(cur, r.get("admin1_code"), None)
            pid = _pid(cur, int(r["reference_period_start"][:4]))
            if lid is None or pid is None: continue
            disag = f"mpi={r.get('mpi')} intensity={r.get('intensity_of_deprivation')} vulnerable={r.get('vulnerable_to_poverty')} severe={r.get('in_severe_poverty')}"
            cur.execute(
                "INSERT OR IGNORE INTO health_humanitarian_data "
                "(location_id,period_id,source,indicator_type,indicator_value,disaggregation) "
                "VALUES (?,?,?,?,?,?)",
                (lid, pid, SRC, "poverty_rate", r.get("headcount_ratio"), disag),
            )
            n += cur.rowcount
        print(f"  poverty-rate: {len(rows)} fetched, {n} inserted")

    rows = fetch_all("coordination-context/conflict-events")
    if rows is not None:
        n = 0
        for r in rows:
            lid = _lid(cur, r.get("admin1_code"), r.get("admin2_code"))
            pid = _pid(cur, int(r["reference_period_start"][:4]))
            if lid is None or pid is None: continue
            severity = f"{r.get('event_type')} fatalities={r.get('fatalities')}"
            cur.execute(
                "INSERT OR IGNORE INTO hazards_data "
                "(location_id,period_id,hazard_type,severity,affected_population,source) "
                "VALUES (?,?,?,?,?,?)",
                (lid, pid, "conflict", severity, r.get("events"), SRC),
            )
            n += cur.rowcount
        print(f"  conflict-events: {len(rows)} fetched, {n} inserted")

    rows = fetch_all("coordination-context/funding")
    if rows is not None:
        n = 0
        for r in rows:
            lid = _lid(cur, "HTI", None)
            pid = _pid(cur, int(r["reference_period_start"][:4]))
            if lid is None or pid is None: continue
            disag = f"appeal={r.get('appeal_code','')} requirements={r.get('requirements_usd')} funding_pct={r.get('funding_pct')}"
            cur.execute(
                "INSERT OR IGNORE INTO health_humanitarian_data "
                "(location_id,period_id,source,indicator_type,indicator_value,disaggregation) "
                "VALUES (?,?,?,?,?,?)",
                (lid, pid, SRC, "funding", r.get("funding_usd"), disag),
            )
            n += cur.rowcount
        print(f"  funding: {len(rows)} fetched, {n} inserted")

    db.commit()
    n_total = sum([
        cur.execute("SELECT COUNT(*) FROM population_data").fetchone()[0],
        cur.execute("SELECT COUNT(*) FROM food_security_data").fetchone()[0],
        cur.execute("SELECT COUNT(*) FROM health_humanitarian_data").fetchone()[0],
        cur.execute("SELECT COUNT(*) FROM hazards_data").fetchone()[0],
    ])
    print(f"  HDX total: {n_total} rows in HDX tables")
