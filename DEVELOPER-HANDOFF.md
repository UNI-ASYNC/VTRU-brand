# Gaps needing technical assistance

This developer handoff brings the source brand kits, produced assets, browseable image previews and website research together for collaborative review. Research was checked **13 November 2026**; this is an evidence date, not an implementation deadline. The items below describe observations and work that would benefit from technical assistance, with no attribution of blame.

Read the [research report](reports/RESEARCH-REPORT.md) and the repository image galleries before changing production sites. Original brand artwork is in `source-brand-kits/`; produced layouts are in `brand-system/` and `social-banners/`; downloadable packs are in `downloads/`.

## P0 — agree the facts used in public copy

| Work item | Acceptance criteria | Evidence |
| --- | --- | --- |
| Record current ecosystem roles and naming | A short approved description exists for Foundation, Vitruveo, Pretrend, Scope and AI Wars; it distinguishes organization, network, asset, application and program. Confirm the Scope/VTRU Scope editorial convention while preserving the supplied logo. Include VTRU, VIBE, HOST, VNS, bridges, Explorer and network metrics in the relationship map where relevant. | [Foundation](https://www.verticalfoundation.net/), [ecosystem](https://www.vitruveo.ai/ecosystem), [Scope About](https://scope.vitruveo.ai/info/about) |
| Reconcile Pretrend current-version/status copy | The product owner confirms the current version, market currency and availability statement. Market rulebooks, protocol, whitepaper and onboarding describe the same current model, with legacy material clearly dated. | [Pretrend report](reports/brand-research/pretrend-research.md), [whitepaper](https://www.pretrend.ai/whitepaper/), [market rulebook](https://www.pretrend.ai/markets/pumpfun-5/) |
| Reconcile AI Wars status | Roadmap, Mint and Genesis agree on what is open, delivered and planned. Copy separately identifies the main game, Trends interface and simulated feed. No campaign implies that simulated telemetry is a live main-game feed. | [AI Wars report](reports/brand-research/aiwars-research.md), [roadmap](https://www.epicaiwars.com/roadmap), [Mint](https://www.epicaiwars.com/mint), [Trends](https://www.epicaiwars.com/trends) |
| Preserve original marks in any deployment | Logos use the supplied SVG/PNG variants at their correct proportions; source hashes remain traceable. No protected geometry or lettering is recreated from a preview image. Existing public kit hashes match all five supplied ZIPs and all 70 members. | [Public-source comparison](reports/evidence/public-brandkit-comparison.json), [brand library](https://www.vitruveo.ai/ecosystem/brands) |

## P1 — improve existing site delivery

| Work item | Acceptance criteria | Evidence |
| --- | --- | --- |
| Pretrend share previews | Relevant published pages declare an approved, reachable image plus appropriate title/description for shared links. Check the resulting Facebook/X preview and cache behavior. Preserve any page-specific metadata. | [Pretrend](https://www.pretrend.ai/), [web asset audit](reports/evidence/web-asset-audit.json) |
| Scope share previews | Appropriate Facebook/X metadata is available to a link crawler from the published response. Verify title, description, absolute image URL and the resulting preview. Preserve existing client-rendered titles. | [Scope](https://scope.vitruveo.ai/), [Scope report](reports/brand-research/scope-research.md) |
| Foundation destination links | The owner confirms the preferred Foundation destination; ecosystem links use it consistently. Test both old HTTP/HTTPS addresses and their redirect behavior before retiring old links. VIBE CTA resolves to the intended current app route. | [Foundation report](reports/brand-research/foundation-research.md), [VIBE](https://scope.vitruveo.ai/assets/vibe) |
| Scope help discovery | The existing About/release-history page is reachable from current navigation. General FAQ navigation leads to useful current answers or another confirmed support destination. | [About](https://scope.vitruveo.ai/info/about), [FAQ route](https://scope.vitruveo.ai/faqers/general) |
| Confirm icon choices and coverage | Retain the existing favicons. Confirm whether Scope intentionally shares Vitruveo's icon. Check readability in light/dark browser tabs and retain the Foundation's existing declared Apple icon. Create only additional sizes/surfaces actually needed. | [Web asset audit](reports/evidence/web-asset-audit.json) |

## P2 — confirm the collateral inventory, then fill gaps

| Work item | Acceptance criteria |
| --- | --- |
| Public resource index | Existing brand kits, developer docs, whitepapers, product onboarding, contact/support and approved media have clear links. Resource owners identify obsolete destinations before replacements are authored. |
| Press/partner copy and deck | Locate any existing version first. If none is suitable, build current approved short descriptions, contact details and partner material using the P0 fact sheet and source artwork. |
| Email/newsletter templates | Confirm existing templates, sending systems and responsible owners. Create only missing templates, using verified contact fields and approved copy. |
| Internal UI/design library | Inventory current product components, typography and tokens. Extend existing components where possible and check accessibility in the actual product context. |
| Support and incident information | Locate existing help, escalation and incident/status resources before proposing a new platform. Existing network metrics should not be mistaken for incident history. |

## Review and verification

- Check visual exports at their intended size and in each platform's actual upload preview; current platform UI crops can vary.
- Keep the `social-banners/00-Guide-and-Audit/Backgrounds/` files beside their relative SVG references when moving editable neon masters.
- SVGs and DOCX files are editable masters. PNG/PDF files are presentation exports. Stationery PDFs are A4 RGB without bleed; DOCX structure was checked, but Word/LibreOffice rendering was not performed in the production environment.
- Separate owner confirmation of copy/status from technical checks that files render and links return the intended resource.
- Record the deployment date and link-check results when changes are actually shipped. This repository's research date does not mean the sites have already been changed.

The repository is a public review package. Publication does not establish copyright ownership, grant a new license to brand marks, or certify product/financial claims. Original marks remain attributable to their respective owners. Included font license notices must travel with the template fonts.
