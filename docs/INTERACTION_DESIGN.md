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

## Operation-to-animation mapping

The mapping below describes observable Codex desktop behavior in app build
`26.715.52143`. A custom pet supplies artwork for fixed runtime states; it does
not choose which application event activates a state.

| User or task operation | Runtime state / row | Yukino action |
| --- | --- | --- |
| Wake the pet for the first time | `waving`, row 3 | Raises an open hand and makes a small formal bow. |
| Move the pointer onto the pet | `jumping`, row 4 | Blushes, raises a stop palm, and shakes her head left–center–right in refusal. |
| Drag the pet toward screen-right | `running-right`, row 1 | Runs toward screen-right while being dragged. |
| Drag the pet toward screen-left | `running-left`, row 2 | Runs toward screen-left while being dragged. |
| Move the pointer around the pet while look tracking is active | rows 9–10 | Eyes, head, neck, and hair follow the pointer through sixteen directions. |
| A task is actively loading or working | `running`, row 7 | Bends clearly from the waist to inspect the work below and in front of her. |
| Codex needs approval, an answer, or other user input | `waiting`, row 6 | Lowers into a compact crouch and waits with her cheek supported by one hand. |
| A task is blocked or fails | `failed`, row 5 | Plants both hands on her hips and leans forward in a stern reprimand. |
| Work completes and has unread output ready | `review`, row 8 | Straightens confidently, keeps one hand on her hip, and gives a deliberate approving nod. |
| No event state is active | `idle`, row 0 | Quiet breathing, blinking, and composed observation. |

Status rows may be easy to miss if the task transition happens while the pet
is covered, off-screen, or unattended. Codex starts the action when the state
changes; it does not wait for the user to look at the pet.

## Why event actions play three times

The desktop renderer deliberately expands every non-idle row into three copies
of the same frame sequence and then switches to the slow idle loop. In compact
form, its playback rule is:

```text
non-idle state = action + action + action + slow idle loop
```

This is application behavior, not three duplicated animations inside this
spritesheet. `pet.json` has no supported repeat-count or per-frame-speed field,
so a custom pet cannot request one play. The hover row is therefore authored as
a repeat-friendly head-shake loop; three repeats read as one sustained refusal
rather than three unrelated gestures.

## Why the hover row has five frames

The Codex v2 contract fixes row 4 to five used cells. Columns 5–7 must remain
transparent, so adding three visible frames would produce an invalid atlas and
would not create an eight-frame runtime loop.

Smoothness is therefore created through restrained movement and stable
registration, not by violating the frame contract.

### Five-frame hover acting plan

1. **Blushing center** — shoulders tense and both hands draw toward the chest.
2. **No, left** — eyes close, the head turns screen-left, and one palm clearly
   signals stop.
3. **Center crossing** — the chin lowers through center while the arms guard
   the torso.
4. **No, right** — the head turns screen-right with the same stop palm.
5. **Refusal hold** — red-faced arms-crossed refusal returns to center and
   connects cleanly to the first frame.

Both feet remain planted on the same baseline in every frame. Component-based
extraction preserves stable scale and placement without the previous
stable-slot exception.

![Hover animation](../previews/hover.gif)

The documentation GIF shows one five-frame row cycle. Codex desktop repeats
that cycle three times when the pointer enters the pet.

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

## Perceived speed and clear silhouettes

Codex owns the animation row timings and used-cell counts. `pet.json` has no
supported per-action speed or repeat-count field. Clear acting is therefore
achieved with large, repeat-friendly full-body silhouettes:

| State | Dominant readable silhouette |
| --- | --- |
| waving | raised open palm plus visible formal bow |
| jumping / hover | red-faced left–center–right head shake with stop palm |
| failed | both hands on hips plus forward scolding lean |
| waiting | compact low crouch with one hand supporting the cheek |
| running | 25–35 degree waist bend for close inspection |
| review | confident hand-on-hip stance plus deliberate nod |

The silhouette is intentionally much larger than the facial cue. A blink,
eyebrow change, hair settle, or blush supports the pose but never carries the
meaning alone.

## Native-size clarity strategy

The runtime cell remains fixed at `192x208`, so facial readability cannot be
improved by shipping a larger incompatible atlas. The current art instead:

- fills the safe cell height while preserving normal 6.5–7-head proportions;
- uses darker, cleaner eye, eyelid, eyebrow, and mouth landmarks;
- keeps red ribbons, the red bow, and white blazer piping high contrast;
- separates hands and bent elbows from the dark hair and blazer silhouette;
- simplifies hair strands, plaid micro-lines, fabric noise, and low-contrast
  shading that would blur after downsampling.
