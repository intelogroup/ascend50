#!/usr/bin/env python3
import sqlite3
from config import DB_PATH


def run_query(db, title, sql):
    rows = db.execute(sql).fetchall()
    print(f"\n=== {title} ({len(rows)} rows) ===")
    for r in rows[:20]:
        print(f"  {r}")
    if len(rows) > 20:
        print(f"  ... and {len(rows) - 20} more")


def main():
    db = sqlite3.connect(str(DB_PATH))
    db.execute("PRAGMA foreign_keys = ON")

    run_query(db, "Departments", """
        SELECT admin1_code, admin1_name FROM locations
        WHERE admin_level=1 ORDER BY admin1_code
    """)

    run_query(db, "Water Quality by Dept", """
        SELECT l.admin1_name, w.sample_type, w.unsafe_percent
        FROM water_quality_data w
        JOIN locations l ON w.location_id = l.location_id
        WHERE w.unsafe_percent IS NOT NULL
        ORDER BY w.unsafe_percent DESC
    """)

    run_query(db, "Recent GDP", """
        SELECT tp.year, e.value
        FROM economic_data e
        JOIN time_periods tp ON e.period_id = tp.period_id
        WHERE e.indicator_code='NY.GDP.MKTP.KD.ZG'
        ORDER BY tp.year DESC LIMIT 5
    """)

    run_query(db, "Forest Cover National", """
        SELECT year, natural_forest_ha, tree_cover_percent, forest_loss_ha
        FROM forest_data
        WHERE location_id=1 ORDER BY year DESC
    """)

    run_query(db, "Strategic Plans Timeline", """
        SELECT plan_name, lead_org, timeframe, year_published
        FROM plan_registry ORDER BY year_published
    """)

    run_query(db, "Mineral Resources", """
        SELECT mineral_type, deposit_name, status, estimated_reserve
        FROM mineral_resources ORDER BY status, mineral_type
    """)

    run_query(db, "Geothermal Springs", """
        SELECT spring_name, temperature_c, source_citation
        FROM geothermal_data ORDER BY temperature_c DESC
    """)

    run_query(db, "Haiti-DR Trade Balance", """
        SELECT tp.year, trade_direction, regime, value_usd
        FROM bilateral_trade_dr b
        JOIN time_periods tp ON b.period_id = tp.period_id
        ORDER BY tp.year DESC, trade_direction
    """)

    run_query(db, "Elevation / DEM Datasets", """
        SELECT dataset_name, resolution_m, data_type, doi
        FROM elevation_data ORDER BY resolution_m
    """)

    run_query(db, "Macroeconomic Snapshot", """
        SELECT tp.year, indicator_code, value, unit, source
        FROM macroeconomic_data m
        JOIN time_periods tp ON m.period_id = tp.period_id
        ORDER BY tp.year DESC, indicator_code
    """)

    run_query(db, "Population by Dept (HDX)", """
        SELECT l.admin1_name, SUM(pd.total_population) AS pop,
               pd.age_range_code
        FROM population_data pd
        JOIN locations l ON pd.location_id = l.location_id
        GROUP BY l.admin1_name, pd.age_range_code
        ORDER BY l.admin1_name, pd.age_range_code
    """)

    run_query(db, "Food Security IPC (HDX)", """
        SELECT l.admin1_name, fs.ipc_phase, fs.ipc_phase_name,
               SUM(fs.population_in_phase) AS pop,
               ROUND(AVG(fs.percent_population) * 100, 1) AS avg_pct
        FROM food_security_data fs
        JOIN locations l ON fs.location_id = l.location_id
        GROUP BY l.admin1_name, fs.ipc_phase, fs.ipc_phase_name
        ORDER BY l.admin1_name, fs.ipc_phase
    """)

    run_query(db, "Humanitarian Coverage (HDX)", """
        SELECT indicator_type, COUNT(*) AS records,
               SUM(indicator_value) AS total_people_affected
        FROM health_humanitarian_data
        WHERE indicator_value IS NOT NULL
        GROUP BY indicator_type ORDER BY indicator_type
    """)

    run_query(db, "Rainfall Hazards (HDX)", """
        SELECT l.admin1_name, hz.severity, tp.year
        FROM hazards_data hz
        JOIN locations l ON hz.location_id = l.location_id
        JOIN time_periods tp ON hz.period_id = tp.period_id
        ORDER BY tp.year DESC LIMIT 10
    """)

    run_query(db, "Conflict Events (HDX)", """
        SELECT l.admin1_name, l.admin2_name, hz.severity,
               hz.affected_population AS events, tp.year
        FROM hazards_data hz
        JOIN locations l ON hz.location_id = l.location_id
        JOIN time_periods tp ON hz.period_id = tp.period_id
        WHERE hz.hazard_type='conflict'
        ORDER BY tp.year DESC LIMIT 10
    """)

    run_query(db, "Poverty Rate by Dept (HDX)", """
        SELECT l.admin1_name, ROUND(hh.indicator_value, 1) AS headcount_pct,
               hh.disaggregation, tp.year
        FROM health_humanitarian_data hh
        JOIN locations l ON hh.location_id = l.location_id
        JOIN time_periods tp ON hh.period_id = tp.period_id
        WHERE hh.indicator_type='poverty_rate'
        ORDER BY tp.year DESC, l.admin1_name
    """)

    run_query(db, "Electricity Access", """
        SELECT tp.year, access_rate_pct, rural_access_pct,
               population_without_access, grid_status, source
        FROM electricity_access ea
        JOIN time_periods tp ON ea.period_id = tp.period_id
        WHERE ea.location_id=1
        ORDER BY tp.year DESC
    """)

    run_query(db, "Energy Production & Consumption", """
        SELECT tp.year, energy_type, metric, value, unit, source
        FROM energy_production_consumption ep
        JOIN time_periods tp ON ep.period_id = tp.period_id
        ORDER BY tp.year DESC, energy_type, metric
    """)

    run_query(db, "Renewable Energy Potential", """
        SELECT resource_type, exploited_capacity_mw,
               unexploited_potential_mw, notes, source
        FROM renewable_potential
        WHERE location_id=1
        ORDER BY resource_type
    """)

    run_query(db, "Social & Institutional (by domain)", """
        SELECT sid.domain, sid.indicator, sid.value, sid.unit,
               sid.source, tp.year
        FROM social_institutional_data sid
        JOIN time_periods tp ON sid.period_id = tp.period_id
        ORDER BY sid.domain, sid.indicator, tp.year DESC
    """)

    run_query(db, "NDC 2030 Targets", """
        SELECT resource_type, metric_value, metric_unit, notes
        FROM renewable_potential
        WHERE metric_name='ndc_target_pct' AND location_id=1
        ORDER BY resource_type
    """)

    run_query(db, "Humanitarian Funding (HDX)", """
        SELECT tp.year, ROUND(SUM(hh.indicator_value)) AS total_funding_usd,
               hh.disaggregation
        FROM health_humanitarian_data hh
        JOIN time_periods tp ON hh.period_id = tp.period_id
        WHERE hh.indicator_type='funding'
        GROUP BY tp.year ORDER BY tp.year DESC LIMIT 10
    """)

    db.close()


if __name__ == "__main__":
    main()
