# STANDING_DECISIONS — Structural Heart
Inherited rules (from coronary-specs):
- Exact-model values only; never copy from a sibling model. Every cell needs doc + page + URL.
- Log conflicts, do not overwrite; IFU/SSED beats brochure.
- Numbered passes (passSHNN) with backups structural-specs-verified.pre-passSHNN.csv.
- Keep FILL_LOG, SOURCES, INDEX, STANDING_DECISIONS current.
- Recalls via openFDA, matched by exact catalog/GTIN/PMA.
- US-labelled indications only (e.g. PASCAL has no US tricuspid label -> no tricuspid row).
- Exclude devices not labelled for the therapy area.
- Publish to /preview/ first; root only with Jeff's explicit approval via release.sh <tag>.
History:
- 2026-10-13: Scope expanded (Jeff approved) to "Coronary & Structural Heart": therapy filter Coronary | TAVI | Mitral TEER | Tricuspid TEER | Shared accessories. Same data rules. US-labelled indications only (e.g. PASCAL tricuspid not added — no US label). Preview only until Jeff approves a root release.
- 2026-10-13: v1.6 (preview-passsh02: Coronary & Structural Heart, fill 76.0%) released to root with Jeff's approval.
- 2026-10-13: Structural heart split into its own bot/guide (this dir). Reprocessing attribute removed. No repo/publish yet — the Structural Heart bot owns that.
- 2026-10-13: passSH03 (preview only): added Mitral TMVR (SAPIEN M3, P250019), Tricuspid TTVR (EVOQUE, P230013), LAAO (WATCHMAN FLX, FLX Pro, Amulet + 4 access/delivery sheaths); Sentinel filled from DEN160043/K192460; SAPIEN 3 PMA P140031. EVOQUE 56 mm is in GUDID but not in the original SSED (logged in conflicts). Guides menu reads /workspace/guides.json at build; this guide stays "coming_soon" (preview link) until release.sh.
- 2026-10-14: UI (preview-passsh05, preview only): CRM-style fixed supplier columns (Edwards, Medtronic, Abbott, Boston Scientific first, then others A–Z; only suppliers with devices in the category), each with its own product dropdown; supplier = US marketer (Baylis→Boston Scientific, Essential Medical→Teleflex, SAFARI→Boston Scientific), GUDID labeler still shown as manufacturer.
- 2026-10-14: passSH06 (preview only): valve_position for TAVI valves (OEM brochure/IFU/web page or FDA order; SAPIEN 3 original left blank — no exact-model source); family/generation/fda_approval_date from FDA PMA decision dates (Latest = newest US approval in family; Navitor + Navitor Titan both Latest, Titan = 35 mm size extension); dropdowns sorted newest-first; Supra/Intra filter on TAVI valve; Trilogy PMA P250024.
- 2026-10-14: v1.0 (preview-passsh06 build) released to ROOT https://jeffmcd83.github.io/structural-compare/ with Jeff's approval; guides.json structural-heart = live. Future passes publish to /preview/ first.
- 2026-10-14: v1.0.1 fix: Desktop view section-header rows now use a sticky th.a label cell + colspan td (was one full-width colspan th, which can't stick); tools/tsticky.py (run by tui.py) checks every label cell stays pinned and opaque.

## sh08 (2026-10-13): single therapy+category dropdown
- #th removed; #cat uses optgroups "Therapy – Category", order TAVI, Mitral TEER, Tricuspid TEER, TMVR, TTVR, LAAO, Shared accessories; default TAVI valve.
- Hash now c=&m=; legacy #t= maps to the therapy's first category; legacy 4-slot m lists remapped by supplier membership. Test: tools/tnav.py.

## sh09: mobile #cat sizing
- <=720px: 14px (matches CRM mobile select), weight 400, padding 6px 8px, auto width; therapy prefixes shortened (M-TEER, T-TEER, TMVR, TTVR, Shared). Desktop unchanged.

## sh10 (2026-10-16): search + compatibility view (preview only)
- Header search: model/family/supplier/manufacturer + ALIAS table in template (S3UR, FX+, FLX Pro, …); results grouped by category; pick switches category and selects in supplier column.
- Compatibility view (#cp=<model>): delivery system / sheaths / access routes from existing sourced cells; wires, embolic protection, closure, valvuloplasty from sources/passSH10/compat.csv (verbatim labeling statements from cached IFU/SSED, page-cited). Nothing inferred; empty = "Not stated in labeling". Generic requirements shown as generic (no brand implied). Embolic/valvuloplasty shown for TAVI valves only. Navitor Titan: Navitor IFU ARTMT600163776_B does not cover it -> all Not stated. Tests: tools/tfeat.py.

## sh11 (2026-10-16): study evidence in Compatibility view
- sources/passSH11/study.csv (27 items, 20 papers), kept separate from labeling (core.json compat[m].label vs .study). Rule: peer-reviewed clinical study (trial/registry/cohort; no case reports, bench, reviews) whose text names BOTH exact products as used in the cohort. Generic "eSheath", "DrySeal" without Flex, "Perclose" without model, "Sapien S3/Ultra" style ambiguity, and "e.g." lists excluded. Cohort-level co-use flagged in the quote text. Links: PMC when available, else PubMed; tools/tlinks.py verifies PMC citation_title and, for PubMed-only items, E-utilities record + DOI handle (PubMed blocks automated fetches from the box with 403/203).
