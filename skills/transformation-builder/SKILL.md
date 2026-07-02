---
name: transformation-builder
description: "Guidance for building ImageKit image/video transformation URLs with the transformation_builder tool — how the tool works, how to write a good query, how to order multi-step chains, and a reference of every supported parameter. Use before calling transformation_builder. Covers resize/crop/focus, AI edits (change objects, colors, styles), background removal/replacement, generative fill, upscaling, retouching, drop shadows, variations, effects (blur/sharpen/rotate/border/color-replace/gradient), image/text/video overlays, and video transforms."
---

# Transformation Builder Skill

Understand how the tool works, write a precise query, order multi-step chains correctly, then call `transformation_builder`.

## How this tool actually works (read this first)

`transformation_builder` is **not** a capability picker. Its only inputs are:

```
transformation_builder(query, src?, previous_errors?)
```

- `query` — a **natural-language** description of the desired transformation.
- `src` — optional ImageKit-hosted source URL (defaults to a sample image).
- `previous_errors` — pass the error text from a prior failed call so the tool can self-correct.

Internally the tool: (1) searches ImageKit docs using your `query`, (2) an LLM turns it into a validated list of transformation steps, (3) the SDK builds the final URL. There is **no `capability` argument** — the parameter names below are **vocabulary to put into your query**, not API fields you set directly. Because step 1 is a doc search over your query text, **using the correct ImageKit parameter names and values in the query materially improves the result.** Using wrong/invented names sends the search off course.

So your job is: translate the user's vague request into a precise query that references **real** parameters and values from the reference section below.

## When to use (triggers this skill)

- Resize, crop, or focus on a region
- Filters, effects, overlays (image/text/video), watermarks
- Multi-step transformation chains
- Background removal, replacement, or generative fill
- Any AI-powered image editing (change objects/colors/styles, upscale, retouch, drop shadow, variations)

## Calling `transformation_builder`

- `query`: the precise, rewritten description (see Query Crafting). **Never pass the user's vague words through unchanged.**
- `src`: the ImageKit delivery URL to transform, if the user gave one. Must be ImageKit-hosted.
- Frame a multi-step request as **one query** describing the steps in order:
  - User: "1) Resize to 800x600  2) Crop to the face"
  - Query: "Resize to width 800 and height 600, then crop with focus on the face"

## Query Crafting

**Rule: rewrite the vague request into a description that names real parameters and values. Use exact parameter names/values when you know them; fall back to plain English only when unsure.**

| User says | Weak query | Good query |
|---|---|---|
| "Make the red balls green" | "make red balls green" | "Apply an AI edit (`ai_edit`) with prompt: change the red balls to green" |
| "Clean it up and put it on white" | "clean up, white background" | "Apply `ai_retouch`, then `ai_remove_background`, then `ai_change_background` with prompt: solid white background" |
| "Make it look like a painting" | "painting style" | "Apply `ai_edit` with prompt: oil-painting style with visible brush strokes" |
| "Crop around the face" | "crop face" | "Resize with `focus`=`face` to crop around the detected face" |
| "Text 'Hello' at the bottom" | "add hello text" | "Add a text overlay with text 'Hello', positioned at the bottom (`focus`=`bottom`)" |
| "Fit a mobile banner" | "mobile banner" | "Resize to `width`=640 with `aspect_ratio`=2-1" |
| "300px wide with a red border" | "resize and border" | "Resize to `width`=300, then add a `border` of width 5 and color red" |
| "Higher resolution, it's blurry" | "fix quality" | "Apply `ai_upscale`, then `ai_retouch`" |
| "Remove bg and add a shadow" | "remove bg shadow" | "Apply `ai_remove_background`, then `ai_drop_shadow`" |
| "Make it wider without stretching" | "make wider" | "Extend the canvas horizontally using a padded crop (`crop_mode`=`pad_extract`) with `background`=`genfill` so AI fills the new area" |

### Intent → real parameter/vocabulary

Use this to translate intent into the correct terms to put in the query. These are the **actual** parameter names the tool validates against.

