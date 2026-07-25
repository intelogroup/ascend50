#!/usr/bin/env python3
import sqlite3, html
from config import DB_PATH

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Haiti Data Hub Report</title>
<style>
body{{font:14px/1.5 system-ui,sans-serif;max-width:960px;margin:auto;padding:20px;color:#222;background:#f8f9fa}}
h1{{font-size:24px}} h2{{font-size:18px;border-bottom:2px solid #ddd;padding-bottom:4px;margin-top:28px}}
table{{border-collapse:collapse;width:100%;margin:8px 0 16px;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
th{{background:#eee;text-align:left;padding:6px 8px;font-weight:600;font-size:13px}}
td{{padding:4px 8px;border-top:1px solid #eee;font-size:13px;vertical-align:top}}
.overview td{{border:none}}
.bar{{display:inline-block;height:12px;background:#4a7;border-radius:2px;min-width:2px}}
.summary{{color:#666;font-size:13px;margin-bottom:20px}}
</style></head>
<body>
<h1>Haiti Data Hub &mdash; Report</h1>
<p class=summary>Generated: {date} &middot; {total_rows} rows across {n_tables} tables &middot; DB: {db_size} KB</p>
{content}
</body></html>"""


def section(title, cols, cursor):
    rows = cursor.fetchall()
    if not rows:
        return f"<h2>{html.escape(title)}</h2><p>(no data)</p>\n"
    h = f"<h2>{html.escape(title)} <span style=font-weight:400;font-size:13px;color:#888>({len(rows)} rows)</span></h2>\n<table><tr>"
    for c in cols:
        h += f"<th>{html.escape(c)}</th>"
    h += "</tr>\n"
    for r in rows:
        h += "<tr>" + "".join(f"<td>{html.escape(str(c)) if c is not None else ''}</td>" for c in r) + "</tr>\n"
    h += "</table>\n"
    return h


def bar_chart(title, labels, values, max_w=300):
    if not values:
        return ""
    mx = max(abs(v) for v in values if v is not None) or 1
    h = f"<h3>{html.escape(title)}</h3><div style=font-size:13px>\n"
    for lbl, val in zip(labels, values):
        v = val or 0
        w = max(int(abs(v) / mx * max_w), 2)
        color = "#c44" if v < 0 else "#4a7"
        h += f"<div style=margin:2px 0><span style=display:inline-block;width:120px>{html.escape(str(lbl))}</span>"
        h += f"<span class=bar style=width:{w}px;background:{color}></span> {v}</div>\n"
    h += "</div>\n"
    return h


def main():
    db = sqlite3.connect(str(DB_PATH))
    content = ""

    tables = [
        "locations","time_periods","population_data","food_security_data",
        "water_quality_data","health_humanitarian_data","economic_data",
        "hazards_data","forest_data","mineral_resources","geothermal_data",
        "geological_data","elevation_data","satellite_imagery",
        "macroeconomic_data","trade_data","bilateral_trade_dr",
        "local_production","plan_registry",
    ]
    total_rows = 0
    trows = []
    for t in tables:
        n = db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        total_rows += n
        trows.append((t, n))
    db_size = DB_PATH.stat().st_size // 1024

    content += "<table class=overview><tr><th>Table</th><th>Rows</th></tr>\n"
    for t, n in trows:
        content += f"<tr><td>{t}</td><td>{n}</td></tr>\n"
    content += "</table>\n"

    content += section("Departments", ["Code","Name"], db.execute("SELECT admin1_code,admin1_name FROM locations WHERE admin_level=1 ORDER BY admin1_code"))

    content += section("Recent GDP Growth", ["Year","GDP Growth %"], db.execute("SELECT tp.year,ROUND(e.value,2) FROM economic_data e JOIN time_periods tp ON e.period_id=tp.period_id WHERE e.indicator_code='NY.GDP.MKTP.KD.ZG' ORDER BY tp.year DESC LIMIT 10"))

    gdp_rows = db.execute("SELECT tp.year,ROUND(e.value,2) FROM economic_data e JOIN time_periods tp ON e.period_id=tp.period_id WHERE e.indicator_code='NY.GDP.MKTP.KD.ZG' ORDER BY tp.year").fetchall()
    if gdp_rows:
        content += bar_chart("GDP Growth Trend", [str(r[0]) for r in gdp_rows], [r[1] for r in gdp_rows])

    content += section("Population by Dept", ["Dept","Population","Age Range"], db.execute("SELECT l.admin1_name,SUM(pd.total_population),pd.age_range_code FROM population_data pd JOIN locations l ON pd.location_id=l.location_id GROUP BY l.admin1_name,pd.age_range_code ORDER BY l.admin1_name,pd.age_range_code"))

    content += section("Food Security (IPC Phase 1)", ["Dept","Pop in Phase 1","Pct"], db.execute("SELECT l.admin1_name,SUM(fs.population_in_phase),ROUND(AVG(fs.percent_population)*100,1) FROM food_security_data fs JOIN locations l ON fs.location_id=l.location_id WHERE fs.ipc_phase=1 AND fs.ipc_phase_name='current' GROUP BY l.admin1_name ORDER BY 3 DESC"))

    content += section("Conflict Events", ["Dept","Admin2","Severity","Events","Year"], db.execute("SELECT l.admin1_name,l.admin2_name,hz.severity,hz.affected_population,tp.year FROM hazards_data hz JOIN locations l ON hz.location_id=l.location_id JOIN time_periods tp ON hz.period_id=tp.period_id WHERE hz.hazard_type='conflict' ORDER BY tp.year DESC LIMIT 20"))

    content += section("Poverty Headcount (%)", ["Dept","2012","2016"], db.execute("""
        SELECT l.admin1_name,
            ROUND(MAX(CASE WHEN tp.year=2012 THEN hh.indicator_value END),1),
            ROUND(MAX(CASE WHEN tp.year=2016 THEN hh.indicator_value END),1)
        FROM health_humanitarian_data hh
        JOIN locations l ON hh.location_id=l.location_id
        JOIN time_periods tp ON hh.period_id=tp.period_id
        WHERE hh.indicator_type='poverty_rate'
        GROUP BY l.admin1_name ORDER BY l.admin1_name
    """))

    content += section("Humanitarian Funding", ["Year","Funding USD","Details"], db.execute("""
        SELECT tp.year,ROUND(SUM(hh.indicator_value)) AS usd,
            hh.disaggregation
        FROM health_humanitarian_data hh
        JOIN time_periods tp ON hh.period_id=tp.period_id
        WHERE hh.indicator_type='funding'
        GROUP BY tp.year ORDER BY tp.year DESC LIMIT 10
    """))

    content += section("Strategic Plans", ["Plan","Lead","Timeframe","Year"], db.execute("SELECT plan_name,lead_org,timeframe,year_published FROM plan_registry ORDER BY year_published"))

    d = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
    html_out = TEMPLATE.format(date=d, total_rows=total_rows, n_tables=len(tables), db_size=db_size, content=content)

    out = DB_PATH.parent / "report.html"
    out.write_text(html_out, encoding="utf-8")
    print(f"Report: {out} ({len(html_out)} bytes)")
    db.close()


if __name__ == "__main__":
    main()
