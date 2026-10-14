# HANDOFF — Structural Heart (TAVI/TEER) guide
Live: https://jeffmcd83.github.io/structural-compare/  ·  Written 2026-10-14

## How it's built
- **Source data:** this repo (`/workspace/structural-specs`): verified CSVs, `sources/`, `FILL_LOG.md`, `SOURCES.md`, `STANDING_DECISIONS.md`, `provenance.json`.
- **Build:** `python3 build_master.py && python3 app/build.py` writes the preview build to `site/preview/` (index.html, data/, sw.js, manifest.webmanifest).
- **Hosting:** GitHub Pages from branch `gh-pages`, which is a `git subtree split` of the `site/` folder on `master`. Root = live, `/preview/` = preview.
- **Offline:** `site/sw.js` (cache `sh-live-…`, network-first with cache fallback) + `site/manifest.webmanifest`.

## Data rules
Verified sources only, naming the exact model/catalog number; every value links to its source; blanks stay blank; conflicts are logged, never overwritten. See STANDING_DECISIONS.md.

## How it's updated (deploy safety)
- `./publish.sh NN` — build preview, run `tools/site_gate.py site "" preview/` (headless Chrome smoke test of live + preview). Failure/crash => exit before commit/push.
- `./release.sh TAG` — promote preview to root (live), then the same gate; on failure do not push (`git checkout -- site`). After a pass: commit, tag, then `git subtree split --prefix site -b g2 && git push -f origin g2:gh-pages && git branch -D g2`.
- Root releases need Jeff's OK (preview first).

## How to roll back
See ROLLBACK.md. Tag `stable` = last known-good live state (2026-10-14).

## Backups
Off-box backup of working files (CSVs, scripts, logs, STANDING_DECISIONS, PDF manifest): private repo `jeffmcd83/device-guides-backup`, refreshed by `bash /workspace/backup_guides.sh`.

## If the bot is gone
The site keeps serving as-is from GitHub Pages. To maintain: clone this repo, restore working files from the backup repo into `/workspace/`, run the build + gate commands above (needs Python 3, openpyxl, playwright + Chrome).
