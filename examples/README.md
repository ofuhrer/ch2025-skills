# Simple examples

Use these with [the chat instructions](../chat/CH2025_CHAT.md) or an installed [skill](../skills/ch2025/SKILL.md). These prompts describe expected behaviour, not precomputed answers or claims that downloads already ran.

## Understand a warmer Switzerland

> What does a 3-degree world mean for Switzerland? I have no scientific background. Keep it short and cite official sources.

Explain global versus Swiss warming and the reference period, describe the changes without false precision and link supporting evidence. Do not assign a unique future year. [Official GWL explanation](https://www.meteoswiss.admin.ch/weather/weather-and-climate-from-a-to-z/global-warming-level-gwl.html).

## Explain an apparent contradiction

> Warum können die Sommer in der Schweiz trockener werden, obwohl Starkregen häufiger wird? Bitte einfach erklären und Quellen verlinken.

Distinguish seasonal water balance/dry spells from intense rainfall events, answer in German and cite [dry-summer](https://www.meteoswiss.admin.ch/climate/climate-change/drier-summers.html) and [heavy-precipitation](https://www.meteoswiss.admin.ch/climate/climate-change/more-frequent-and-more-intense-heavy-precipitation.html) evidence. Do not invent a local percentage.

### Example of a short sourced answer

Trockenheit hängt davon ab, wie viel Wasser über den Sommer im Boden bleibt. Weniger Sommerregen und mehr Verdunstung können den Boden austrocknen. Einzelne Regengüsse können trotzdem heftiger werden, weil wärmere Luft mehr Wasserdampf aufnehmen kann. Mehr Starkregen gleicht die Austrocknung also nicht automatisch aus. [MeteoSwiss: Drier summers](https://www.meteoswiss.admin.ch/climate/climate-change/drier-summers.html), [Heavy precipitation](https://www.meteoswiss.admin.ch/climate/climate-change/more-frequent-and-more-intense-heavy-precipitation.html).

This is an illustrative qualitative explanation, not a local quantitative forecast.

## Find information about a place

> Que disent les scénarios CH2025 sur les nuits tropicales à Lausanne ? Aide-moi à trouver les informations officielles.

Identify station/urban context, locate the product or ask a consequential clarification, and preserve definition, period, GWL and uncertainty. Cite the actual product for numerical values. [Official urban-heat information](https://www.meteoswiss.admin.ch/climate/climate-change/more-extreme-heat/urban-heat.html).

## Start an expert workflow

> Download Bern/Zollikofen DAILY-LOCAL mean temperature for GWL3.0 as CSV. Describe its calendar, model columns, units and missing values, and save provenance. Do not calculate an ensemble mean yet.

From the repository root:

```sh
python3 skills/ch2025/scripts/ch2025.py station \
  --station ber --parameter tas --gwl gwl3.0 --download ./ch2025-data
```

Report what actually succeeded, retain the synthetic calendar and cite [the access guide](https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios) and [dataset DOI](https://doi.org/10.18751/climate/scenarios/ch2025/data/1.0/). The helper does not modify values or calculate climate statistics.

## Choose a scenario for planning

> We are planning infrastructure that should last several decades. What official guidance helps us choose a CH2025 scenario, and what information do you need from us?

Distinguish scientific evidence from planning recommendations and cite [current FOEN guidance](https://www.bafu.admin.ch/de/empfehlung-klimaszenarien). Ask only for consequential project context. Do not present a recommendation as a binding legal standard for all projects.

## Use a published time-horizon result

> What does CH2025 project for Swiss summer rainfall around 2050 under SSP2-4.5? Please use published results rather than calculate a new indicator.

Choose the [Changes by emission scenario](https://www.meteoswiss.admin.ch/services-and-publications/applications/ext/climate-ch2025-periodbars.html) product. Its central-year 2050 period is **2035–2064**, not weather in one year or a daily 2041–2070 series. Preserve variable, region, JJA, pathway, baseline, published range and source selection. [Product documentation](https://productinformation.app.meteoswiss.ch/climate-ch2025-periodbars-temperature/climate-ch2025-periodbars-temperature_en.md).

```sh
python3 skills/ch2025/scripts/ch2025.py atlas --product pathways \
  --select scenarioIndicator=pr --select emissionScenario=ssp245 \
  --select timeOfYear=JJA --select referencePeriod=1991-2020
```

## Ask about evidence beyond the main messages

> Does CH2025 say that hail, fog and wind will all become more extreme? How confident are the findings?

Start with the [phenomena overview](https://www.meteoswiss.admin.ch/dam/jcr:d21a2534-89d2-4b8f-96df-4fdf826cd380/CH2025_Overview-of-past-and-future-changes.pdf), then its report-section pointers. Separate observations, process expectations and projections for each phenomenon, and preserve their different levels of scientific understanding. Do not generalize the strong evidence for warming to every weather phenomenon.

## Find published extreme-precipitation changes

> Find the published change in the 50-year return value of 1-day precipitation for western Switzerland. Do not estimate a new return level from station daily data.

Use the Seasonal changes product (`x1d50`, model region `CHW`) and read the returned product help. It provides a regional change signal relative to 1991–2020; it is not an absolute local design rainfall. [Official application](https://www.meteoswiss.admin.ch/services-and-publications/applications/ext/climate-ch2025-barplotperiod.html).

```sh
python3 skills/ch2025/scripts/ch2025.py atlas --product seasonal \
  --select scenarioIndicator=x1d50 --select region=CHW
```
