def _lid(cur, code, admin2=None):
    if code == "HTI":
        return cur.execute(
            "SELECT location_id FROM locations WHERE location_code='HTI' AND admin_level=0"
        ).fetchone()[0]
    if admin2:
        r = cur.execute(
            "SELECT location_id FROM locations WHERE admin2_code=?", (admin2,)
        ).fetchone()
        if r: return r[0]
    return cur.execute(
        "SELECT location_id FROM locations WHERE admin1_code=? AND admin_level=1", (code,)
    ).fetchone()[0]

DEPARTMENTS = [
    (0, "HTI", "Haiti", None, 18.9712, -72.2852),
    (1, "HT01", "Artibonite", None, 19.3667, -72.6833),
    (1, "HT02", "Centre", None, 19.1500, -72.0167),
    (1, "HT03", "Grand'Anse", None, 18.4333, -74.0000),
    (1, "HT04", "Nippes", None, 18.4667, -73.4167),
    (1, "HT05", "Nord", None, 19.6000, -72.5500),
    (1, "HT06", "Nord-Est", None, 19.5000, -71.8500),
    (1, "HT07", "Nord-Ouest", None, 19.9000, -72.8000),
    (1, "HT08", "Ouest", None, 18.6667, -72.4167),
    (1, "HT09", "Sud", None, 18.2833, -73.7500),
    (1, "HT10", "Sud-Est", None, 18.2833, -72.5333),
]

ADMIN2 = [
    (2, "HT08", "HT0811", "La Gonave"),
    (2, "HT08", "HT0111", "Port-au-Prince"),
]

WATER_QUALITY = [
    ("HT02", "2022", "department_water_points", 9837, 75.0, None, None, "Wampler et al. 2022, Hydrogeology Journal 30, 1453-1467"),
    ("HT05", "2022", "department_water_points", 9837, 55.0, None, None, "Wampler et al. 2022"),
    ("HT08", "2022", "department_water_points", 9837, 12.0, None, None, "Wampler et al. 2022"),
    ("HTI", "2022", "kiosk_study", 3, None, 60.0, 47.0, "Drinking-water kiosks, Northern Haiti, 2022"),
    ("HTI", "2024", "rural_wells", None, 89.0, None, 89.0, "Rural Haiti hand-dug wells study, 2024"),
    ("HTI", "2008", "karst_springs", 25, None, None, None, "Verrettes area karst springs, 2008"),
]

FOREST_DATA = [
    ("HTI", 2020, "GFW", 910000, 33.0, None, None, None),
    ("HTI", 2025, "GFW", None, None, 2100, 980, None),
    ("HT03", 2020, "GFW", 130000, 70.0, 250, None, None),
    ("HT08", 2020, "GFW", 41000, 21.0, 120, None, None),
    ("HT08", 2020, "GFW", 12000, 18.0, 60, None, "HT0811"),
]

MINERAL_RESOURCES = [
    ("HT09", "bauxite", "Miragoane", "historic", "14 million+ tons exported", "USGS BME"),
    ("HT09", "bauxite", "Rochelois Plateau", "historic", "Known deposits", "USGS 1948, Aluminous lateritic soil of Haiti"),
    ("HT05", "copper", "Northern Haiti", "potential", "Favorable for prospecting", "Springer historical survey"),
    ("HT10", "gold_copper_lead_zinc", "Southern Haiti", "potential", "New prospective zones", "Academic surveys"),
    ("HTI", "manganese", "Various", "historic", "Investigated 1945", "USGS 1945 investigation"),
    ("HTI", "gold", "Various", "potential", "Undetermined", "Geological studies"),
    ("HTI", "cobalt", "Various", "potential", "Undetermined", "Geological studies"),
    ("HTI", "rare_earth", "Various", "potential", "Undetermined", "Geological studies"),
]

GEOTHERMAL_DATA = [
    ("HTI", "Los Posos", 37.1, None, None, None, None, "BME / OLADE 1977 / BRGM 1984"),
    ("HTI", "Sources Puantes", 35.0, None, None, None, None, "BME / OLADE 1977"),
    ("HTI", "Eaux de Boynes", 50.0, None, None, None, None, "BME"),
    ("HTI", "Anse d'Hainault", 40.0, None, None, None, None, "BME"),
    ("HTI", "Jeremie", 40.0, None, None, None, None, "BME"),
]

