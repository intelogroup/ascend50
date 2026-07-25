# Graph Report - ascend50  (2026-07-25)

## Corpus Check
- 12 files · ~9,197 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 55 nodes · 106 edges · 9 communities (7 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f73ef355`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- seed_static.py
- refresh.py
- Ascend50 — Haiti Data Hub
- _lid
- fetch_hdx.py
- fetch_wb.py
- report.py
- fetch_iom.py
- queries.py

## God Nodes (most connected - your core abstractions)
1. `seed_all()` - 21 edges
2. `_lid()` - 11 edges
3. `main()` - 8 edges
4. `Ascend50 — Haiti Data Hub` - 7 edges
5. `fetch_hdx()` - 5 edges
6. `fetch_worldbank()` - 5 edges
7. `fetch_iom()` - 4 edges
8. `fetch_who()` - 3 edges
9. `main()` - 3 edges
10. `create_schema()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `fetch_hdx()`  [EXTRACTED]
  refresh.py → fetch_hdx.py
- `main()` --calls--> `fetch_iom()`  [EXTRACTED]
  refresh.py → fetch_iom.py
- `main()` --calls--> `fetch_worldbank()`  [EXTRACTED]
  refresh.py → fetch_wb.py
- `main()` --calls--> `seed_all()`  [EXTRACTED]
  refresh.py → seed_static.py
- `main()` --calls--> `fetch_who()`  [EXTRACTED]
  refresh.py → fetch_who.py

## Import Cycles
- None detected.

## Communities (9 total, 2 thin omitted)

### Community 0 - "seed_static.py"
Cohesion: 0.29
Nodes (12): seed_all(), seed_bilateral(), seed_energy_production(), seed_forest(), seed_geological(), seed_locations(), seed_macro(), seed_plans() (+4 more)

### Community 1 - "refresh.py"
Cohesion: 0.46
Nodes (4): fetch_who(), main(), print_summary(), create_schema()

### Community 2 - "Ascend50 — Haiti Data Hub"
Cohesion: 0.25
Nodes (7): Ascend50 — Haiti Data Hub, Data Sources, Deploy, Files, License, Quick Start, Schema — 24 Tables

### Community 3 - "_lid"
Cohesion: 0.25
Nodes (8): _lid(), seed_elevation(), seed_energy_access(), seed_geothermal(), seed_minerals(), seed_renewable(), seed_satellite(), seed_water_quality()

### Community 4 - "fetch_hdx.py"
Cohesion: 0.83
Nodes (3): fetch_hdx(), _lid(), _pid()

### Community 5 - "fetch_wb.py"
Cohesion: 0.83
Nodes (3): fetch_worldbank(), get_period_id(), upsert_economic()

### Community 6 - "report.py"
Cohesion: 0.83
Nodes (3): bar_chart(), main(), section()

## Knowledge Gaps
- **6 isolated node(s):** `Quick Start`, `Data Sources`, `Schema — 24 Tables`, `Files`, `Deploy` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `seed_all()` connect `seed_static.py` to `refresh.py`, `_lid`?**
  _High betweenness centrality (0.238) - this node is a cross-community bridge._
- **Why does `main()` connect `refresh.py` to `seed_static.py`, `fetch_hdx.py`, `fetch_wb.py`, `fetch_iom.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `fetch_hdx()` connect `fetch_hdx.py` to `refresh.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **What connects `Quick Start`, `Data Sources`, `Schema — 24 Tables` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._