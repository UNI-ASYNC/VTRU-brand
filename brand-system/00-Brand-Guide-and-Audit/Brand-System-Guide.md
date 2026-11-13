# Vitruveo ecosystem brand system

Production edition 1.0 · prepared 13 November 2026

A coordinated set of layouts built around five distinct, user-supplied brand identities. The supplied ZIP artwork is the source of truth for the marks. The visual system adds typography, spacing, backgrounds, and communication templates; those additions are production recommendations, not pre-existing official brand standards.

## Review status

The source audit passed. All supplied artwork is source-matched to the uploaded archives, and the package contains new derivative layouts. Editorial and brand-owner approval has not been asserted. Review proposed headlines, layout choices, and placeholders before publication. No legal ownership certification is provided.

## Five brand families

### Vitruveo

Role used in this system: Network and infrastructure identity. These role labels are based on the supplied plan and are descriptive.

Source family: `vitruveo-*.svg` and matching PNG files in `vitruveo-brandkit.zip`. Full logo for named communications; supplied logomark for compact identity where available.

Source-derived colors (rounded sRGB): `#FF00FF` gradient stop, `#00FFFF` gradient stop, `#000000` primary lettering.

Proposed template colors: accent `#7B64F5`, secondary `#39BEEB`, dark ink `#19162E`, pale field `#F4F1FC`. These colors support the new layouts; they do not recolor the protected logo.

### Vertical Foundation

Role used in this system: Foundation and community identity. These role labels are based on the supplied plan and are descriptive.

Source family: `verticalfoundation-*.svg` and matching PNG files in `verticalfoundation-brandkit.zip`. Full logo for named communications; supplied logomark for compact identity where available.

Source-derived colors (rounded sRGB): `#C2D3C7` architecture, `#949F9C` architecture, `#7C8280` architecture, `#D5E2D8` architecture, `#B5A88C` lettering.

Proposed template colors: accent `#7C827F`, secondary `#B5A88C`, dark ink `#293A34`, pale field `#F2F5F0`. These colors support the new layouts; they do not recolor the protected logo.

### Pretrend

Role used in this system: Trend and prediction identity. These role labels are based on the supplied plan and are descriptive.

Source family: `pretrend-*.svg` and matching PNG files in `pretrend-brandkit.zip`. Full logo for named communications; supplied logomark for compact identity where available.

Source-derived colors (rounded sRGB): `#7ABE4D` gradient endpoint, `#0057D6` gradient endpoint, `#0B82BE` gradient endpoint, `#A5D03F` gradient endpoint, `#000000` lettering.

Proposed template colors: accent `#0056BB`, secondary `#7AC543`, dark ink `#102C37`, pale field `#F0F7F4`. These colors support the new layouts; they do not recolor the protected logo.

### AI Wars

Role used in this system: Gaming and competition identity. These role labels are based on the supplied plan and are descriptive.

Source family: `aiwars-*.svg` and matching PNG files in `aiwars-brandkit.zip`. Full logo for named communications; supplied logomark for compact identity where available.

Source-derived colors (rounded sRGB): `#060B14` primary lettering, `#0B5CFF` slash accent.

Proposed template colors: accent `#0B5CFF`, secondary `#A3C5FF`, dark ink `#060B14`, pale field `#F0F4FF`. These colors support the new layouts; they do not recolor the protected logo.

### VTRU Scope

Role used in this system: Ecosystem discovery and intelligence identity. These role labels are based on the supplied plan and are descriptive.

Source family: `vtruscope-*.svg` and matching PNG files in `vtruscope-brandkit.zip`. Full logo for named communications; supplied logomark for compact identity where available.

Source-derived colors (rounded sRGB): `#FF00FF` gradient stop, `#00FFFF` gradient stop, `#000000` primary lettering, `#FFFFFF` target detail.

Proposed template colors: accent `#8D5CF5`, secondary `#22BCEB`, dark ink `#1B1835`, pale field `#F4F2FC`. These colors support the new layouts; they do not recolor the protected logo.

## Artwork rules

- Embed the exact supplied SVG or PNG. Keep paths, gradients, lettering, transparent negative spaces, and the original aspect ratio.
- Scale uniformly. Do not stretch, rotate, redraw, recolor, outline, add effects to, or crop the mark. Decorative lines, charts, and status glyphs remain separate from it.
- Start with clear space equal to at least one quarter of the visible logo height, then increase it where composition allows. This is a proposed layout rule, not a source-defined official requirement.
- Use the primary full-color source on a light field. Use a supplied white variant on a dark field. A filename alone does not establish contrast suitability: inspect its rendered appearance.
- Keep the entire mark inside a crop-safe area. Profile files use padded 1024-square canvases; check the actual circular crop and upload preview in the destination account.
- New emoji symbols and sticker illustrations are supporting artwork. They must never be presented as replacement brand logos.

### Important source quirks

AI Wars has no separate compact icon in these archives. Its file named `aiwars-logomark.svg` is the full wordmark, with the same geometry and viewBox as its primary logo. Its circle and square variants place that wordmark in a square viewport; preserve it rather than inventing a letter symbol.

Vertical Foundation is taller than the other wordmarks, approximately 1.59:1. The full logo includes the name beneath the architecture; the separate logomark omits that name. Allocate enough height. Its `logo-dark.svg` is byte-identical to the primary logo; choose `logo-white.svg` when a white lockup is needed.

