SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_code TEXT NOT NULL DEFAULT 'HTI',
    admin_level INTEGER NOT NULL,
    admin1_name TEXT,
    admin1_code TEXT,
    admin2_name TEXT,
    admin2_code TEXT,
    parent_location_id INTEGER REFERENCES locations(location_id),
    latitude REAL,
    longitude REAL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_locations_uniq ON locations(
    location_code, admin_level,
    COALESCE(admin1_code,''), COALESCE(admin2_code,'')
);

CREATE TABLE IF NOT EXISTS time_periods (
    period_id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_type TEXT NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    start_date TEXT,
    end_date TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_time_uniq ON time_periods(
    period_type, COALESCE(year,0), COALESCE(quarter,0), COALESCE(month,0)
);

CREATE TABLE IF NOT EXISTS population_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    period_id INTEGER REFERENCES time_periods(period_id),
    source TEXT NOT NULL,
    total_population REAL,
    male_population REAL,
    female_population REAL,
    age_range_code TEXT,
    age_range_min INTEGER,
    age_range_max INTEGER,
    data_quality TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_pop_uniq ON population_data(
    location_id, period_id, source, COALESCE(age_range_code,'')
);

CREATE TABLE IF NOT EXISTS food_security_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    period_id INTEGER REFERENCES time_periods(period_id),
    source TEXT NOT NULL,
    ipc_phase INTEGER,
    ipc_phase_name TEXT,
    population_in_phase REAL,
    percent_population REAL,
    data_quality TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_food_uniq ON food_security_data(
    location_id, period_id, source
);

CREATE TABLE IF NOT EXISTS water_quality_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    sample_date TEXT,
    sample_type TEXT NOT NULL,
    water_point_count INTEGER,
    unsafe_percent REAL,
    total_coliform_positive_pct REAL,
    e_coli_positive_pct REAL,
    source_citation TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_water_uniq ON water_quality_data(
    location_id, COALESCE(sample_date,''), sample_type
);

CREATE TABLE IF NOT EXISTS health_humanitarian_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    period_id INTEGER REFERENCES time_periods(period_id),
    source TEXT NOT NULL,
    indicator_type TEXT NOT NULL,
    indicator_value REAL,
    unit TEXT,
    disaggregation TEXT,
    data_quality TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_health_uniq ON health_humanitarian_data(
    location_id, period_id, source, indicator_type
);

CREATE TABLE IF NOT EXISTS economic_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    period_id INTEGER REFERENCES time_periods(period_id),
    indicator_code TEXT NOT NULL,
    indicator_name TEXT,
    value REAL,
    unit TEXT,
    source TEXT DEFAULT 'WorldBank'
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_econ_uniq ON economic_data(
    location_id, period_id, indicator_code
);

CREATE TABLE IF NOT EXISTS hazards_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    period_id INTEGER REFERENCES time_periods(period_id),
    hazard_type TEXT NOT NULL,
    severity TEXT,
    affected_population REAL,
    source TEXT,
    data_quality TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_hazards_uniq ON hazards_data(
    location_id, period_id, hazard_type
);

CREATE TABLE IF NOT EXISTS forest_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    year INTEGER NOT NULL,
    source TEXT NOT NULL,
    natural_forest_ha REAL,
    tree_cover_percent REAL,
    forest_loss_ha REAL,
    co2_emissions_kt REAL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_forest_uniq ON forest_data(
    location_id, year, source
);

CREATE TABLE IF NOT EXISTS mineral_resources (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    mineral_type TEXT NOT NULL,
    deposit_name TEXT,
    status TEXT,
    estimated_reserve TEXT,
    source_citation TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_mineral_uniq ON mineral_resources(
    location_id, mineral_type, COALESCE(deposit_name,'')
);

CREATE TABLE IF NOT EXISTS geothermal_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    spring_name TEXT,
    temperature_c REAL,
    flow_rate REAL,
    flow_unit TEXT,
    mineralization REAL,
    ph REAL,
    source_citation TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_geo_uniq ON geothermal_data(
    COALESCE(spring_name,''), location_id
);

CREATE TABLE IF NOT EXISTS geological_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    data_type TEXT NOT NULL,
    mineral_type TEXT,
    deposit_name TEXT,
    formation_name TEXT,
    era TEXT,
    scale TEXT,
    source_citation TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_geol_uniq ON geological_data(
    location_id, data_type, COALESCE(mineral_type,''), COALESCE(deposit_name,'')
);

CREATE TABLE IF NOT EXISTS elevation_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    dataset_name TEXT,
    resolution_m REAL,
    data_type TEXT,
    source_url TEXT,
    doi TEXT,
    coverage_area_km2 REAL,
    year_start INTEGER,
    year_end INTEGER
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_elev_uniq ON elevation_data(
    dataset_name, location_id
);

CREATE TABLE IF NOT EXISTS satellite_imagery (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER REFERENCES locations(location_id),
    sensor TEXT,
    product_type TEXT,
    resolution_m REAL,
    temporal_resolution TEXT,
    date_acquired TEXT,
    source_url TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_sat_uniq ON satellite_imagery(
    sensor, product_type, COALESCE(date_acquired,''), location_id
);

CREATE TABLE IF NOT EXISTS macroeconomic_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_id INTEGER REFERENCES time_periods(period_id),
    indicator_code TEXT NOT NULL,
    indicator_name TEXT,
    value REAL,
    unit TEXT,
    source TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_macro_uniq ON macroeconomic_data(
    period_id, indicator_code, source
);

CREATE TABLE IF NOT EXISTS trade_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_id INTEGER REFERENCES time_periods(period_id),
    trade_flow TEXT NOT NULL,
    product_name TEXT,
    value_usd REAL,
    partner_country TEXT,
    source TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_trade_uniq ON trade_data(
    period_id, trade_flow, COALESCE(product_name,''), COALESCE(partner_country,''), source
);

CREATE TABLE IF NOT EXISTS bilateral_trade_dr (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_id INTEGER REFERENCES time_periods(period_id),
    trade_direction TEXT NOT NULL,
    regime TEXT,
    value_usd REAL,
    growth_pct REAL,
    top_products TEXT,
    source TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_bilateral_uniq ON bilateral_trade_dr(
    period_id, trade_direction, COALESCE(regime,''), source
);

CREATE TABLE IF NOT EXISTS local_production (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_id INTEGER REFERENCES time_periods(period_id),
    sector TEXT NOT NULL,
    subsector TEXT,
    indicator TEXT,
    value REAL,
    unit TEXT,
    source TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_prod_uniq ON local_production(
    period_id, sector, COALESCE(subsector,''), COALESCE(indicator,''), source
);

CREATE TABLE IF NOT EXISTS plan_registry (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_name TEXT NOT NULL,
    lead_org TEXT,
    timeframe TEXT,
    year_published INTEGER,
    key_theme TEXT,
    source_url TEXT,
    notes TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_plan_uniq ON plan_registry(
    plan_name, lead_org
);
"""


def create_schema(db):
    db.executescript(SCHEMA_SQL)
    db.commit()
