# In-depth CH2025 source-use review

Review date: **2 November 2026**. Baseline: initial skill v0.1.0. Revised package: **v0.2.0, `ch2025`**. The GitHub repository remains `ofuhrer/ch2025-skills`.

## Assessment

The original skill had sound scientific boundaries and source-attribution rules, but **did not make optimal use of CH2025's published information**. It was strongest for general explanations and daily station data. Much of the richer material was merely listed, requiring an agent to rediscover the product choice or unnecessarily calculate a result already published by MeteoSwiss.

This review inspected the current official overview/product/atlas/explainer pages, all eight live atlas configurations, their product-information documents, daily-data documentation/catalogue, relevant scientific-report sections and supporting observation routes. A separate reviewing agent inspected the initial skill and public sources independently. Published evidence takes precedence over cached search text and historical planning material.

Primary website references: [CH2025 overview](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios.html), [reports/data/graphics](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios.html), [web atlas](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios/swiss-climate-scenarios-web-atlas.html), [interpretation guide](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/understanding-climate-change-scenarios.html), [Open Data guide](https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios).

## Findings and changes

| Priority | Finding in v0.1.0 | Why it matters | Change in v0.2.0 |
|---|---|---|---|
| High | Eight atlas families were named but lacked a decision guide or direct discovery workflow | A user could get a generic link or a daily-data calculation instead of the published answer | Added a question-to-product matrix, all eight official entry points, product-specific restrictions, live options/file discovery and examples |
| High | The short overview of weather/climate phenomena was missing from the source registry | Hail, fog, storms, radiation and fire-weather questions could be forced into the four headline themes or a broad report search | Registered the official overview, its confidence/process/observation/projection distinction and report-section routing |
| High | Calendar cautions were stronger than the routing to published time-horizon products | An agent could correctly reject synthetic-date relabelling yet miss a valid temperature/precipitation summary around 2050 | Added the SSP/time-period product and exact 30-year windows, while preserving the prohibition on inventing dated daily forcing |
| Medium | Generic percentile cautions omitted CH2025's explicit uncertainty interpretation | An answer might stop at “not a calibrated probability” without explaining the published assessment | Added the roughly two-thirds/66% “likely” interpretation of the 5–95 model range, with report Section 2.11 and source-specific qualifications |
| Medium | Observed-climate questions had only generic home/catalogue links | Current trends, records, normals and historical series require distinct sources | Added Climate Monitor, observed records/indices, homogeneous station series, spatial analyses and station/gridded normals |
| Medium | Local/cantonal and source-generation checks were implicit | A CH2018 fact sheet, station value and CH2025 canton average are different things | Added explicit generation/baseline checks, station/altitude/map routing and an availability caveat for NCCS |
| Medium | Browser/PDF fallback was documented, but template text extraction was not | The official pages often appear as navigation-only shells to text tools despite containing their prose in templates | Added template/shadow-root extraction as a lightweight fallback, requiring recovered content verification |
| Lower | Video/launch/print media were absent from task routing | Novice/teaching users benefit from an appropriate medium | Added official introductory/launch routes and language-aware brochure guidance; recordings are not treated as inspected evidence without inspection |

The revised core remains short; detailed choice guidance is in [the product reference](../skills/ch2025/references/products.md). A source registry is a discovery aid, not proof that each link supports an arbitrary claim.

## Coverage against the website's product overview

| Official information channel | Revised use |
|---|---|
| Public topic pages and brochure | First explanation, language-specific introduction and printable material |
| Introductory video | Optional audiovisual learning; source text/data remain available for precise claims |
| Scientific report | Methods, detailed findings, uncertainty, processes and limitations; full report distinguished from summary/contents PDF |
| Phenomena overview | Fast route to evidence strength and report sections beyond the four headline messages |
| Web atlas and associated data | Preferred route for a published number/plot, selected by the question rather than visual style |
| Daily datasets | Bounded input-data workflows, current metadata and suitability checks; not the default for every numerical question |
| Launch presentations/discussion | Teaching/background material with time/version context |
| Previous scenarios | Historical/method comparisons with generation and baseline reconciliation |
| Current specialist guides | Indicator definitions, ensemble sub-selection, extreme-precipitation guidance and hydrological extensions |
| Supporting official observations/adaptation | Separate evidence for current measured climate, planning recommendations and impacts |

