# Answer patterns and attribution

Adapt the length and language; these are examples of behaviour, not mandatory templates or fixed scientific answers. Retrieve the evidence needed for the actual request.

## A public question

User: “What does a 3-degree world mean for Switzerland?”

Explain that it means a global average temperature increase relative to a specified pre-industrial period, not precisely 3 °C everywhere in Switzerland. Give the principal Swiss changes in plain language, introduce uncertainty and link the [official GWL explanation](https://www.meteoswiss.admin.ch/weather/weather-and-climate-from-a-to-z/global-warming-level-gwl.html) and the relevant [CH2025 findings](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios.html). If quoting a Swiss numerical value, give its baseline, estimate/range and exact supporting report section or product. Do not attach a unique year without pathway evidence.

## A local question with missing context

User: “Will my town have enough snow for skiing?”

Explain the direction of the published snow changes, then request the location/elevation and intended time horizon if needed to refine the answer. Cite [MeteoSwiss snow information](https://www.meteoswiss.admin.ch/climate/climate-change/less-snow-and-cold.html). Distinguish a climate indicator from ski-area viability, which also depends on terrain, operations and adaptation. Do not invent a town-specific snow-day count. The initial answer should still be helpful.

## A published map or indicator

Return the relevant figure/data link plus the chosen indicator, station/region, season, baseline, GWL/pathway and uncertainty estimate. Explain whether the numbers are observations, future absolute values or changes. Use the [web atlas](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios/swiss-climate-scenarios-web-atlas.html) and its product-specific documentation; for an exact value, preserve the actual selection/shared product URL. A generic homepage does not establish that value.

## An expert data request

User: “Download Bern daily mean temperatures for GWL3.0 and prepare them for analysis.”

Discover the actual STAC station asset, inspect its metadata and download it if the host permits. Report product/version, station, variable/unit, model count, synthetic calendar and missingness. Do not turn synthetic years into 2041–2070 or call the model baseline observations. Link [the official data access guide](https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios) and [the daily-data DOI](https://doi.org/10.18751/climate/scenarios/ch2025/data/1.0/). Save data provenance with the output. If unable to download, give a precise route or runnable request and say it has not been executed.

## A calculated answer

Label an output as “Calculated here from CH2025 …” and report the indicator definition, per-model calculation, matching reference/future chains, calendar/missing-value treatment and ensemble summary. Cite the input dataset and the official indicator definition/method. Name any user-supplied assumptions separately. Do not pass the result off as a published CH2025 number.

## Attribution examples

- Published finding: “... [MeteoSwiss: Drier summers](https://www.meteoswiss.admin.ch/climate/climate-change/drier-summers.html).”
- Method: “... [MeteoSwiss & ETH Zurich (2025), scientific report, Section 2.8](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/).”
- Download/derived output: “Source: MeteoSwiss & ETH Zurich (2025), Climate CH2025 – Daily Datasets, [DOI](https://doi.org/10.18751/climate/scenarios/ch2025/data/1.0/), version [read from file], [station/variable/GWL], retrieved [actual date]; CC BY 4.0. Calculation: [method].” Replace brackets with actual metadata rather than leaving placeholders in an answer.
- Clarification only: “Which station or region should I use? Official entry point: [CH2025 datasets](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios/climate-ch2025-datasets.html).”
- No live access: “I cannot verify the latest value in this environment. The dated material available here establishes [limited supported statement]. Current verification route: [MeteoSwiss climate reporting](https://www.meteoswiss.admin.ch/climate.html).” Do not claim that a linked page was fetched if it was not.

Use one or two sources when they suffice; add sources where claims require them. Do not append a long unrelated reading list to a short novice answer. Preserve source names and links in the user's language without translating quotations as if they were verbatim originals.
