# Changelog

All notable changes are documented here. The project follows Semantic
Versioning for repository releases; the installed pet id remains
`yukino-yukinoshita`.

## [Unreleased]

### Added

- Added a version-locked macOS Codex `26.721.41059` runtime patcher with
  integrity updates, automatic backups, status checks, and restoration.
- Added a reproducible native-size animated showcase generated directly from
  the final atlas using the patched one-cycle, `2x`-duration timing.

### Changed

- Patched interaction playback uses one action cycle at twice the stock frame
  duration before returning to the slow idle loop.
- Updated installation and interaction documentation to distinguish stock
  renderer behavior from the optional runtime patch.
- Documented the macOS Files and Folders permission reset that can follow an
  application-signature change.

## [1.5.0] - 2026-07-25

### Changed

- Rebuilt event rows 3–8 as large-silhouette **pose holds** (raised-hand greeting,
  bent-knee hover refusal, head-down failure, open-palm crouch wait, waist-bent
  inspection, and arms-crossed peace-sign finish) so Codex's stock three-copy
  playback reads as one sustained slow action instead of restarted gestures.
- Strengthened native-size readability for low-resolution pet cells with broader
  full-body silhouettes, especially crouch-wait and bend-to-inspect.
- Regenerated motion previews and contact sheet for the repaired rows.

### Notes

- `pet.json` still has no supported speed or repeat-count field; timing and the
  three-copy rule remain renderer-owned.
- Rows 0–2 and 9–10 are unchanged from 1.4.0. Row 8 review is a raised
  victory/peace-hand hold assembled for native-size readability under imagegen
  network unavailability.

### Verified

- `python scripts/validate_pet.py` passes.
- Codex v2 atlas validation passes at `1536x2288` with zero transparent RGB residue.
- Only rows 3–7 differ from the previous packaged atlas.

## [1.4.0] - 2026-07-21

### Changed

- Upgraded action rows 3–8 to Option C micro-dynamics pose holds: actions instantly enter key poses and hold continuous state without repetitive loop motion, enriched by natural eye blinks, breathing shifts, and subtle gaze micro-movement.
- Re-rendered all preview GIFs and contact sheet with 220ms slow frame durations to match the refined living hold dynamics.

## [1.3.0] - 2026-07-20

### Changed

- Rebuilt all six event rows around large native-size silhouettes: formal bow,
  blushing head-shake refusal, hands-on-hips reprimand, compact crouch,
  waist-bent inspection, and confident nodding approval.
- Re-authored hover as a five-frame left-center-right refusal loop that remains
  natural when Codex repeats the row three times.
- Used stable-slot extraction for the crouching waiting row so the character
  does not grow or jump vertically when her body becomes shorter.
- Added an explicit operation-to-animation table to the Chinese and English
  READMEs and the interaction design document.
- Documented the renderer-owned three-repeat rule, fixed per-frame timings, and
  the lack of a supported repeat-count or speed field in `pet.json`.

### Fixed

- Updated GitHub Actions to `actions/setup-python@v6` and explicitly pointed
  pip caching at `requirements-dev.txt`, fixing the failed setup step and the
  Node 20 deprecation warning.

### Verified

- Independent native-size visual QA passes all six repaired event rows.
- Codex v2 atlas validation passes at `1536x2288` with no errors or warnings.
- Rows 0–2 and 9–10 are pixel-identical to version 1.2.0; only rows 3–8 changed.
- All hard cardinal blind-direction gates pass; intermediate ambiguity remains
  recorded as reviewed warnings.

## [1.2.0] - 2026-07-19

### Changed

- Rebuilt all six event-action rows with adjacent-frame key-pose holds so the
  actions read more slowly without changing Codex's fixed frame contract.
- Strengthened native-size silhouettes and high-contrast eyes, brows, ribbons,
  blazer piping, hands, socks, and shoes while simplifying blur-prone
  micro-detail.
- Kept the hover reaction fully grounded and replaced the former toe-rise with
  a guarded upper-body recoil and held displeased side-eye.
- Added individual previews for greeting, hover, failure, waiting, working,
  and review states.

### Verified

- Independent visual QA passes at the native `192x208` cell size.
- Rows 3–8 changed; rows 0–2 and 9–10 are pixel-identical to version 1.1.0.
- Codex v2 atlas validation and existing hard cardinal direction gates pass.

## [1.1.0] - 2026-07-19

### Changed

- Replaced the airborne celebratory hover animation with a grounded,
  persona-consistent notice/recoil/reproach/recovery loop.
- Improved final-size readability with cleaner cel edges and reduced
  micro-detail noise.
- Added complete GitHub-ready documentation, validation tooling, CI, issue
  templates, and explicit asset licensing boundaries.

### Verified

- Codex v2 atlas: `1536x2288`.
- Lossless RGBA WebP.
- Only the hover row changed from the previous approved atlas.
- Direction rows and blind cardinal validation remain unchanged and passing.

## [1.0.0] - 2026-07-19

- Initial Codex v2 pet release with nine standard animation rows and sixteen
  clockwise look directions.
