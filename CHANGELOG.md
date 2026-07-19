# Changelog

All notable changes are documented here. The project follows Semantic
Versioning for repository releases; the installed pet id remains
`yukino-yukinoshita`.

## [Unreleased]

### Fixed

- Updated GitHub Actions to `actions/setup-python@v6` and explicitly pointed
  pip caching at `requirements-dev.txt`, fixing the failed setup step and the
  Node 20 deprecation warning.

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