GEOLOGICAL_DATA = [
    ("HTI", "bedrock_map", None, None, "Greater Antilles", "Cretaceous-Tertiary", "1:200,000", "USGS Geologic Map of the Greater Antilles"),
    ("HTI", "mineral_assessment", "copper", "Porphyry Copper", None, None, None, "USGS Mineral Resource Assessment"),
    ("HTI", "soil_survey", "bauxite", "Aluminous lateritic soil", None, "Quaternary", None, "USGS 1948"),
]

ELEVATION_DATA = [
    ("HTI", "OpenTopography Haiti DTM", 1.5, "DTM", "https://opentopography.org", "10.5069/G9GX48R8", 29239, 2014, 2016),
    ("HTI", "GTOPO30", 1000.0, "DEM", "https://www.usgs.gov/centers/eros", None, None, None, None),
    ("HTI", "NOAA CUDEM", 10.0, "bathymetric-topographic", "https://coast.noaa.gov/digitalcoast", None, None, None, None),
]

SATELLITE_DATA = [
    ("HTI", "MODIS", "EVI", 250, "16-day", "2012-2024", "World Bank / FAO"),
    ("HTI", "Sentinel-2", "MSI", 10, "5-day", "2015-present", "Copernicus"),
    ("HTI", "GOES-19", "GeoColor", 500, "real-time", "2024-present", "NOAA"),
    ("HTI", "Landsat", "TM/ETM/OLI", 30, "16-day", "1972-present", "USGS"),
]

MACRO_DATA = [
    (2025, "GDP_growth", -2.7, "percent", "World Bank"),
    (2024, "GDP_growth", -4.18, "percent", "World Bank"),
    (2023, "GDP_growth", -1.86, "percent", "World Bank"),
    (2025, "inflation_avg", 28.3, "percent", "World Bank"),
    (2024, "inflation_avg", 26.95, "percent", "World Bank"),
    (2025, "gov_revenue_pct_gdp", 4.8, "percent", "World Bank"),
    (2025, "poverty_3usd_day", 49.0, "percent", "World Bank"),
    (2025, "gdp_per_capita_rank", 155, "rank_out_of_193", "OEC"),
    (2024, "gdp_per_capita_rank", 155, "rank_out_of_193", "OEC"),
    (2024, "total_gdp_usd", 25.2e9, "current_USD", "OEC"),
]

TRADE_DATA_STATIC = [
    (2024, "export", "Knit T-shirts", 339e6, "United States", "OEC"),
    (2024, "export", "Knit Sweaters", 119e6, "United States", "OEC"),
    (2024, "export", "Non-Knit Men's Suits", 49.4e6, "United States", "OEC"),
    (2024, "export", "Essential Oils", 46.4e6, "United States", "OEC"),
    (2024, "export", "Knit Women's Suits", 35.3e6, "United States", "OEC"),
    (2024, "export_summary", "Total Exports", 815e6, "World", "OEC"),
    (2024, "import", "Refined Petroleum", 500e6, "United States", "OEC"),
    (2024, "import", "Rice", 368e6, "United States", "OEC"),
    (2024, "import", "Raw Sugar", 133e6, "United States", "OEC"),
    (2024, "import", "Palm Oil", 124e6, "United States", "OEC"),
    (2024, "import", "Knit T-shirts", 103e6, "United States", "OEC"),
    (2024, "import_summary", "Total Imports", 3.41e9, "World", "OEC"),
    (2024, "export", "All Products", 637e6, "United States", "OEC"),
    (2024, "export", "All Products", 37.2e6, "Canada", "OEC"),
    (2024, "export", "All Products", 21.2e6, "Mexico", "OEC"),
    (2024, "export", "All Products", 20.8e6, "France", "OEC"),
    (2024, "export", "All Products", 14.5e6, "Dominican Republic", "OEC"),
    (2024, "import", "All Products", 1.13e9, "United States", "OEC"),
    (2024, "import", "All Products", 896e6, "Dominican Republic", "OEC"),
    (2024, "import", "All Products", 450e6, "China", "OEC"),
    (2024, "import", "All Products", 109e6, "Indonesia", "OEC"),
    (2024, "import", "All Products", 87.2e6, "India", "OEC"),
]

