# Structural Heart Comparison Guide — working dir

Standalone hand-off, split from /workspace/coronary-specs on 2026-10-13. It covers TAVI, Mitral TEER, Tricuspid TEER and Shared accessories (34 device families, overall fill 65.0%).
**Not a git repo and not published yet.** The Structural Heart bot creates the GitHub repo and Pages site.

## Layout
- `structural-specs-verified.csv`: master table, one row per device family. `therapy` and `category` columns. Values come from GUDID plus pass values.
- `provenance.json`: per-cell source (doc + page + URL).
- `structural-recalls.csv`, `raw/recall_counts.json`: openFDA recalls matched by exact catalog/GTIN/PMA.
- `spec_by_cat.json`, `therapy_by_cat.json`: fields per category and the category→therapy map.
- `fam.py`: family definitions (the SH dict). Each entry is (raw/udi file, brand regex, include, exclude, category).
- `raw/udi/SH_*.json`: openFDA GUDID pulls (`fetch_sh.py`). `raw/catalogs.json` holds the catalog numbers.
- `sources/passSHNN/values.csv`: hand-verified values (model,field,value,source). `docs/` holds the downloaded IFUs/SSEDs, and `conflicts.json` is the conflict log when present.
- `build_master.py` (calls `passes_apply.py`) → master CSV. `recalls.py` → recalls. `fill.py` → fill rates per category/therapy.
- `app/template.html` + `app/build.py` → `site/preview/` (static site + service worker, cache prefix `sh-preview-` / `sh-live-`).
- `tools/tth.py <url> <tag>`: therapy-filter test (every therapy × 3 views × desktop/mobile, screenshots, JS errors).
- `tools/tl.py <url> <tag>`: view and picker-dedupe test.
- `tools/tui.py` is inherited from coronary. Its reprocessing test is coronary-specific; adapt or drop it.
- `screenshots/`: verification captures (`sh02-*` from the coronary preview, `*local*` from this standalone build).
- `pg.py <pdf> <regex> <n>`: prints matches with page numbers.

## UI
- Therapy filter (TAVI | Mitral TEER | Tricuspid TEER | Shared accessories) drives the category list.
- Three views: Compare, Stacked, Desktop (remembered in localStorage `sh-view`).
- Picker dedupe; empty "+ Add device" slots (the table never collapses).
- Differences-only mode applies when 2 or more devices are selected.
- Non-applicable attributes are hidden per category.
- The reprocessing attribute was removed.

## Build
    python3 build_master.py && python3 recalls.py && python3 fill.py
    sed -i "s/'pass':'[0-9a-z]*'/'pass':'sh03'/" app/build.py && python3 app/build.py   # -> site/preview/
    cd site && python3 -m http.server 8765   # then: python3 tools/tth.py http://localhost:8765/preview/ local

`publish.sh` / `release.sh` are kept from coronary. Set `SITE_URL` and the git remote first. They assume a gh-pages subtree split of `site/`.

## Rules
See STANDING_DECISIONS.md. FILL_LOG.md has the pass history and gaps; SOURCES.md lists the sources.

## Open gaps (after pass sh13)
- Navitor Titan: commercial US IFU not found (only annulus range is filled, from the Abbott US page).
- EVOQUE: an updated IFU for S004 (56 mm) and S027 (jugular access, new sizing table) is not posted. Conflicts are logged.
- Accessory specs: wires (Safari/Confida/Lunderquist/Amplatz), large-bore sheath type/ID/OD, TRUE/Z-MED pressures, BRK, VersaCross, Tempo, WATCHMAN access sheaths.
- TEER independent grasping (OEM source needed).