| User intent | Use this vocabulary | Notes |
|---|---|---|
| Modify specific objects/regions ("enlarge the cat", "add sunglasses", "make it a painting") | `ai_edit` (prompt-based) | AI content edit driven by a text prompt |
| Replace the whole background scene ("put them on a beach") | `ai_change_background` (prompt-based) | Keeps the subject, generates a new scene. Not for plain removal or color changes |
| Remove background → transparent | `ai_remove_background` | ImageKit-native. For the external remove.bg engine use `ai_remove_background_external` |
| Extend/outpaint the canvas ("add more sky", "make it panoramic") | padded crop + `background`=`genfill` | Generative fill lives in the **background** param, not a standalone AI field. Takes **no prompt** |
| Increase resolution / fix low-res | `ai_upscale` | Boolean; no params |
| Clean up / remove blemishes | `ai_retouch` | Boolean; no params |
| Realistic shadow under a cut-out subject | `ai_drop_shadow` | Transparent images only. Optional `azimuth`, `elevation`, `strength` |
| Different version / remix | `ai_variation` | Boolean; preserves structure |
| Resize / aspect ratio / crop | `width`, `height`, `aspect_ratio`, `crop`, `crop_mode` | See Resize & Crop table |
| Smart crop to face/object | `focus` (`auto`, `face`, or an object name) + optional `zoom` | Object names are COCO classes (`person`, `car`, `dog`, …) |
| Swap one color across all pixels ("all red → blue") | `color_replace` | Global pixel color swap with `tolerance` |
| Filters/adjustments (B&W, blur, sharpen, rotate, border, round corners) | `grayscale`, `blur`, `sharpen`, `rotation`, `border`, `radius`, … | See Effects table |
| Overlay a logo/watermark image | text/image **overlay** | Single `overlay` concept, typed (see Overlays) |
| Write text on the image | text **overlay** with `text` | See Overlays |

> There is **no** "generate an image from scratch" step in this tool — it always transforms an existing `src`. Text-to-image (`ik-genimg`) is a separate feature, not part of `transformation_builder`.

### Key distinction: `ai_edit` vs `color_replace` vs `ai_change_background`

1. Changing specific objects/regions ("make the balls bigger", "turn the car red") → **`ai_edit`**
2. Swapping one color globally across all pixels ("replace all red with blue") → **`color_replace`**
3. Replacing the entire background scene ("put them on a beach") → **`ai_change_background`**

## Ordering multi-step chains

When a request spans multiple operations, chain them in **one query in this order**:

1. **Upscale / retouch** (quality first)
2. **AI content edits** (`ai_edit`)
3. **Background removal / replacement** (`ai_remove_background`, `ai_change_background`)
4. **Resize / crop** (final dimensions)
5. **Effects / overlays** (finishing touches)

**Critical: background removal goes AFTER upscale/retouch, never before.**
Correct: `ai_upscale → ai_remove_background`. Wrong: `ai_remove_background → ai_upscale`.

Example — "clean up this photo, remove the background, make it 500x500":
→ Query: "Apply `ai_retouch`, then `ai_remove_background`, then resize to `width`=500 and `height`=500".

## Background removal: clarify intent

- If the user says "remove background" ambiguously, ask whether they want:
  1. **Real-time URL** — `ai_remove_background` in a delivery URL (nothing stored).
  2. **Remove and save** — apply the background-removal extension and upload the result as a new file version (a media-library operation, not this tool).
- Only use `ai_change_background` when they want a **new** background scene. For a plain transparent cut-out or a solid color, use `ai_remove_background` (optionally followed by `background`=a color).

## Handling failures

1. **400 / Bad Request or validation error**: refine the query and retry, passing the error text as `previous_errors`. Invoke the `search-docs` skill and call `search_docs` to confirm supported parameters/limits.
2. **3+ failures**: use `search-docs` to find supported methods and constraints before retrying.
3. **Unsupported**: confirm via docs and offer the closest supported alternative.

## Gotchas

- Source URL must be ImageKit-hosted.
- Background removal order matters (upscale/retouch first).
- Generative fill = `background`=`genfill` on a padded/enlarged canvas; it takes no prompt. `ai_change_background` is the prompt-driven one.
- `ai_drop_shadow` needs a transparent subject (run `ai_remove_background` first).
- Negative offsets/rotation are written with an `N` prefix in the final URL (the tool handles this) — just describe the value normally.

---

## Parameter reference

These are the real names/values the tool validates. Put them into your query.

### Resize & crop

| Parameter | What it does |
|---|---|
| `width` | Output width. Integer px, decimal 0–1 (fraction of original), or an arithmetic expression. |
| `height` | Output height. Same formats as `width`. |
| `aspect_ratio` | Aspect ratio (e.g. `16-9`). Use with `width` **or** `height`; ignored if both are set. |
| `crop` | Resize strategy: `force`, `at_max`, `at_max_enlarge`, `at_least`, `maintain_ratio`, `maintain_ratio_no_enlarge`. |
| `crop_mode` | Pad/extract behavior: `pad_resize`, `extract`, `pad_extract`, `pad_resize_no_enlarge`, `pad_extract_no_shrink`. |
| `focus` | Focal point: `auto`, `face`, `custom`, a directional position (`center`, `top`, `left`, `bottom_right`, …), or an object name (COCO class such as `person`, `car`, `dog`). |
| `zoom` | Zoom factor around the focused area (with face/object focus). |
| `x`, `y`, `x_center`, `y_center` | Region coordinates for `extract` crops (top-left vs center-based). |
| `dpr` | Device pixel ratio (number or `auto`) for high-density displays. |
| `background` | Fill for padded areas — see Background modes. |

