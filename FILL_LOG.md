# FILL_LOG — Structural Heart (split from coronary-specs 2026-10-13)

## Structural heart expansion — 34 families / 25 SH rows added (GUDID families via fam.py SH dict; therapy field; recall matching re-run)
## Pass SH01 — TAVI valves (/preview/ only, tag preview-passsh01). 65 values. Backup coronary-specs-verified.pre-passSH01.csv. Overall 73.6% (TAVI valve 81%).
Sources: Edwards combined S3/S3U/S3UR US IFU DOC-0251232B (pp.1–13); Abbott Navitor IFU ARTMT600163776_B (pp.3–5); Medtronic US Evolut FX+ HCP page ISI (shared PRO+/FX/FX+ labelling) + FX+ spec sheet UC202402378a; FDA SSED P250024 (Trilogy, approved 2026-03-17 for aortic REGURGITATION).
Gaps: Navitor Titan (separate IFU not found); Evolut PRO+/FX annulus + tissue/skirt (no exact-model US doc fetched; Medtronic PDFs block curl); Trilogy annulus table (SSED gives perimeter-diameter trial criteria only); S3 transapical/transaortic (Certitude) not captured.
## Pass SH02 — TEER + closure + submissions (/preview/ only, tag preview-passsh02). 33 values. Backup coronary-specs-verified.pre-passSH02.csv. Overall 76.0%.
Sources: SSED P220003 (PASCAL Precision), SSED P230007 (TriClip G4), SSED P180025 (MANTA), Abbott US MitraClip page + G4 US ISI PDF, openFDA PMA/510(k) records.
Findings: PASCAL has no US tricuspid indication (P220003 = degenerative MR, prohibitive risk) — no PASCAL tricuspid row created. TriClip SSED labels no transjugular route.
Gaps: wires/sheaths/Sentinel/valvuloplasty/Tempo/BRK/VersaCross/Agilis spec fields mostly unfilled (need OEM IFUs); Perclose closure range; independent grasping (only third-party JACC source for MitraClip G4 — declined).

## Split — 2026-10-13
Moved to standalone /workspace/structural-specs. Reprocessing attribute dropped (no reprocessed structural devices; TAVI etc). Not yet published; overall fill 65.0% (34 rows).