This is a product-class coverage review, not a claim that every individual graphic, file, talk or sectoral question has been tested.

## All eight atlas families are different evidence routes

| Family | Distinct use now captured |
|---|---|
| Maps | Spatial patterns; observations versus GWL; aggregate gridded downloads |
| Altitude levels | Regionally averaged elevation bands; not precise site/piste predictions |
| Indicators at stations | Broad indicator set, including urban heat, fire weather, growing season and heating/cooling indices |
| Seasonal changes | Raw EURO-CORDEX regional change signals, including 1/3/5-day precipitation return-level changes over 5–100-year return periods |
| GWL comparisons | Regional temperature/precipitation and zero-degree-line changes; baseline restrictions |
| Emission-scenario/time comparisons | SSP1-2.6/2-4.5/5-8.5 and 30-year periods centred on 2040/2050/2060 |
| Climate charts | Typical station annual cycle; the documented mm/day ×30 precipitation convention |
| Ensemble selection | Selected-member tables by case/region, rankings, boxplots and CCS-by-GWL diagnostics; guide plus actual model identities |

See [the official atlas](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios/swiss-climate-scenarios-web-atlas.html) and the product-information link returned by each live display. The new helper discovers current controls and file/share links; it rejects dropped/substituted requested selections. It does not promise that an observed implementation API is a stable public contract.

## Important source caveats

- **Uncertainty:** Section 2.11 of the [scientific report](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/) distinguishes a 90% modeled range from the assessment's roughly 66% actual-outcome interpretation. The revision explains both without asserting independent probabilistic calibration.
- **Time:** the published 2050 summary is 2035–2064. It is not a single-year forecast, an exact 2041–2070 mean, or a recipe to assign calendar years to GWL daily files. [Time-product information](https://productinformation.app.meteoswiss.ch/climate-ch2025-periodbars-temperature/climate-ch2025-periodbars-temperature_en.md).
- **Aggregation:** requesting data can remove figure controls because a table combines selections. This happened for station locations and pathway/season controls. The helper's rejection is intentional: discover the combined table and inspect/filter it before reporting a narrower result.
- **NCCS:** the cantons entry point returned 404 to direct retrieval while cached page text described CH2018 sheets and a future update. That does not establish the current update status. A retrievable fact sheet's actual generation must be checked.
- **Launch recording:** the official overview still links the C2SM recording page, but both HEAD and GET retrieval returned 404 in this environment. The registry flags it as a rediscovery route; the review did not watch the recording or treat the failure as proof of global unavailability.
- **Ancillary documentation:** live controls and some product-information prose can disagree, including older GWL wording and links. Preserve actual indicator IDs, returned selections and source versions; consult the report/guide and disclose unresolved contradictions.
- **Impact scope:** fire-weather hazard is not actual wildfire incidence, degree-day indices are not actual energy demand/crop yield, and a climate scenario alone is not a property-loss/flood-risk calculation.

## Verification and remaining limits

The renamed package passes frontmatter, link, package-consistency and offline helper checks. Live checks exercised all eight atlas families, station-name metadata, raw daily-grid asset discovery, published pathway/extreme examples and a French-language station figure. No raw national daily-grid data were downloaded. The combined pathway table exposed the selection-dropping case above; a subsequent discovery without incompatible controls succeeded.

The actual validation results are recorded in [evaluation/RESULTS.md](../evaluation/RESULTS.md). Native Claude/ChatGPT installation remains untested, and sector-specific impact workflows still require their appropriate official evidence. Request-only data and inconsistent upstream availability remain real service limitations. No internal source was added to the distributable skill.
