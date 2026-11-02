# Access and handle data

Reviewed 2 November 2026. Start with the [current official dataset page](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios/climate-ch2025-datasets.html) and [Open Data guide](https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios); inspect actual metadata before using a file. No account or ECMWF integration is required for the public CH2025 routes described here.

## Choose the right product

| Need | Product | Key properties |
|---|---|---|
| Published figures, climate indicators or change signals | Web atlas | Aggregated products with their own definitions, selections and uncertainty estimates |
| Daily input at a station | DAILY-LOCAL | Semicolon CSV for the ensemble; ZIP containing one NetCDF per model chain |
| Daily input over a grid | DAILY-GRIDDED | NetCDF by model/variable/GWL on a localized 1 km grid; individual files can be around 1 GB or more |
| Historical measured series, climate normals or current observations | Separate MeteoSwiss observation products | Discover via [climate Open Data documentation](https://opendatadocs.meteoswiss.ch/c-climate-data); not the modeled CH2025 reference files |
| Upstream catchments/foreign partner stations | Hydrological Switzerland extension | Current documentation says data are supplied on request; metadata are public |

DAILY-LOCAL covers tas/tasmin/tasmax/pr/rsds/hurs/wind; DAILY-GRIDDED covers the three temperatures and precipitation. Availability varies by station and variable. Use metadata for units and exact model coverage. Documentation uses `sfcWind`, whereas observed public asset keys use `sfcwind`. Asset names also differ in capitalization and the grid `_ch_` token from some documentation examples. Discover keys; do not guess filenames. [Localized-data documentation, Sections 2–4](https://www.meteoswiss.admin.ch/dam/jcr:f54fae36-9a40-4e45-8abb-0308d0a68a10/CH2025_documentation_localized_v1.1.pdf).

## Production STAC route

Root: `https://data.geo.admin.ch/api/stac/v1/`

- Station collection: `ch.meteoschweiz.ogd-climate-scenarios-ch2025`
- Grid collection: `ch.meteoschweiz.ogd-climate-scenarios-ch2025-grid`
- Station item example: `https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-climate-scenarios-ch2025/items/ber`
- Grid item observed: `ch` in the grid collection.

Read collection-level station/parameter metadata, then select the returned asset key and follow its `href`. A station code is not every station in a town: distinguish Bern/Zollikofen from city-centre sites. When enumerating a collection, follow `rel=next`; a first page is not a complete inventory. Use the official browser or documented STAC clients as alternatives. The Open Data guide also supplies original Python/bash download examples.

The optional helper uses only Python 3.10+ standard-library modules. Paths below are relative to the skill folder; run with the actual installed path and write output to the user's workspace:

```sh
python3 scripts/ch2025.py sources --topic heat
python3 scripts/ch2025.py products
python3 scripts/ch2025.py stations --query Bern
python3 scripts/ch2025.py station --station ber --parameter tas --gwl gwl3.0
python3 scripts/ch2025.py station --station ber --parameter tas --gwl gwl3.0 --download ./ch2025-data
python3 scripts/ch2025.py grid --parameter tas --gwl gwl3.0 --model clmcom-cclm4-cccma
python3 scripts/ch2025.py atlas --product pathways --select emissionScenario=ssp245 --select timeOfYear=JJA
```

`sources` and `products` list bundled discovery information without network requests. `stations` searches current official metadata for station names/codes. `grid` lists matching live assets without downloading large daily grids. `atlas` returns the live selection, available controls, product-information URLs and actual file/share URLs; it downloads no figure/data and rejects requests the backend silently changes or drops. Use `--language de|fr|it|en`, repeated `--select OPTION=VALUE`, and optionally `--product-type plot|data`. Query options are product-dependent; inspect the returned `options` and read `information_urls` before interpreting a result.

Without `--download`, the station command discovers one exact asset and prints its URL/citation; it does not save data. Download mode saves the original plus a `.provenance.json` sidecar. It refuses overwrites and limits a file to 25 MB by default (`--max-mb` changes the limit). Downloads support CSV/ZIP station products only; the helper does not fetch national daily grids or process climate statistics. CSV checks require all 10,950 consecutive synthetic days, unique model columns, numeric/NA values and matching station/GWL metadata; inspection counts missing values by model. ZIP checks cover archive integrity, NetCDF/HDF5 signatures and an uncompressed-size cap of 20 times the download limit; they do not decode scientific NetCDF metadata. If data or provenance writing fails, newly created outputs are removed. Failed requests must not be reported as successful downloads.

## Calendars, masks and scientific calculations

The daily files contain 10,950 days, with synthetic dates 0001-01-01 through 0030-12-31 on a `365_day` calendar. Calendar conversion from native 360-day simulations introduces missing values; leap days from Gregorian simulations are removed. Missingness is part of the product, not automatically an error to fill. Reference files are simulations calibrated against 1991–2020, not observed event sequences. [Documentation, Sections 4 and 7](https://www.meteoswiss.admin.ch/dam/jcr:f54fae36-9a40-4e45-8abb-0308d0a68a10/CH2025_documentation_localized_v1.1.pdf).

- Detect the CSV table's `DATE;` header after metadata; do not parse the first line as a data header. Reviewed files put it on line 24. Values are semicolon-separated, model chains are columns, and `NA` means missing.
- NetCDF time/variable metadata describe the actual units, calendar, model and fill values (documented daily fill value `-999`). Use calendar-aware arrays; do not coerce years 1–30 into modern Gregorian dates. CSV precision can be lower than NetCDF precision.
- Keep baseline/future matching by model identity, station/grid and variable. Identical synthetic dates from different models are not simultaneous weather. Never concatenate GWL blocks into one historical-to-future series.
- Calculate an indicator within each model and the intended season/year, then summarize the ensemble. Distinguish temperature increments, absolute values and percentage changes in precipitation. Quantify missingness and explain the chosen treatment; do not automatically substitute zero or interpolate.
- Inspect cross-variable consistency before impact modelling. Univariate correction can produce `tasmin > tasmax` on some days; the documentation discusses this. Preserve originals and explain any needed correction rather than silently changing data.
- Check coordinate ranges and explicit CRS information against station metadata and WGS84 coordinates before transformation. Do not assign LV95 just from a narrative label. A station header, a grid projection and a regional mask are separate things to verify.

For raw daily-grid processing, inspect the file size and spatial/time chunks before computation. Use the user's established NetCDF/geospatial tools. This skill does not prescribe a library, install system dependencies, or assume that a small aggregate map is a raw DAILY-GRIDDED series.

## Web-atlas products

Use the [official atlas](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios/swiss-climate-scenarios-web-atlas.html). Its eight display types cover maps, altitude levels, station indicators, seasonal changes, GWL changes, emissions/time-period changes, climate charts and ensemble sub-selection. Read the selected product's information before extracting a value. Most products provide figures and data, but supported selections differ.

Where browser tools are available, choose the product/indicator, place, season, GWL/pathway and estimate; use its Download and Share functions. Preserve the actual share link and selection with the output. In the reviewed station-indicator display, data mode gives an all-stations summary table and removes some figure controls; it is not a station daily series.

Data tables can combine selections represented separately in figures. For example, a pathway data table can drop the figure's single season/pathway controls. If the helper rejects such a change, first discover that data mode without the dropped controls, inspect its table metadata, and only then filter the actual rows/columns. Do not report an unfiltered table as a successfully selected single-season/pathway result.

Expert fallback: the official application was observed using `https://api.productbrowser.app.meteoswiss.ch/pbbackend/api/v1/displays/` with display names such as `climate-ch2025-columns` and `climate-ch2025-maps`, `lang=en`, and `cg1.*` state parameters. Returned configuration lists available states and realization URLs. This is an implementation endpoint, not a guaranteed stable API: discover it from the current application if needed, inspect returned state/media type and fall back to the official UI. A realization may return image/PDF/CSV/NetCDF, not JSON. Asking for a data state does not guarantee the response accepted it.

A downloaded aggregate grid can have one time slice, a standard calendar and its own CRS; those properties do not override the daily-file convention. A text companion may be only a download instruction. Validate actual content before claiming that a data file was obtained.

## Provenance and request-only data

Keep public dataset/source URLs, DOI, version, station/region, variable/unit, GWL/pathway, reference period, model identities, retrieval date and processing steps with a result. Prefer an official parameterized share URL or source metadata over a bare temporary realization identifier. Source data/atlas graphics are documented as CC BY 4.0; retain attribution and identify modifications. The skill's own licensing is separate.

For hydrological Switzerland, consult the current dataset page: the reviewed April 2026 extension is supplied on request via the published climate-scenarios contact. Give that public route if data are unavailable. Do not claim access to request-only files, require internal CSCS paths, or send a message on the user's behalf unless asked.