### Background modes (`background`)

| Value | Meaning |
|---|---|
| a color | Hex (`FFFFFF`) or CSS name (`white`, `red`, …). |
| `blurred` | Blurred version of the image (optionally `blurred_<intensity>_<brightness>`). |
| `dominant` | The image's dominant color. |
| `genfill` | AI generative fill of the padded area (outpainting). No prompt. |
| `gradient` | Gradient from dominant colors (`gradient_dominant`, optional palette size 2 or 4). |

### AI transforms

| Parameter | What it does |
|---|---|
| `ai_remove_background` | ImageKit-native background removal → transparent. |
| `ai_remove_background_external` | Background removal via external provider (remove.bg). |
| `ai_edit` | Prompt-based AI edit of image content. |
| `ai_change_background` | Prompt-based replacement of the background scene (subject preserved). |
| `ai_drop_shadow` | AI drop shadow (transparent images only). Optional `azimuth` (0–360), `elevation` (0–90), `strength` (0–100). |
| `ai_upscale` | AI super-resolution upscaling. No params. |
| `ai_retouch` | AI quality enhancement / blemish removal. No params. |
| `ai_variation` | Generate a structural variation of the image. No params. |

### Effects & enhancement

| Parameter | What it does |
|---|---|
| `blur` | Gaussian blur, 0–100. |
| `sharpen` | Sharpen, 0–100. |
| `unsharp_mask` | Advanced sharpening (`radius`, `sigma`, `amount`, `threshold`). |
| `grayscale` | Convert to grayscale. |
| `contrast_stretch` | Auto-enhance contrast. |
| `shadow` | Drop shadow under non-transparent pixels (needs transparency). Optional `blur`, `saturation`, `x_offset`, `y_offset`. |
| `gradient` | Linear gradient overlay (`linear_direction`, `from_color`, `to_color`, `stop_point`). |
| `color_replace` | Replace a color and similar shades: `to_color`, `tolerance` (0–100), optional `from_color`. |
| `colorize` | Tint the image: `color`, `intensity` (0–100). |
| `border` | Border of `border_width` and `color`. |
| `trim` | Trim solid edges around the subject. |
| `rotation` | Rotate by degrees (or `auto` from EXIF). Negative = counter-clockwise. |
| `flip` | `h`, `v`, `h_v`, or `v_h`. |
| `radius` | Round corners (integer, `max` for a circle, or per-corner `20_40_80_160`). |
| `opacity` | Layer opacity, 0–100. |
| `distort` | Perspective warp (4 coordinate pairs) or arc distortion (degrees). |

### Overlays (`overlay`)

One `overlay` concept with a typed shape. Each overlay supports `position` (`x`, `y`, `x_center`, `y_center`, `focus`, `anchor_point`), `timing` for video (`start`, `end`, `duration`), `layer_mode` (`multiply`, `cutter`, `cutout`, `displace`), and a nested `transformation` list.

| Overlay type | Key fields |
|---|---|
| Text | `text`, plus styling: `font_size`, `font_family`, `font_color`, `inner_alignment`, `padding`, `alpha` (1–9), `typography`, `line_height`, `radius`, `rotation`, `flip`, `background`. |
| Image | `input` (media-library path of the overlay image); nested transformations allowed. |
| Video | `input` (video path); nested transformations + timing. |
| Subtitle | `input` (subtitle file); styling: `font_size`, `font_family`, `color`, `typography`, `font_outline`, `font_shadow`, `background`. |
| Solid color | `color`, plus `width`, `height`, `radius`, `alpha`, `background`, `gradient`. |

### Video transforms

| Parameter | What it does |
|---|---|
| `start_offset`, `end_offset`, `duration` | Trim the clip (seconds or arithmetic expressions). |
| `audio_codec` | `aac`, `opus`, or `none` (to mute/strip). |
| `video_codec` | `h264`, `vp9`, `av1`, or `none`. |
| `streaming_resolutions` | Adaptive-bitrate ladder, e.g. `[360, 720, 1080]`. |
| `rotation`, `radius`, `border`, `flip` | Same as image effects, applied to the video frame. |

### Output & delivery

| Parameter | What it does |
|---|---|
| `format` | `auto`, `webp`, `avif`, `jpg`, `png`, `gif`, `mp4`, `webm`, `orig`, … |
| `quality` | 0–100. |
| `progressive` | Progressive JPEG. |
| `lossless` | Lossless WebP/PNG. |
| `named` | Apply a saved named transformation. |
| `default_image` | Fallback image if the source is missing. |

### Conditionals

Transformations can be conditional on image properties (e.g. width/height/aspect ratio) — describe the condition in plain language ("if width > 1000, then …") and the tool builds the `if`/`if-else`/`if-end` chain.
