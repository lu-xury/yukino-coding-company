# Interaction and character design

## Character principles

The pet is designed around a restrained interpretation of Yukinoshita Yukino:

- cool, intelligent, observant, and self-possessed;
- tsundere warmth appears through small involuntary cues, not broad comedy;
- eye direction, eyelids, eyebrows, chin, head, hair, and shoulders carry most
  emotional information;
- feet, hips, body scale, and baseline remain stable whenever possible;
- no chibi proportions, celebratory bouncing, exaggerated surprise, or
  attention-seeking gestures.

The native cell is only `192x208`, so readable expression is achieved through
clear silhouettes and large facial landmarks rather than fine micro-detail.

## Event mapping

| Row | Runtime state | Design interpretation |
| ---: | --- | --- |
| 0 | idle | Quiet breathing, blinking, and composed observation. |
| 1 | running-right | Directional drag/travel toward screen-right. |
| 2 | running-left | Directional drag/travel toward screen-left. |
| 3 | waving | Restrained acknowledgement with the raised hand held across two frames. |
| 4 | jumping / hover | Pointer notice, grounded recoil, two-frame guarded side-eye, recovery. |
| 5 | failed | Arms-crossed cool reproach held long enough to read as a blocked-state reaction. |
| 6 | waiting | Crossed-arm, hip-shifted expectation held while user approval or input is required. |
| 7 | running | Focused hand-to-chin work/processing rather than literal locomotion. |
| 8 | review | Calm inspection followed by a held, restrained approval beat. |
| 9–10 | look directions | Continuous mouse gaze in sixteen clockwise directions. |

## Why the hover row has five frames

The Codex v2 contract fixes row 4 to five used cells. Columns 5–7 must remain
transparent, so adding three visible frames would produce an invalid atlas and
would not create an eight-frame runtime loop.

Smoothness is therefore created through restrained movement and stable
registration, not by violating the frame contract.

### Five-frame hover acting plan

1. **Notice** — neutral baseline; eyes detect the pointer and one brow changes.
2. **Grounded recoil** — shoulders draw inward, the upper body shifts back,
   and the arms begin guarding personal space.
3. **Guarded side-eye** — chin turns away, eyes narrow toward the intrusion,
   one hand stays near the chest or opposite arm, and faint blush appears.
4. **Held side-eye** — almost the same guarded pose remains on screen; only a
   blink, wrist change, or hair settle occurs.
5. **Composed recovery** — original baseline returns; blush nearly disappears
   and posture is dignified.

Both feet remain planted on the same baseline in every frame. Component-based
extraction preserves stable scale and placement without the previous
stable-slot exception.

![Hover animation](../previews/hover.gif)

## Mouse-look mechanics

The look system follows a clockwise sixteen-direction loop:

```text
000 up → 022.5 → 045 → 067.5 → 090 right → 112.5 → 135 →
157.5 → 180 down → 202.5 → 225 → 247.5 → 270 left →
292.5 → 315 → 337.5 → 000 up
```

The body uses a galgame standing-sprite lock:

- feet, legs, hips, skirt, and lower torso stay nearly frontal;
- eyes and eyelids lead;
- head and neck follow;
- shoulders follow only slightly;
- hair and red ribbons trail continuously;
- whole-sprite rotation, skewing, or broad raster warping is forbidden.

The four cardinals must be unmistakable. Near-axis intermediate directions may
be subtle if the ordered loop remains coherent and does not reverse.

## State priorities

Pets communicate activity rather than changing task behavior. Typical runtime
status mapping is:

- **Running** → focused work row;
- **Needs input** → waiting row;
- **Ready** → review row;
- **Blocked** → failed row.

The visual design should remain useful and low-distraction during long work.

## Perceived speed and held key poses

Codex owns the animation row timings and used-cell counts. `pet.json` has no
supported per-action speed field. Slower, clearer acting is therefore achieved
inside the fixed contract by holding the strongest pose in adjacent frames:

| State | Held frames (zero-based) | Readable beat |
| --- | --- | --- |
| waving | 1–2 | shoulder-height acknowledgement |
| jumping / hover | 2–3 | grounded guarded side-eye |
| failed | 2–5 | arms-crossed reproach |
| waiting | 2–4 | impatient needs-input pose |
| running | 2–4 | focused hand-to-chin work |
| review | 2–4 | small nod and restrained approval |

The held frames are not required to be pixel copies. A blink, tiny wrist
change, hair settle, or slight chin recovery keeps the animation alive while
preserving the same readable silhouette.

## Native-size clarity strategy

The runtime cell remains fixed at `192x208`, so facial readability cannot be
improved by shipping a larger incompatible atlas. The current art instead:

- fills the safe cell height while preserving normal 6.5–7-head proportions;
- uses darker, cleaner eye, eyelid, eyebrow, and mouth landmarks;
- keeps red ribbons, the red bow, and white blazer piping high contrast;
- separates hands and bent elbows from the dark hair and blazer silhouette;
- simplifies hair strands, plaid micro-lines, fabric noise, and low-contrast
  shading that would blur after downsampling.