Vitruveo's circular symbol is built from six gradient-filled paths with transparent separators. Keep the original source geometry intact. Do not reconstruct a circle or fill its open spaces.

Across the source families, circle/square filenames describe viewports and spacing, not a guaranteed circular background. White SVG variants can contain unused gradient definitions; visible appearance, not a list of color tokens, determines how that variant looks.

## Typography and layout

DejaVu Sans is the proposed supporting typeface: bold for headlines, regular for body text and labels. It is independent of the outlined lettering in the logos, which remains unchanged. Use a clear title/body/metadata hierarchy and generous quiet space around the artwork. Font files are not bundled. If an editor lacks the font, substitute deliberately and review line breaks.

Each brand retains its own source colors and visual character. The shared system contributes consistent margins, label sizes, modular cards, and export standards. Shared ecosystem pieces use a neutral composition with each source mark intact.

## Asset formats and production targets

| Asset | Production target | Use |
| --- | --- | --- |
| Emoji | 128 × 128 transparent PNG, below 256 KB | 10 distinct static expressions per brand |
| Sticker | 320 × 320 transparent PNG, below 512 KB | 4 static expressions per brand |
| Letterhead | A4 portrait, 210 × 297 mm | 3 layouts per brand: formal, office, technical |
| Profile image | 1024 × 1024 PNG | Light, dark, and framed treatments |
| X banner | 1500 × 500 PNG | Profile header |
| Facebook cover | 1640 × 720 PNG | Cover production canvas |
| LinkedIn company cover | 1512 × 256 PNG | Company header |
| LinkedIn personal cover | 1584 × 396 PNG | Personal profile header |
| Discord banner | 960 × 540 PNG | Server-banner canvas |
| Website hero | 1920 × 640 PNG | Wide hero image |
| Square social | 1080 × 1080 PNG | Square post |
| Landscape social | 1200 × 630 PNG | Wide post |
| Story | 1080 × 1920 PNG | Vertical post |

These are the package's production targets. They are not a claim that every platform's current requirements, mobile crop, or account-specific placement has been independently verified. Review the live destination preview before uploading.

The social collection contains nine compositions per brand, plus three announcement templates and two document headers per brand. Editable SVG masters accompany the graphics. Header dimensions are recorded in the export manifest.

### Letterhead use

Each design has an editable DOCX, an A4 PDF, and a blank high-resolution PNG at approximately 300 dpi. The writing area remains clear. The PDF is an RGB print master with no bleed; commercial printing may require printer-specific color conversion. Do not claim PDF/X certification or CMYK separation. The DOCX keeps contact fields editable. Replace bracketed placeholders such as `[Email]` and `[Website]`; do not invent legal addresses, staff titles, or ownership statements.

The DOCX is an editable office layout. Word processors can reflow text or substitute fonts; inspect its print preview before sending. Use the supplied PDF when fixed placement matters.

### Social and announcement use

Edit the SVG to update content, then export a fresh PNG at the recorded dimensions. The PNG is a fixed rendering. Keep important content away from expected profile-picture overlays and the edge of the frame. A wide composition and a vertical composition use different arrangements, so avoid making one from an automatic crop of another.

Proposed headlines and descriptors are sample copy, not verified product promises. Review them editorially before publication. Bracketed fields in announcement masters must be replaced. Never publish placeholder text as finished communication.

## Ecosystem compositions

The original four-brand composition contains Vitruveo, Pretrend, AI Wars, and Vertical Foundation. VTRU Scope belongs in the separate five-brand ecosystem compositions. All five remain included in the complete package.

No previous promotional banner was supplied in this thread. The new four-brand banner is a fresh composition based on the actual source marks, rather than a pixel-specific correction of an unavailable original.

## Verification and provenance

Five archives supplied 70 assets: 35 SVGs and 35 PNGs, seven of each per brand. Archive CRC checks passed, all extracted-file hashes matched archive bytes, all SVGs parsed and rendered, and all PNGs decoded. No SVG script, event handler, foreignObject, or external reference was found.

Rendered SVGs were compared with their paired supplied PNGs at a 512-pixel width on white and dark fields. The largest mean absolute channel difference was 0.814 on a 0–255 scale, consistent with small rasterization differences. This numerical comparison supplements the source hash audit; it does not certify legal authorship or trademark rights.

`08-Manifests-and-Export-Checks/source-inventory.csv` records every supplied filename, source archive, format, byte size, SHA-256 hash, dimensions or viewBox, and structural details. `source-audit.json` contains the full audit, gradient stops, source notes, and SVG/PNG comparisons. The export manifest links derivative files to the source artwork used and records export checks.

A derivative layout combines exact supplied artwork with newly authored layout elements. A source match means the embedded artwork traces to those source bytes; it does not mean the complete derivative has received the brand owner's approval. The original ZIPs and unchanged standalone source artwork are not repackaged. Keep the uploaded originals as archival masters.

## Working workflow

1. Choose the brand folder and the destination format.
2. Open an editable SVG or DOCX, replace placeholders, and review proposed copy.
3. Preserve the embedded logo and its proportions; adjust only the supporting layout.
4. Export at the manifest dimensions and check transparency, edge spacing, and text size.
5. Preview the actual destination crop or print page, then publish the reviewed asset.
6. Keep the edited master and the exported file together for future updates.

The package is a reusable production system with recorded source provenance. Owner review remains appropriate for editorial choices and final placement; it is not a statement of legal ownership.
