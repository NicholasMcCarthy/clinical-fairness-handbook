# Build and review record

Edition: 5 November 2026.

## Completed

- Rendered the complete 22-document Quarto book to HTML and EPUB with Quarto 1.11.9.
- Used the official portable Windows release; its SHA-256 matched the digest supplied by the official release API: `eda220a2f39c392f622049de013ddf7b4dfdf019ba877f251be14ce43e5734d1`.
- Checked registration of all chapters and appendices, 51 bibliography entries, citation and cross-reference targets, and all 15 placeholder/brief pairs.
- Checked local links and fragment targets in the rendered HTML, including the EPUB download.
- Checked EPUB archive integrity and XML package documents.
- Checked confusion-table arithmetic, stated sensitivity and specificity, predictive values, selection rates, and the main conformal order-statistic examples.
- Checked the documented CFT `report` and `validate-config` command interfaces against the installed toolkit help.
- Preserved source commits and file hashes in `manifest.json`. No clinical experiments were run.

## Review limits

The automated checks are not a methodological or clinical peer review. A browser visual check could not be completed: isolated command-line browser launches did not produce screenshots, and the browser tool rejected local `file:` navigation under its URL policy. No browser-security workaround was used after that rejection.

The HTML and EPUB build successfully, but final visual inspection in a local browser and an EPUB reader remains an editorial check. In particular, inspect long equations, wide tables, dark-theme contrast, mobile navigation, search, and EPUB-reader mathematical support. The stylesheet permits horizontal scrolling for long equations and tables.

Illustrations remain deliberate textual placeholders. The source-notes appendix records the broader editorial scope and limitations.
