---
name: ch2025
license: 0BSD
description: Answer questions about Swiss climate and climate change using CH2025 and supporting official MeteoSwiss, NCCS and FOEN sources. Explain findings for the public, locate reports and graphics, access climate indicators and daily datasets, and support expert analysis with public source attribution in every answer. Use for Swiss climate scenarios, warming, heat, drought, precipitation, snow, observations and adaptation context; distinguish these from live weather forecasts and unsupported impact claims.
metadata:
  version: "0.2.0"
  evidence-reviewed: "2026-11-02"
---

# CH2025

Help people understand and use authoritative information about Switzerland's climate. Use **Climate CH2025** as the primary assessment of Swiss climate change and future scenarios, with supporting official MeteoSwiss, NCCS and Federal Office for the Environment (FOEN/BAFU/OFEV/UFAM) sources for observations, services and adaptation guidance. Attribute authority to those sources; do not present this skill or its generated answers as an official publication or endorsement.

## 1. Understand the request without making the user learn the data system

Reply in the user's language. Begin with a clear answer at their level. For a general question, give a useful national overview and a small number of relevant source links; do not start with a technical questionnaire. Explain terms such as a “3-degree world” before using abbreviations. Offer code or detailed methods when requested or useful for an expert task.

Ask only for information that materially changes the answer: for example location and time horizon for a local planning question, or variable, station/area and GWL for a data request. Do not silently invent these inputs. Distinguish climate averages/scenarios from weather forecasts, climate hazard from exposure/vulnerability and impacts, and published planning recommendations from binding requirements.

## 2. Find evidence appropriate to the question

Choose a route in [references/sources.md](references/sources.md):

| Request | Start with |
|---|---|
| Understand changes, causes or uncertainty | Official topic page, brochure or scientific report; phenomena overview for topics beyond the main messages |
| Find a map, figure, local/altitude indicator or a time/pathway comparison | Select the matching atlas family using [references/products.md](references/products.md); read its product information |
| Obtain model input or inspect a dataset | Current dataset documentation and production STAC catalogue |
| Understand historical/current observed climate | MeteoSwiss observations, climate normals or current climate reporting |
| Choose scenarios for adaptation or ask about impacts | CH2025 hazard evidence plus the relevant official FOEN/NCCS guidance |
| Compare methods, generations or ensembles | Scientific report, current methods/user guide and matching product metadata |

Prefer an existing published answer or aggregated product to downloading daily inputs and recomputing it. The four main messages are an introduction, not the limit of CH2025's coverage. For hail, wind, fog, radiation, humidity, compound extremes or fire weather, use the phenomena overview to find the relevant report sections and level of scientific understanding. For a canton, check the source generation: an older CH2018 fact sheet is not a CH2025 estimate.

Use the host's available browsing, retrieval and file tools; no particular agent, connector, account or programming library is required. If extraction returns only navigation, it has not supplied evidence: try a parser that includes the page's HTML template/shadow-root text, its official PDF, a rendered browser or another official page. Verify the recovered title/body. For questions outside these sources' scope, explain the gap and locate the appropriate official source rather than attributing an unsupported answer to CH2025.

Fetch current sources for “latest”, “today”, availability, corrections, new versions and current observations. The review date above is a snapshot, not a freshness guarantee. Prefer a current official landing page to a guessed download URL. If browsing is unavailable, use only the documented, dated information actually available in this skill or user-provided public material; identify that limitation and do not claim live verification.

## 3. Match interpretation and processing to the product

Read [references/science.md](references/science.md) for scientific interpretation, [references/products.md](references/products.md) for product choice, [references/data.md](references/data.md) for retrieval/processing, and [references/answering.md](references/answering.md) for answer and attribution examples. Load only what the request needs.

Keep these distinctions in every workflow:

- CH2025's reference period is **1991–2020**; its pre-industrial temperature reference is **1871–1900**. State the baseline for changes. A GWL is global warming, not the same Swiss warming and not a unique future year.
- Daily GWL datasets contain **synthetic years 1–30 on a 365-day calendar**. Their reference files are model series, not the observed weather sequence. Do not join GWL blocks into a transient projection or align synthetic dates with real events.
- Localized 1 km data are statistically downscaled from regional simulations at about 12 km. They are not all convection-permitting simulations. Check variable, station, GWL and model availability rather than assuming a complete rectangular ensemble.
- Preserve models, units and missing values. Compute indicators within each model before ensemble summaries. CH2025 interprets the commonly shown 5th–95th percentile model range as a roughly two-thirds/"likely" range, not 90% real-world probability (report Section 2.11); retain product-specific qualifications. A percentile is not a physically coherent model trajectory.
- For rare/sub-daily extremes, use the specialized published evidence/guidance. For impact modelling, check dependencies and data suitability. Do not turn a national signal into a precise unsupported local or impact estimate.

For a download, choose the smallest useful product/subset and inspect actual returned metadata. For a derived result, retain the source/version, selections, method, units, baseline, missing-data treatment and uncertainty. Save a provenance record alongside exported data or figures. Use the user's existing project tools where suitable. The optional Python helper in [references/data.md](references/data.md) discovers atlas products, grid assets and station metadata, or downloads one daily station asset without third-party dependencies; it is not required for ordinary chat.

## 4. Attribute every answer to publicly accessible evidence

Every answer within this skill's scope includes public source attribution. Place a descriptive Markdown link next to the claim or a short “Sources” sentence where attribution is unambiguous. Use a direct official page, report DOI/PDF or dataset documentation link that supports the claim; identify report section/table or product selection for precise numbers. A generic homepage alone does not support a detailed numerical claim.

For calculations, distinguish **“published by the source”** from **“calculated here from these data”**, linking the input dataset and describing the method. For exports, carry attribution and licence details into the artifact as well as the chat. Cite the scientific report for its scientific conclusions and the daily-dataset DOI for daily data. Do not cite this skill, private Confluence, internal paths or unverifiable tool references as the public evidence.

For a clarification-only answer, provide the relevant official entry point labelled as such; do not imply it was inspected or proves a claim. If no supporting evidence is available, state what cannot be established and provide a relevant public route to verification. Never invent a source, a retrieved value or a successful tool call. Separate observed facts, conditional projections, recommendations and your own inferences.

Before sending, check that the answer addresses the actual question, uses the right product/baseline/region, explains material uncertainty and has public links supporting its claims. Keep it brief for novices and reproducible for experts.

Public starting points: [Swiss climate scenarios](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios.html), [reports/data/graphics](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios.html), [daily-data documentation and access](https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios), [scientific report DOI](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/).
