---
name: transformation-builder
description: "MANDATORY PRE-STEP: You MUST read and follow this skill BEFORE calling the `transformation_builder` tool. This skill teaches you how to identify the correct ImageKit capability, craft precise queries, and handle multi-step transformations. Covers AI editing (change objects, colors, styles), background removal/replacement, generative fill, upscaling, retouching, resize, crop, overlays, text overlays, blur, sharpen, rotate, borders, shadows, color replace, and all visual modifications. Never call the transformation_builder MCP tool without first consulting this skill."
---

# Transformation Builder Skill

## IMPORTANT: Read This BEFORE Calling the Tool

This skill MUST be invoked and read before you call `transformation_builder`. It contains critical instructions for identifying the right capability, crafting precise queries, and ordering multi-step transformations that determine whether the tool produces correct results.

**Workflow:**
1. Agent reads this skill (you are here)
2. Agent identifies the correct capability using the Intent → Capability Mapping below
3. Agent crafts a precise query using the Query Crafting Guide
4. Agent calls `transformation_builder` with the prepared query
5. Agent handles results or failures following the rules below

## When to use (triggers this skill)
- User requests resize, crop, or focus on specific areas
- User wants filters, overlays, or visual effects
- User describes multi-step transformation chains
- User needs background removal (especially with upscaling)
- User wants AI-powered image editing of any kind

## Background Removal: Clarify Intent

When user says "remove background" without specifying the approach, **ask which option they prefer**:

1. **Real-time URL transformation** — Applies `e-bgremove` via transformation URL. Best for on-the-fly delivery, no new file stored.
2. **Remove and upload** — Applies background removal extension and uploads the result to DAM as new file version.

## Change background to something else: Clarify Intent

Only apply `ai_changebg` if the user wants to replace the background with a new scene or design. If they just want to remove the background and change color or keep it transparent, use or `ai_remove_background` or `ai_removedotbg` instead.

## Critical: Background Removal Sequence

**ALWAYS apply background removal AFTER upscale/retouch, NEVER before.**

Correct: `Upscale -> Then remove background`
Wrong: `Remove background -> Then upscale`

Use `e-bgremove` (not `ai_remove_background`) for background removal.

## Calling `transformation_builder`

After reading this skill and preparing your query, call the tool with:
- `query`: The precise, rewritten query (see Query Crafting Guide below — NEVER pass vague user input directly)
- `src`: Optional source URL (defaults to sample image)

**Chain transformations**: Frame multi-step requests as a single query.
- User: "1) Resize to 800x600 2) Crop to face"
- Query: "Resize to 800x600, then crop to focus on face"

## Query Routing & Crafting Guide

Users describe what they want in vague, everyday language. Your job is to **identify the right IK capability** and **rewrite the query** into a precise, tool-friendly description. Never pass vague queries through as-is.

### Intent → Capability Mapping

Use this table to decide which capability handles the user's request:

| User Intent (vague) | Maps To | Why |
|---|---|---|
| "Make the red balls green", "enlarge the cat", "remove the car", "add sunglasses" | `ai_edit` | Modifying **specific objects or regions** within the image requires AI content editing |
| "Put this on a beach", "change background to sunset", "make it look like they're in Paris" | `ai_changebg` | Replacing the **background scene** while keeping the subject. Adds new scene elements defined by prompt. Should not be used for simple background removal or color changes. |
| "Remove the background", "make it transparent", "cut out the person" | `ai_remove_background` | Removing the background entirely (transparent output) |
| "Make it wider without stretching", "extend the sky", "add more space on the left" | `ai_bg_genfill` | Expanding the image canvas with **AI-generated content** beyond original bounds |
| "Make it higher resolution", "it's blurry can you fix it", "enhance quality" | `ai_upscale` | Increasing resolution / fixing low-res images |
| "Clean up this photo", "remove blemishes", "fix skin imperfections" | `ai_retouch` | General visual quality improvement and artifact removal |
| "Add a realistic shadow", "make the product look like it's on a surface" | `ai_drop_shadow` | Adding natural-looking shadows (transparent images only) |
| "Create a variation", "give me a different version", "remix this image" | `ai_genvar` | Generating visual variations while preserving structure |
| "Generate an image of a sunset over mountains" | `ai_gen_image` | Creating a brand new image from text (no source image needed) |
| "Make it 800x600", "resize for Instagram", "make it smaller", "crop to 16:9" | `resize_and_crop` | Changing overall **dimensions, aspect ratio, or crop** of the image |
| "Focus on the face", "crop around the product", "zoom into the subject" | `resize_and_crop` (with `focus`) | Smart cropping using face/object detection |
| "Change all red pixels to blue", "swap the background color from white to gray" | `color_replace` (effects) | Global **pixel-level color swap** across the entire image |
| "Make it black and white", "blur it", "sharpen", "rotate 90°", "add a border" | `effects_and_enhancement` | Standard image filters and adjustments |
| "Add my logo on top", "put a watermark", "overlay this badge" | `image_overlay` | Compositing another image on top |
| "Write 'SALE 50% OFF' on the image", "add a caption" | `text_overlay` | Rendering text on the image |

