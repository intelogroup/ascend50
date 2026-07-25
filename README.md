# Ascend50 — Haiti Data Hub

Combined SQLite database of Haiti development data. Refreshes from live APIs (World Bank, HDX HAPI) plus static reference data (minerals, geothermal, water, forest, trade, strategic plans).

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# fill HDX_APP_IDENTIFIER in .env (get at link in file)
python refresh.py
python queries.py
python report.py   # generates report.html
```

## Data Sources

| Source | Type | Endpoints | Rows |
|--------|------|-----------|------|
| World Bank API | Live | 11 indicators (GDP, inflation, population, trade, health, internet, forest, unemployment, poverty, electricity) | 257 |
| HDX HAPI v2 | Live | baseline-population, food-security, refugees, humanitarian-needs, rainfall, operational-presence, poverty-rate, conflict-events, funding | ~180 |
| Static reference | Seeded | Water quality, forest cover, mineral resources, geothermal springs, geology, DEM, satellite, macroeconomic, trade, bilateral trade DR, local production, strategic plans, energy access, energy production, renewable potential, governance, justice, security, education, diaspora, telecom, transport, climate | 188 |

## Schema — 24 Tables

population_data, food_security_data, water_quality_data, health_humanitarian_data, economic_data, hazards_data, forest_data, mineral_resources, geothermal_data, geological_data, elevation_data, satellite_imagery, macroeconomic_data, trade_data, bilateral_trade_dr, local_production, plan_registry, electricity_access, energy_production_consumption, renewable_potential, social_institutional_data, displacement_data, locations, time_periods

## Files

| File | Purpose |
|------|---------|
| `refresh.py` | Entry point — builds/updates `ascend50.db` |
| `schema.py` | All CREATE TABLE + UNIQUE index statements |
| `config.py` | API endpoints, env vars, indicator lists |
| `seed_static.py` | Static reference data seeding |
| `fetch_wb.py` | World Bank API fetcher (pagination + null filtering) |
| `fetch_hdx.py` | HDX HAPI v2 fetcher (9 endpoints) |
| `queries.py` | 14 pre-built analytic views |
| `report.py` | Self-contained HTML report generator (zero deps) |
| `.env.example` | Env template with HDX key instructions |

## Deploy

Render cron job runs `python refresh.py` daily at midnight UTC:

https://dashboard.render.com/cron/crn-d9ihkk7lk1mc73d3e8kg

## License

MIT
