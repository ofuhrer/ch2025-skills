# Validation record

Draft: 0.1.0. Date: 2 November 2026.

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