BILATERAL_TRADE = [
    (2024, "total", None, 909.5e6, None, None, "DGA"),
    (2024, "DR_to_HTI", "formal", 895.6e6, None, None, "DGA"),
    (2024, "HTI_to_DR", "formal", 13.9e6, None, None, "DGA"),
    (2017, "total", "formal+informal", 1.36e9, None, None, "CES"),
    (2017, "DR_to_HTI", "informal", 331.5e6, None, None, "CES"),
    (2017, "HTI_to_DR", "informal", 98.1e6, None, None, "CES"),
    (2026, "DR_to_HTI", "Regimen Nacional", None, 76.55, "Steel bars 15.2%, cement 11.1%, wheat flour 5.6%", "DGA_JanMay2026"),
    (2026, "DR_to_HTI", "Zonas Francas", None, 14.83, "T-shirts 30.7%, cotton fabrics 20.3%, plastic packaging 6.4%", "DGA_JanMay2026"),
    (2026, "HTI_to_DR", "Despacho a Consumo", None, 62.40, "Insecticides 61.1%, ethyl alcohol 20.4%, textile rags 5.4%", "DGA_JanMay2026"),
    (2026, "HTI_to_DR", "Zonas Francas", None, 37.60, "Textile rags/ropes 66.8%, knit blouses 14.3%, ethyl alcohol 7.4%", "DGA_JanMay2026"),
]

LOCAL_PRODUCTION = [
    (2023, "agriculture", "rice", "harvested_area_1000ha", 52, "1000 HA", "USDA"),
    (2024, "agriculture", "rice", "harvested_area_1000ha", 53, "1000 HA", "USDA"),
    (2023, "agriculture", "rice", "milled_production_1000mt", 52, "1000 MT", "USDA"),
    (2024, "agriculture", "rice", "milled_production_1000mt", 53, "1000 MT", "USDA"),
    (2024, "agriculture", "rice", "imports_1000mt", 475, "1000 MT", "USDA"),
    (2024, "agriculture", "rice", "consumption_1000mt", 530, "1000 MT", "USDA"),
    (2024, "agriculture", "all", "value_added_usd", 4.18e9, "current_USD", "UN"),
    (2023, "agriculture", "all", "value_added_usd", 3.47e9, "current_USD", "UN"),
    (2022, "manufacturing", "all", "value_added_gourdes", 257.5e9, "constant_2020_Gourdes", "UN"),
    (2023, "manufacturing", "all", "value_added_gourdes", 250.9e9, "constant_2020_Gourdes", "UN"),
    (2024, "manufacturing", "all", "value_added_gourdes", 240.8e9, "constant_2020_Gourdes", "UN"),
]

PLANS = [
    ("PSDH - Haiti emergent en 2030", "Government of Haiti", "2030", 2012, "Foundational national development", None, "Led by MPCE"),
    ("Medium-Term Recovery and Development Plan", "IDB (coordinating)", "2025-2030", 2025, "Recovery & private-sector growth", None, "3 pillars: economic recovery, basic services, institutions/security"),
    ("World Bank Group Country Partnership Framework", "World Bank", "2025-2029", 2025, "Resilience & governance", None, "~$320M in grants"),
    ("National Environmental Action Plan (PNAE)", "Ministry of Environment", "2025-2050", 2025, "Long-term environmental governance", None, "8 priority areas incl. climate adaptation, coastal management"),
    ("National Biodiversity Strategy and Action Plan", "Government of Haiti", "2020-2030", 2020, "Biodiversity conservation", None, "Published March 2020"),
    ("EU Strategy for Haiti", "European Union", "2021-2027", 2021, "Sustainable development & stability", None, "~261M EUR; Team Europe on TVET education"),
    ("UNSDCF", "United Nations", "2023-2027", 2023, "SDG alignment", None, "Aligns with PSDH 2030"),
    ("Vision 2050 Grand Nord", "Regional/Independent", "2050", None, "Regional economic development", None, "Public-private partnership concept"),
    ("Haiti 2050: A Vision for Sustainable Prosperity", "Independent", "2050", None, "Sustainable prosperity principles", None, "7 principles incl. SMEs, digital transformation"),
    ("National Adaptation Plan (PNA)", "Government of Haiti", "2022-2030", 2022, "Climate change adaptation", None, "Comprehensive climate adaptation strategy"),
]


