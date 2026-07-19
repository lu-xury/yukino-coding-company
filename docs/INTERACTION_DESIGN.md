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
| 3 | waving | Restrained acknowledgement rather than enthusiastic greeting. |
| 4 | jumping / hover | Pointer notice, grounded micro-flinch, toe-rise/recoil, cool side-eye, recovery. |
| 5 | failed | Cool reproach, disappointment, or blocked-state reaction. |
| 6 | waiting | Reserved expectation when user approval or input is required. |
| 7 | running | Focused work/processing rather than literal locomotion. |
| 8 | review | Calm inspection and restrained acknowledgement of completed work. |
| 9–10 | look directions | Continuous mouse gaze in sixteen clockwise directions. |

## Why the hover row has five frames

The Codex v2 contract fixes row 4 to five used cells. Columns 5–7 must remain
transparent, so adding three visible frames would produce an invalid atlas and
would not create an eight-frame runtime loop.

Smoothness is therefore created through restrained movement and stable
registration, not by violating the frame contract.

### Five-frame hover acting plan

1. **Notice** — neutral baseline; eyes detect the pointer and one brow changes.
2. **Micro-flinch** — shoulders rise slightly, body shifts back, heels begin to
   lift, hair and ribbons lag.
3. **Peak avoidance** — subtle rise on the toes, cool side-eye, faint
   involuntary blush; the body never becomes airborne.
4. **Controlled settle** — heels lower and surprise becomes restrained
   reproach.
5. **Composed recovery** — original baseline returns; blush nearly disappears
   and posture is dignified.

The row uses stable-slot extraction to preserve one-to-two-pixel position
changes that would otherwise be erased by per-frame recentering. Independent
playback review confirmed no clipping or size popping.

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
