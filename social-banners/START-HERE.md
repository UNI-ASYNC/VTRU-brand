# Neon Social Banner Pack

This set uses the exact brand artwork from your five supplied ZIP files. The Vitruveo, Pretrend, AI Wars, Vertical Foundation and VTRU Scope logo SVG bytes are embedded directly in the editable masters. Logo geometry, colors and lettering remain as supplied. The blue/purple/green atmospheric backgrounds are newly generated decorative art.

## Use the files

- Upload the PNG in the relevant platform folder.
- For editing, extract the entire ZIP and keep its folder structure. SVGs refer to the two shared background images in `00-Guide-and-Audit/Backgrounds/`; the original logos are embedded inside the SVGs. Template fonts and their license are included. Re-export a PNG after editing an SVG.
- `01-Ecosystem-Four-Brands` follows your example: Vitruveo, Pretrend, AI Wars and Vertical Foundation, with the example's “AI Blockchain”, “powered by” and “Now Featuring” copy.
- `02-Ecosystem-Five-Brands` adds VTRU Scope. Folders 03–07 contain each brand separately.
- The two `Master/reference-wide-master` designs are wide reference compositions at 2400 × 800.
- See `08-Previews/Neon-Social-Banners-Preview.pdf` for all designs and the YouTube center-crop previews.

## Sizes

| Platform / surface | PNG dimensions |
|---|---:|
| Facebook — Page cover | 1702 × 630 |
| Facebook — Alternate Page cover | 1640 × 720 |
| Facebook — Feed landscape | 1200 × 630 |
| X — Profile header | 1500 × 500 |
| YouTube — Channel banner | 2560 × 1440 |
| YouTube — Video thumbnail | 1280 × 720 |
| TikTok — Vertical content cover | 1080 × 1920 |
| Instagram — Square feed post | 1080 × 1080 |
| Instagram — Portrait feed post | 1080 × 1350 |
| Instagram — Story / Reel cover | 1080 × 1920 |
| Rumble — Channel backsplash | 3600 × 600 |

Instagram and TikTok files are content covers/feed/Story formats. They are not channel-header upload slots. On those services, select the image as an appropriate content cover or publish it in the corresponding post/Story format.

YouTube's full canvas is deliberately spacious: important logos and text sit in the centered 1544 × 422 production safe area for the narrow desktop/mobile crop. X keeps important content at least 60 px from the top and bottom and away from the lower-left profile area. Rumble exports are 3600 × 600 and below 2 MB. Platform UI crops can vary by account and device; check the upload preview before publishing. Facebook and Instagram sizes are production targets; their official documentation was access-blocked during this pass. Evidence and source URLs are recorded in `00-Guide-and-Audit/social-platform-specs.json`.

## Original artwork verification

The asset manifest maps each output master and PNG export to the exact supplied source filename and SHA-256. All embedded logo images were checked against extracted ZIP contents. No logo was redrawn or generated. All upload PNGs use the same matched layouts. For sharper raster output, VTRU Scope's PNG exports use its untouched supplied 2400 px PNG logo at the identical layout position; the editable masters retain the supplied SVG. Both source hashes are recorded. Background art and framing are new derivatives. The packet includes 79 compositions, each in PNG + editable SVG, plus previews and audit documentation. Original ZIP archives and standalone unchanged logo masters are excluded.