def seed_locations(db):
    cur = db.cursor()
    for row in DEPARTMENTS:
        admin_level, code, name, parent_code, lat, lng = row
        cur.execute("""INSERT OR IGNORE INTO locations
            (location_code, admin_level, admin1_code, admin1_name, parent_location_id, latitude, longitude)
            VALUES (?, ?, ?, ?, (SELECT location_id FROM locations WHERE admin1_code=? AND admin_level=1), ?, ?)""",
            ("HTI", admin_level, code, name, parent_code, lat, lng))
    for row in ADMIN2:
        admin_level, admin1_code, admin2_code, admin2_name = row
        cur.execute("""INSERT OR IGNORE INTO locations
            (location_code, admin_level, admin1_code, admin1_name, admin2_code, admin2_name)
            VALUES (?, ?, ?, (SELECT admin1_name FROM locations WHERE admin1_code=? AND admin_level=1), ?, ?)""",
            ("HTI", admin_level, admin1_code, admin1_code, admin2_code, admin2_name))
    db.commit()
    print(f"  locations: seeded {len(DEPARTMENTS) + len(ADMIN2)} rows")


def seed_time_periods(db):
    cur = db.cursor()
    for year in range(2000, 2031):
        cur.execute("""INSERT OR IGNORE INTO time_periods
            (period_type, year, start_date, end_date)
            VALUES ('year', ?, ?, ?)""",
            (year, f"{year}-01-01", f"{year}-12-31"))
    db.commit()
    print(f"  time_periods: seeded 31 rows")


def seed_water_quality(db):
    cur = db.cursor()
    for (code, date, stype, pts, unsafe, tc, ecoli, cite) in WATER_QUALITY:
        cur.execute("""INSERT OR IGNORE INTO water_quality_data
            (location_id, sample_date, sample_type, water_point_count, unsafe_percent,
             total_coliform_positive_pct, e_coli_positive_pct, source_citation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (_lid(cur, code), date, stype, pts, unsafe, tc, ecoli, cite))
    db.commit()
    print(f"  water_quality_data: seeded {len(WATER_QUALITY)} rows")


def seed_forest(db):
    cur = db.cursor()
    for row in FOREST_DATA:
        code, year, src, nf, tc, loss, co2 = row[:7]
        admin2 = row[7] if len(row) > 7 else None
        cur.execute("""INSERT OR IGNORE INTO forest_data
            (location_id, year, source, natural_forest_ha, tree_cover_percent, forest_loss_ha, co2_emissions_kt)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (_lid(cur, code, admin2), year, src, nf, tc, loss, co2))
    db.commit()
    print(f"  forest_data: seeded {len(FOREST_DATA)} rows")


