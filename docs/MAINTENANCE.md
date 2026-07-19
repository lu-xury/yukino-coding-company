# Maintenance and release guide

## Safe maintenance principles

- Preserve the last passing release before visual changes.
- Change the smallest complete animation row that satisfies the request.
- Never patch a final normalized look cell independently; regenerate its
  complete coherent eight-frame look row.
- Preserve unrelated rows and QA evidence.
- Keep character-derived assets outside the MIT license grant.
- Do not include official reference images in commits or releases.

## Updating documentation only

1. Edit Markdown or repository metadata.
2. Run `python scripts/validate_pet.py` to ensure packaging was not damaged.
3. Check relative links.
4. Update `CHANGELOG.md` when user-visible instructions change.
5. Open a pull request.

## Updating a standard animation row

1. Record the behavioral problem and target character interpretation.
2. Preserve the exact row frame count from
   [SPRITE_CONTRACT.md](SPRITE_CONTRACT.md).
3. Generate or edit the entire row coherently at high source resolution.
4. Use deterministic extraction and preserve subtle source placement when
   stable-slot extraction materially improves motion.
5. Inspect the row at native `192x208` size.
6. Recompose the nine standard rows.
7. Reattach the existing approved look rows.
8. Run the single final chroma cleanup pass for that repair build.
9. Validate the complete v2 atlas.
10. Compare every row against the previous release and confirm only intended
    rows changed.
11. Run independent visual QA.

## Updating look directions

1. Define character-specific look mechanics.
2. Approve four cardinals: up, right, down, left.
3. Generate row 9 as one eight-pose family.
4. Register and review row 9 before generating row 10.
5. Generate row 10 using final row 9 as continuity evidence.
6. Run labeled semantic review, continuity analysis, and three isolated blind
   axis reviews.
7. Regenerate a complete containing row for any major failure.

## Managing large multimodal requests

To reduce HTTP 413 and context-size failures:

- generate one visual job per request;
- load only that job's required references;
- use resized/high viewing detail instead of original resolution when it is
  sufficient;
- do not include unrelated conversation history or multiple row prompts;
- decode and persist the selected image immediately;
- run deterministic image processing locally.

## Versioning

- Patch: documentation, validation, or packaging fix with unchanged visuals.
- Minor: visible row improvement or interaction refinement.
- Major: incompatible atlas contract, pet id, or installation layout change.

Update `VERSION`, `CHANGELOG.md`, `CITATION.cff`, and the Git tag together.

## Release checklist

```text
[ ] python scripts/validate_pet.py passes
[ ] pet/pet.json and pet/spritesheet.webp are staged together
[ ] contact sheet matches the release atlas
[ ] previews show the current behavior
[ ] QA JSON files match the release
[ ] README installation commands are current
[ ] asset notice and license boundary remain visible
[ ] CHANGELOG and VERSION are updated
[ ] git diff contains no official reference images or secrets
[ ] GitHub Actions passes
[ ] release notes include install and update instructions
```

## Suggested Git commands

```bash
git switch -c fix/hover-animation
python scripts/validate_pet.py
git status
git diff --stat
git add .
git commit -m "fix: refine hover interaction"
git push -u origin fix/hover-animation
```

Avoid force-pushing the default branch and avoid destructive reset commands in
a dirty worktree.
