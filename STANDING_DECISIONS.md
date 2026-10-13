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
