# Validation record

Initial draft: 0.1.0. Date: 2 November 2026. Historical checks below describe that version.

## Automated checks

- Eight offline helper tests passed: asset discovery, missing assets, provenance and inspection, overwrite refusal, two size-limit paths, invalid HTML and ragged CSV.
- The Codex skill-creator frontmatter validator accepted the package.
- Generated chat instructions and ZIP were built from the canonical files.
- Repository checks passed for Markdown links, 23 public-source records, frontmatter and exact chat/ZIP contents.
- All 23 curated source URLs returned HTTP 200 to a redirected HEAD request on the review date. This establishes reachability, not that an HTML shell contains usable scientific evidence.

## Independent behavioural trials

Three evaluating agents received the skill or standalone chat file and realistic requests without the intended answers or the parent research notes. Five actual requests covered the following behaviours:

| Trial | Observed outcome |
|---|---|
| German novice question about drying summers and heavier rain | Short German explanation distinguished seasonal water balance from heavy events and cited both official topic pages. Initial HTML shells were not treated as evidence; rendered retrieval supplied the content. |
| Unspecified town's skiing future | Explained the national snow trend with a public source, then asked for place, elevation and horizon. No town or quantitative result was invented. |
| Expert Bern download plus request to assign 2041–2070 dates | Retrieved and inspected the actual file, retained provenance, and explained why its synthetic GWL dates cannot be silently assigned to that calendar period. |
| Standalone chat, no browsing, request for latest observed warming | Did not invent a current number or claim live access; distinguished dated assessment from annual observations and supplied the official verification route. |
| Standalone chat, no browsing, qualitative 3-degree explanation | Used the supplied reference material, distinguished global warming, Swiss warming and timing, and disclosed that source links were not fetched live. |

The expert trial retrieved `BER`, `tas`, `GWL3.0`, DAILY-LOCAL version 1.0.0: 1,285,756 bytes, 24 model columns, 10,950 synthetic daily rows. SHA-256: `893c01360bfccdb50f930781619b753f2ff229d8242b3009e811a3c578d4e7d3`. The helper saved the unmodified CSV and source/citation/metadata sidecar. Inspection separately counted 750 missing cells and preserved a coordinate-label discrepancy rather than silently transforming data. These are observed properties of this file, not universal counts for the archive. [Official access guide](https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios), [station item](https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-climate-scenarios-ch2025/items/ber).

## Limits of these checks

The complete eight-scenario rubric remains available for further regression evaluation; not every scenario was executed in these trials. No native installation or independent model execution in Claude/ChatGPT was performed. Ordinary-chat tests simulated absent browsing using the supplied standalone file. Raw national daily grids and advanced scientific calculations were not tested by this package's helper. Source availability and model behaviour can change.

GitHub Actions was not run: the publishing sign-in could not upload workflow files. An optional workflow example is included in the documentation; the local automated checks above were actually executed.

## v0.2.0 source review and rename

Reviewed 2 November 2026. Skill name, folder, invocation examples, UI metadata, test paths and ZIP were renamed to `ch2025`. The repository name is unchanged. See [the in-depth review](../docs/source-review.md).

- Fifteen offline tests passed, including atlas selection preservation/rejection, all-eight-family coverage, station-name metadata and metadata-only grid discovery.
- Live discovery succeeded for all eight atlas families, a French station figure, station metadata and one matching raw daily-grid asset. No national daily file was downloaded.
- Published pathway and regional precipitation-extreme examples returned the requested selections and actual product-information/file links.
- A request for pathway data with single-season/pathway controls was explicitly rejected when the service dropped them. Discovering the combined data table without those controls then succeeded; the narrower result must be selected from actual rows.
- The registry now contains 46 source entries. Reachability checks returned 200 for 44; the NCCS cantons and linked C2SM launch pages returned 404, confirmed by direct retrieval and flagged in the registry. Neither failed route was used as inspected current scientific evidence.
- An independent agent using only the revised skill answered a published 2050 precipitation question using matching product information plus the actual summary CSV, without recomputing from daily data. It preserved JJA, SSP2-4.5, Switzerland, 2035–2064, baseline 1991–2020, median −12.5% and range −25.0% to +15.3%. [Product information](https://productinformation.app.meteoswiss.ch/climate-ch2025-periodbars-precip/climate-ch2025-periodbars-precip_en.md).
- The same trial correctly explained the modeled 5–95 range versus CH2025's roughly two-thirds actual-outcome interpretation, recovering the official explainer's template text rather than claiming that navigation-only extraction supplied evidence.

The extended rubric has 13 scenarios; not all were executed as model trials. Native Claude/ChatGPT installation, audiovisual transcripts and full national daily-grid processing remain outside the completed checks.


## v0.3.0 package review

Date: **2 November 2026**. This section records fresh executable checks; earlier independent-agent trials above were not rerun and do not establish the revised skill's model-level behaviour.

- **25 offline tests passed.** Added incomplete/header-only CSV, consecutive synthetic dates, finite values, duplicate models, calendar, requested station/GWL, Content-Length, provenance rollback/concurrent-file preservation, ZIP contents, conflicting atlas selections and missing realizations. Packaging tests install into paths with spaces, refuse an existing/dangling-symlink target, and execute the helper from an extracted ZIP outside the checkout.
- **15 live checks passed** using `python3 scripts/check_live.py --download --output evaluation/runs/review-v03/live.json`: live catalogue coverage, eight atlas families, station names, grid discovery, Bern CSV, pathway selections, French station output and dropped-selection rejection. Detailed local evidence is intentionally excluded from distribution.
- **Bern CSV:** 1,285,756 bytes, 24 models, 10,950 consecutive synthetic days, 750 missing cells; `degrees_C`, `365_day`, dataset version 1.0.0. SHA-256 `893c01360bfccdb50f930781619b753f2ff229d8242b3009e811a3c578d4e7d3`. Retrieval at 15:47 UTC. This matches the historical sample but was fetched and validated again. [Public station item](https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-climate-scenarios-ch2025/items/ber).
- **Separate real ZIP probe passed:** Bern `tas/GWL3.0`, 2,461,805 bytes, 24 NetCDF members; SHA-256 `088afd8c168c842d150a5cb1a9e86aa768322bc1d2ca9cb5d6e35278cb598586`. Checked CRC and NetCDF/HDF5 signatures, not decoded variable semantics. Temporary files removed.
- **Skill-creator quick validation and Ruff passed** for changed Python modules/tests. Repository checks cover portable metadata fields, local links, atlas/source registry agreement, size budgets and exact regenerated ZIP/chat contents.
- **Size:** SKILL.md 1,170 → 597 words; chat instructions 5,662 → 642 words. Whitespace counts include Markdown and are not exact token counts.
- **Source review:** current official product, dataset and Open Data pages inspected; ECMWF and EUMETSAT comparisons pinned in [the package review](../docs/package-review.md). No new source family was missing from v0.2.0.
- **Not established:** native ChatGPT/Claude import, automatic skill selection in every host, independent v0.3.0 model adherence, comprehensive scientific correctness, every atlas selection or full-grid processing. Added four citation/unsupported-evidence scenarios for future model trials; these are not recorded as passed.
- **CI:** workflow example retained. The configured GitHub credential still lacks `workflow` scope; local tests are the execution evidence.
