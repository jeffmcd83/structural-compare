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

## 2026-10-21 weekly recall check (pass sh12)
- New openFDA recall: Amplatzer Amulet, Z-0191-2027 (event 99844), Class 2, initiated 2026-09-10, posted 2026-10-16, IFU update re pulmonary artery injury risk; 8 models 9-ACP2-* matched by catalog/GTIN. Source: https://api.fda.gov/device/recall.json?search=product_res_number:"Z-0191-2027" and https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRES/res.cfm?id=222724
- New FDA Early Alert (not yet in openFDA): Edwards Commander M delivery system 9880CM29 for SAPIEN M3, lots 67718561/67804014/67887043/67887044, balloon burst, 1 death. Posted 2026-10-15. Stored in raw/recall_manual.csv (merged by recalls.py). Source: https://www.fda.gov/medical-devices/medical-device-recalls-and-early-alerts/early-alert-transcatheter-mitral-valve-delivery-system-issue-edwards-lifesciences
- Recall entries now show a Source link on the page.

## Pass SH13 — gap fill (2026-10-22, /preview/ only, tag preview-passsh13). 29 values applied, 2 conflicts logged (not applied). Backup structural-specs-verified.pre-passSH13.csv. Overall 69.9% → 75.0% (TAVI valve 83→91%, closure 67→93%, CEP 83→100%, valvuloplasty 46→58%, steerable 50→64%, LAAO device 94→97%).
Filled (sources/passSH13/values.csv, docs in sources/passSH13/docs/):
- Evolut PRO+ / Evolut FX: annulus table, leaflet tissue, skirt, delivery profile; Evolut FX+: tissue, skirt. Source: FDA-posted labeling P130021S174D.pdf, which holds three separate exact-model US IFUs (PRO+ pp.1–28, FX pp.29–56, FX+ pp.57–84). Page numbers are PDF pages.
- Navitor Titan: annulus range only (NVRO-35 row, Abbott US HCP Navitor page; NVRO-35 = Titan per FDA P190023/S023).
- Trilogy: annulus table (FDA-posted Trilogy IFU P250024D Table 2 p.4).
- Amplatzer Amulet: fda_submission P200049 (SSED P200049 p.1 + openFDA PMA record, original approval 2021-08-14). P160012 is NOT Amulet; it is a Physio-Control LIFEPAK AED PMA.
- Perclose ProStyle (IFU P960043S118C) and ProGlide (SSED P960043S118B): mechanism, closure range (artery 5–21F, vein 5–24F), sheath/wire, indications.
- Agilis NxT: curves, deflection type, inner diameter (Abbott US ordering + ISI pages).
- TRUE Dilatation: shaft length 110 cm, sheath 11–14 Fr, indication (510(k) summary K150667).
- Sentinel: 6 Fr, 95 cm working length (510(k) summary K192460 p.4).
Conflicts (sources/conflicts_passes.json, existing values kept):
- EVOQUE valve_sizes_mm: FDA PMA P230013/S004 (2024-10-03) approved the 56 mm size. New value 44/48/52/56 mm vs existing GUDID 44/48/52 mm. This resolves the passSH03 open question: 56 mm is US-approved. The updated IFU is not posted on accessdata.
- EVOQUE access_routes: P230013/S027 (2026-09-16) adds internal jugular venous access and revises the sizing table. New value vs existing "Transfemoral venous". Updated IFU not posted. The annulus/sizing table may also be out of date.
Gaps / declined:
- Navitor Titan: the only Titan-specific IFU found (ARTEN600158216 A, PRT-NG-35) is the IDE/investigational version, so it was declined. Navitor IFU rev D (ARTMT600163776_D) is OUS multilingual and has no NVRO-35. All other Titan fields still blank.
- Safari: the BSC US page covers SAFARI² (H74939406/407, 275 cm), a different model from the master Safari (H74939271/272, 260/300 cm), so nothing was copied. Confida, Lunderquist and Amplatz specs: no OEM US IFU fetched.
- TRUE nominal/RBP: not in the 510(k) summary, the BD sell sheet is blocked (403), and the BD US page gives no numbers. Z-MED II, eSheath+/Optima/Sentrant/DrySeal type/ID/OD, BRK, VersaCross, Tempo, WATCHMAN access sheaths: not attempted this pass.
- Agilis 13 F SI-1371 (US ordering page) is not in master/GUDID family: candidate for a future row.