### Key Distinction: `ai_edit` vs `color_replace` vs `ai_changebg`

These three are commonly confused. Use this decision tree:

1. **Is the user changing specific objects/regions?** (e.g. "make the balls bigger", "turn the car red") → **`ai_edit`**
2. **Is the user swapping a color globally across all pixels?** (e.g. "replace all #FF0000 with #00FF00") → **`color_replace`**
3. **Is the user replacing the entire background scene?** (e.g. "put them on a beach") → **`ai_changebg`**

### How to Craft Good Queries

**Rule: Always rewrite the user's vague request into a query that references actual IK parameters and capabilities. Use parameter names when you know them; fall back to descriptive English only when the exact parameter is unclear.**

| User Says | Bad Query (don't do this) | Good Query |
|---|---|---|
| "Make the red balls bigger and the blue ones green" | "make red balls bigger and blue balls green" | "Apply `ai_edit` with prompt: increase the size of the red-colored balls and change the blue-colored balls to green" |
| "Can you clean this up and put it on a white background?" | "clean up and white background" | "Apply `ai_retouch`, then `ai_remove_background`, then `ai_changebg` with prompt: solid white background" |
| "I want this to look like a painting" | "make it look like a painting" | "Apply `ai_edit` with prompt: transform into an oil painting style with visible brush strokes and artistic texture" |
| "Crop around the person's face" | "crop face" | "Apply `resize_and_crop` with `focus` set to `face` to crop around the detected face" |
| "Add some text saying Hello World at the bottom" | "add hello world text" | "Apply `text_overlay` with `text`='Hello World', `layer_y`=bottom, `layer_focus`=bottom" |
| "Make this fit for a mobile banner" | "mobile banner" | "Apply `resize_and_crop` with `width`=640, `aspect_ratio`=2-1" |
| "The background is boring, make it interesting" | "change background" | "Apply `ai_changebg` with prompt: vibrant gradient studio backdrop" |
| "Extend the image to make it panoramic" | "make panoramic" | "Apply `ai_bg_genfill` to extend image horizontally with `aspect_ratio`=3-1" |
| "This is too low quality" | "fix quality" | "Apply `ai_upscale`, then `ai_retouch`" |
| "Make it 300px wide and add a red border" | "resize and border" | "Apply `resize_and_crop` with `width`=300, then apply `border` with color red and width 5" |
| "Blur everything and put white text on top" | "blur and text" | "Apply `blur`=10, then `text_overlay` with `text`='Your Text', `color`=white, `font_size`=40, `layer_focus`=center" |
| "Remove background and add a drop shadow" | "remove bg shadow" | "Apply `ai_remove_background`, then `ai_drop_shadow`" |

### Multi-Step Query Chaining

When the user's request involves multiple capabilities, **chain them in one query in the correct order**:

1. **Upscale / Retouch first** (quality improvements)
2. **AI edits** (content changes) 
3. **Background removal / change** (always after content edits)
4. **Resize / Crop** (final dimensions)
5. **Effects / Overlays** (finishing touches)

Example: User says "clean up this photo, remove the background, and make it 500x500"
→ Query: "Apply `ai_retouch`, then `ai_remove_background`, then `resize_and_crop` with `width`=500, `height`=500"

## Handling Failures

1. **400 / Bad Request**: Invoke the `search-docs` skill first, then call `search_docs` for parameters/limits
2. **Multiple failures (3+)**: Invoke `search-docs` skill, then call `search_docs` to find supported methods and constraints
3. **Unsupported**: Search docs to confirm, offer alternatives if available

## Gotchas

- Background removal order matters: upscale/retouch first
- Source URL must be ImageKit-hosted

## IK Transformation Parameters Reference

### Resize & Crop (`resize_and_crop`)

| IK Parameter | What It Does |
|---|---|
| `width` | Output width. If only width is provided, height auto-scales to preserve aspect ratio. Accepts integer (px), decimal 0–1 (percentage), or arithmetic expression. |
| `height` | Output height. If only height is provided, width auto-scales to preserve aspect ratio. Accepts integer (px), decimal 0–1 (percentage), or arithmetic expression. |
| `aspect_ratio` | Sets aspect ratio (width:height). Must be used with either width or height; ignored if both are provided. |
| `crop_mode` | Controls resize/crop behavior: `pad_resize` (fit within dimensions with padding), `extract` (extract fixed region), `pad_extract` (padded extract). |
| `crop` | Controls crop strategy: `force` (exact resize, ignores aspect ratio), `at_max_enlarge` (resize at max without enlarging), `at_least` (cover minimum dimensions), `maintain_ratio` (preserve ratio). |
| `focus` | Focal point for cropping. Values: `custom` (predefined area), `auto` (smart crop), `face` (face detection), or an object name for object detection. |
| `zoom` | Controls zoom level around the focused area during face/object-based cropping. |
| `x`, `y`, `x_center`, `y_center` | Coordinates for `cm_extract`: `x`/`y` set top-left corner; `x_center`/`y_center` set center of extracted region. |
| `dpr` | Device pixel ratio — scales output dimensions for high-DPR displays (e.g. Retina). |
| `background` | Background color for padded areas. Supports hex, named colors, blurred background, and dominant color modes. |

### AI Transforms (`ai_transform`)

| IK Parameter | What It Does |
|---|---|
| `ai_remove_background_external` | Removes image background using external AI provider (remove.bg), producing transparent background. |
| `ai_remove_background` | Removes image background using ImageKit native AI, producing transparent background. |
| `ai_drop_shadow` | Adds AI-generated drop shadow around main subject. Controls: light direction, elevation, shadow intensity. Works on transparent images only. |
| `ai_changebg` | Changes image background using a text prompt while preserving the foreground subject. Supports plain text and base64-encoded prompts. |
| `ai_edit` | Edits/modifies image content using a descriptive text prompt with AI-driven visual changes. |
| `ai_bg_genfill` | Extends image beyond original boundaries by generating new background content using AI (generative fill / outpainting). |
| `ai_gen_image` | Generates a new image from a text prompt using AI and stores it at a specified file path. |
| `ai_genvar` | Generates AI-based visual variations of an existing image while preserving overall structure and composition. |
| `ai_retouch` | Improves visual quality using AI — enhances details and corrects imperfections. No additional parameters. |
| `ai_upscale` | Increases image resolution using AI super-resolution upscaling. No additional parameters. |

### Image Overlay (`image_overlay`)

| IK Parameter | What It Does |
|---|---|
| `image_path` | Path of the overlay image from ImageKit media library. Can also specify a solid color for color block overlays. |
| `encoded` | Whether to base64-encode the image path. |
| `layer_x` | Horizontal position of the overlay relative to the base image. Supports arithmetic expressions and negative offsets. |
| `layer_y` | Vertical position of the overlay relative to the base image. Supports arithmetic expressions and negative offsets. |
| `height` | Height of the overlay image. |
| `width` | Width of the overlay image. |
| `crop_mode` | Controls padding vs extraction behavior for the overlay. |
| `background` | Background color for padded areas of the overlay. |
| `layer_focus` | Positions the overlay relative to its parent container (e.g. center, top_left, bottom_right). |
| `layer_mode` | Blending mode: `multiply` (darken blend), `cutout` (cut transparent regions), `cutter` (mask base using overlay shape). |
| `effects.grayscale` | Converts overlay to grayscale. |
| `effects.border` | Adds border around the overlay. |
| `effects.trim` | Auto-trims transparent edges of overlay. |
| `effects.zoom` | Zooms into cropped region of overlay. |
| `x`, `y`, `xc`, `yc` | Defines exact crop region using absolute or center-based coordinates. |

### Text Overlay (`text_overlay`)

| IK Parameter | What It Does |
|---|---|
| `text` | The text string to overlay on the image. |
| `layer_x`, `layer_y` | Horizontal and vertical position of the text layer relative to the base image. |
| `width` | Maximum width of the text box. Text wraps automatically when exceeded. |
| `font_size` | Font size of the overlaid text. Supports numbers and arithmetic expressions. |
| `color` | Text color. Supports named colors, RGB hex, and RGBA hex with opacity. |
| `inner_alignment` | Horizontal alignment of text within the text box. |
| `padding` | Space around the text inside its background box. |
| `alpha` | Transparency of the entire text layer. |
| `typography` | Typographic styling: bold, italic, strikethrough, or combinations. |
| `font_family` | Font used to render the text. |
| `line_height` | Spacing between lines when text wraps across multiple lines. |
| `flip` | Flips or mirrors the text layer horizontally/vertically. |
| `layer_mode` | Blending mode for text: `multiply`, `cutout`, or `cutter`. |

### Effects & Enhancement (`effects_and_enhancement`)

| IK Parameter | What It Does |
|---|---|
| `contrast` | Auto-enhances contrast by stretching pixel intensity to full range. |
| `sharpen` | Basic sharpening. Excessive values may cause artifacts. |
| `unsharp_mask` | Advanced sharpening via Unsharp Masking (USM) with better perceptual quality. |
| `shadow` | Adds drop shadow beneath non-transparent pixels (requires transparent background). |
| `gradient` | Applies linear gradient overlay/background with configurable colors, direction, and stop point. |
| `grayscale` | Converts image to grayscale. |
| `perspective_distort` | Distorts image perspective using custom coordinates. |
| `arc_distort` | Curves the image upward or downward. |
| `trim` | Removes solid/near-solid background pixels around a central object. |
| `blur` | Applies Gaussian blur with configurable intensity. |
| `border` | Adds border with specified width and color around the image. |
| `rotate` | Rotates image clockwise/counter-clockwise or auto-rotates using EXIF data. |
| `flip` | Mirrors image horizontally, vertically, or both. |
| `radius` | Rounds image corners; max value produces a fully circular image. |
| `color_replace` | Replaces a source color and similar shades with a target color, preserving luminosity. |

### Video Transforms (`video_transforms`)

| IK Parameter | What It Does |
|---|---|
| `radius` | Rounds video corners. Use max for circular/oval clipping. |
| `rotate` | Rotates video clockwise by a fixed degree. |
| `mute_audio` | Mutes the video audio track. |
| `extract_audio` | Extracts audio track and outputs as audio-only file. |
| `border` | Adds border around the video frame with configurable width and color. |
| `trim_video` | Trims video using `start_time`, `end_time`, and `duration` parameters. Supports arithmetic expressions. |

### Video Overlay (`video_overlay`)

| IK Parameter | What It Does |
|---|---|
| `image_path` | Path of image to overlay on video. Supports base64-encoded paths via `encoded`. |
| `text` | Text string to overlay on video. |
| `video_path` | Path of video to overlay on base video. |
| `background` | Solid color for color block overlays on video. Supports named colors, RGB hex, RGBA hex. |
| `subtitle_path` | Path to subtitle file for subtitle overlays. |
| `layer_x`, `layer_y` | Position of any overlay (image/text/video/solid) relative to the base video. |
| `layer_focus` | Aligns overlay relative to base video frame (e.g. center, top_left). |
| `start`, `end`, `duration` | Controls overlay timing — when it appears, disappears, and how long it stays visible. |
| `color` | Text color for text overlays. Supports named colors, RGB hex, RGBA hex. |
| `font_size` | Font size for text overlays. Supports numbers and arithmetic expressions. |
| `typography` | Typography style for text overlays. |