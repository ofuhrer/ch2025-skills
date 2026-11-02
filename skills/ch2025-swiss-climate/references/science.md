# Scientific interpretation

Use this reference for baselines, scenario interpretation, methods or uncertainty. Evidence: [CH2025 scientific report](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/), especially Chapters 2, 4 and 6, and the [localized-data documentation](https://www.meteoswiss.admin.ch/dam/jcr:f54fae36-9a40-4e45-8abb-0308d0a68a10/CH2025_documentation_localized_v1.1.pdf). Reviewed 2 November 2026; verify current versions for detailed operational use.

## Meaning of periods and warming levels

CH2025 uses 1871–1900 as its pre-industrial temperature period and 1991–2020 as its main reference period; 1961–1990 is another historical comparison period. The IPCC's commonly encountered 1850–1900 baseline must not be silently substituted. Always preserve the baseline stated for a number. “Current climate in 2024” in the 2025 report is a dated estimate of the climate mean, not the weather of one year or a live 2026 value. [Report, Section 2.5](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/).

Global warming levels (GWLs, or degree-worlds) condition on global mean warming; Swiss regional warming can be larger. A GWL is not a calendar date or a unique emissions pathway. Timing requires the relevant pathway/time-dependent evidence and its uncertainty. Public communication commonly uses GWL1.5, GWL2.0 and GWL3.0; daily data and selection products also include GWL2.5. Check the particular product. [Official GWL explanation](https://www.meteoswiss.admin.ch/weather/weather-and-climate-from-a-to-z/global-warming-level-gwl.html).

## Models and downscaling

The core regional simulations are EURO-CORDEX EUR-11 at roughly 12 km, driven by CMIP5 GCMs. The CH2025 framework incorporates CMIP6 information through pairing and adjustment; the daily products should not be called direct CMIP6-driven regional simulations. GWL information using Block-Time-Shift and transient warming-adjustment information are separate constructions. Their existence does not supply a direct recipe for concatenating the public synthetic daily blocks. [Report, Sections 2.2–2.9](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/).

Quantile mapping, calibrated over 1991–2020, provides statistical bias adjustment and localization to stations and a 1 km grid. It does not add every unresolved physical process, guarantee corrected temporal variability/dependencies, or make all fields convection-permitting. Check suitability for impact and extremes applications. [Report, Sections 2.10 and 6.4](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/); [daily-data documentation, Section 7](https://www.meteoswiss.admin.ch/dam/jcr:f54fae36-9a40-4e45-8abb-0308d0a68a10/CH2025_documentation_localized_v1.1.pdf).

The documented ensemble comprises 54 underlying simulations across RCP2.6/4.5/8.5; localized GWL sets generally contain 26 GCM–RCM chains for GWL1.5/2.0/2.5 and 24 for GWL3.0, with fewer for some variables (notably humidity). Inspect actual availability; do not assume the same members or missingness for every product. The documentation's Tables 1, 2 and 5 identify models and scenario correspondence. [Daily-data documentation, Section 2 and tables](https://www.meteoswiss.admin.ch/dam/jcr:f54fae36-9a40-4e45-8abb-0308d0a68a10/CH2025_documentation_localized_v1.1.pdf).

## Regions and uncertainty

Preserve the selected region system. The five biogeographic regions (Jura, Swiss Plateau, Pre-Alps, Alps, south side of the Alps) differ from raw-model regions CHNE/CHW/CHS/CHAW/CHAE and from the larger WWCE framework region. Hydrological Switzerland additionally covers upstream catchments outside political Switzerland. A station or urban measurement location is not interchangeable with an entire municipality. [Report, Section 2.4/Figure 2.4](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/).

Many products show the 50th percentile/median and 5th/95th percentile estimates. Explain what distribution the product summarizes. Ensemble spread is not automatically a calibrated real-world probability interval; emissions, timing, internal variability and model/method uncertainty play different roles. GWL conditioning reduces some sources of uncertainty without eliminating uncertainty about regional responses or timing. [Report, Section 2.11](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/).

Prefer the full ensemble. If resources require fewer members, use the documented selection for the user's GWL, region and application. The 2026 guide has seven cases: temperature; precipitation; both; drought; heatwaves; heavy precipitation; snow-scarce winter. A selected lower/middle/upper model is application-dependent, not a universally best model. [Ensemble-selection guide, Sections 1–3](https://www.meteoschweiz.admin.ch/dam/jcr:c746625d-da94-4bb0-bd8f-f8260c15f8f1/CH2025_ensemble_subselection_guide_v1.0.pdf).

## Hazards, extremes and impacts

Changes in mean precipitation, dry spells and heavy precipitation are distinct quantities. Seasonal drying and intensifying heavy rainfall can coexist. Use exact indicator definitions and seasons. Future loss or risk additionally depends on exposure, vulnerability and adaptation; CH2025 alone does not supply an individual's flood probability, crop yield or property loss. [Report, Chapters 3–4](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/).

For rare/sub-daily precipitation extremes, consult the dedicated Chapter 4 evidence and [official heavy-precipitation guidance](https://www.meteoswiss.admin.ch/climate/climate-change/more-frequent-and-more-intense-heavy-precipitation.html). Its practical scaling note uses a regional temperature increment relative to an appropriate observational baseline. Preserve accumulation duration, return period, spatial context and stated assumptions. Do not use the GWL number itself as that temperature increment or present a simplified scaling as an exact local design result.
