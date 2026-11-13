# Reference tools

`verify_assets.py` checks the delivered file hashes and source-kit integrity using only Python's standard library. It reads local files and does not call external services.

`reference-generators/` preserves the production scripts used to author the collections. They are included for developer reference. Their original `/workspace/work` build paths and export orchestration need configuration for another environment; they are not presented as a one-command portable build pipeline.

The production environment used Python, Pillow, python-docx, ReportLab, PyMuPDF, lxml, Inkscape, and DejaVu Sans. Inkscape rendered SVGs to PNG/PDF. Some background artwork was generated separately; the delivered background PNGs are included with the neon collection. Scope's final high-resolution PNG export substitution is documented in the neon asset manifest and independent QA report; its SVG masters retain the original source SVG.

Use the checked-in exported assets and manifests as the review baseline when adapting the scripts. Preserve source-logo geometry, colors, lettering, aspect ratios, and source hashes.