def seed_minerals(db):
    cur = db.cursor()
    for (code, mtype, dname, status, reserve, cite) in MINERAL_RESOURCES:
        cur.execute("""INSERT OR IGNORE INTO mineral_resources
            (location_id, mineral_type, deposit_name, status, estimated_reserve, source_citation)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (_lid(cur, code), mtype, dname, status, reserve, cite))
    db.commit()
    print(f"  mineral_resources: seeded {len(MINERAL_RESOURCES)} rows")


def seed_geothermal(db):
    cur = db.cursor()
    for (code, name, temp, flow, funit, minz, ph, cite) in GEOTHERMAL_DATA:
        cur.execute("""INSERT OR IGNORE INTO geothermal_data
            (location_id, spring_name, temperature_c, flow_rate, flow_unit, mineralization, ph, source_citation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (_lid(cur, code), name, temp, flow, funit, minz, ph, cite))
    db.commit()
    print(f"  geothermal_data: seeded {len(GEOTHERMAL_DATA)} rows")


def seed_geological(db):
    cur = db.cursor()
    for (code, dtype, mtype, dname, fname, era, scale, cite) in GEOLOGICAL_DATA:
        cur.execute("""INSERT OR IGNORE INTO geological_data
            (location_id, data_type, mineral_type, deposit_name, formation_name, era, scale, source_citation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (_lid(cur, code), dtype, mtype, dname, fname, era, scale, cite))
    db.commit()
    print(f"  geological_data: seeded {len(GEOLOGICAL_DATA)} rows")


def seed_elevation(db):
    cur = db.cursor()
    for (code, dsn, res, dt, url, doi, area, ys, ye) in ELEVATION_DATA:
        cur.execute("""INSERT OR IGNORE INTO elevation_data
            (location_id, dataset_name, resolution_m, data_type, source_url, doi, coverage_area_km2, year_start, year_end)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (_lid(cur, code), dsn, res, dt, url, doi, area, ys, ye))
    db.commit()
    print(f"  elevation_data: seeded {len(ELEVATION_DATA)} rows")


def seed_satellite(db):
    cur = db.cursor()
    for (code, sensor, ptype, res, tres, acquired, url) in SATELLITE_DATA:
        cur.execute("""INSERT OR IGNORE INTO satellite_imagery
            (location_id, sensor, product_type, resolution_m, temporal_resolution, date_acquired, source_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (_lid(cur, code), sensor, ptype, res, tres, acquired, url))
    db.commit()
    print(f"  satellite_imagery: seeded {len(SATELLITE_DATA)} rows")


def seed_macro(db):
    cur = db.cursor()
    for (year, code, val, unit, src) in MACRO_DATA:
        pid = cur.execute("SELECT period_id FROM time_periods WHERE year=? AND period_type='year'", (year,)).fetchone()
        if not pid: continue
        cur.execute("""INSERT OR IGNORE INTO macroeconomic_data
            (period_id, indicator_code, indicator_name, value, unit, source)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (pid[0], code, code, val, unit, src))
    db.commit()
    print(f"  macroeconomic_data: seeded {len(MACRO_DATA)} rows")


def seed_trade(db):
    cur = db.cursor()
    for (year, flow, product, val, partner, src) in TRADE_DATA_STATIC:
        pid = cur.execute("SELECT period_id FROM time_periods WHERE year=? AND period_type='year'", (year,)).fetchone()
        if not pid: continue
        cur.execute("""INSERT OR IGNORE INTO trade_data
            (period_id, trade_flow, product_name, value_usd, partner_country, source)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (pid[0], flow, product, val, partner, src))
    db.commit()
    print(f"  trade_data: seeded {len(TRADE_DATA_STATIC)} rows")


def seed_bilateral(db):
    cur = db.cursor()
    for (year, direction, regime, val, growth, products, src) in BILATERAL_TRADE:
        pid = cur.execute("SELECT period_id FROM time_periods WHERE year=? AND period_type='year'", (year,)).fetchone()
        if not pid: continue
        cur.execute("""INSERT OR IGNORE INTO bilateral_trade_dr
            (period_id, trade_direction, regime, value_usd, growth_pct, top_products, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (pid[0], direction, regime, val, growth, products, src))
    db.commit()
    print(f"  bilateral_trade_dr: seeded {len(BILATERAL_TRADE)} rows")


def seed_production(db):
    cur = db.cursor()
    for (year, sector, sub, ind, val, unit, src) in LOCAL_PRODUCTION:
        pid = cur.execute("SELECT period_id FROM time_periods WHERE year=? AND period_type='year'", (year,)).fetchone()
        if not pid: continue
        cur.execute("""INSERT OR IGNORE INTO local_production
            (period_id, sector, subsector, indicator, value, unit, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (pid[0], sector, sub, ind, val, unit, src))
    db.commit()
    print(f"  local_production: seeded {len(LOCAL_PRODUCTION)} rows")


def seed_plans(db):
    cur = db.cursor()
    for (name, org, tf, year, theme, url, notes) in PLANS:
        cur.execute("""INSERT OR IGNORE INTO plan_registry
            (plan_name, lead_org, timeframe, year_published, key_theme, source_url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name, org, tf, year, theme, url, notes))
    db.commit()
    print(f"  plan_registry: seeded {len(PLANS)} rows")


def seed_all(db):
    seed_locations(db)
    seed_time_periods(db)
    seed_water_quality(db)
    seed_forest(db)
    seed_minerals(db)
    seed_geothermal(db)
    seed_geological(db)
    seed_elevation(db)
    seed_satellite(db)
    seed_macro(db)
    seed_trade(db)
    seed_bilateral(db)
    seed_production(db)
    seed_plans(db)
