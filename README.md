# CH2025 Swiss Climate — Agent Skills

Ask about Switzerland's climate in everyday language, find an official figure or report, or obtain climate data for an expert workflow. This repository provides a portable skill grounded in **Climate CH2025** and supporting official MeteoSwiss, NCCS and FOEN sources, with **official sources beside substantive climate claims**.

The skill serves both the general public and researchers, consultants and developers. It adapts the depth to the question, explains uncertainty, and distinguishes observations, conditional projections and adaptation guidance. Authority belongs to the cited sources; this repository is not an official MeteoSwiss/NCCS/FOEN publication or endorsement.

## Start here

| How you work | Use |
|---|---|
| Ordinary ChatGPT, Claude or another chat | [Compact chat instructions](chat/CH2025_CHAT.md): upload the file or paste its contents, then ask a question |
| A product supporting custom skills | Download [the skill ZIP](releases/ch2025.zip) and follow that product's import instructions |
| Codex, Claude Code or another skills-compatible agent | Install the [skill folder](skills/ch2025) as described below |
| Python workflow | Optional [discovery/data helper](skills/ch2025/scripts/ch2025.py), without API keys or third-party packages |

A file cannot add browsing, code execution or network access that the host does not provide. Without live access, use is limited to dated reference material and official verification links. Chat instructions are not a native skill installation. See [compatibility and installation](docs/installation.md).

## What you can ask

- “What does a 3-degree world mean for Switzerland? Explain simply.”
- “Warum können die Sommer trockener werden und Starkregen trotzdem zunehmen?”
- “Que disent les scénarios CH2025 sur la chaleur en ville ? Cite les sources officielles.”
- “Find the official snow scenarios for my region and explain their limits.”
- “Get Bern/Zollikofen daily mean temperatures for GWL3.0 and describe the calendar and ensemble.”
- “Which published ensemble sub-selection fits a drought impact study?”

See [simple examples](examples/README.md), [the skill instructions](skills/ch2025/SKILL.md), and [public sources](skills/ch2025/references/sources.md).

The skill now selects among **all eight atlas families**: maps, altitude bands, station indicators, seasonal/extreme changes, GWL comparisons, emission-scenario/time comparisons, annual cycles and ensemble selection. It also routes less-certain topics such as hail, fog, wind and fire weather through the official phenomena overview. [Which product fits my question?](skills/ch2025/references/products.md) [In-depth source-coverage review](docs/source-review.md).

## Install for an agent

```sh
git clone https://github.com/ofuhrer/ch2025-skills.git
cd ch2025-skills
```

Install with Python 3.10+ into **one** host's skills directory (existing installations are preserved):

```sh
# Personal Codex installation; works across projects.
python3 scripts/install_skill.py ~/.agents/skills

# Or install for a particular Codex project.
python3 scripts/install_skill.py /path/to/your/project/.agents/skills

# Or install for Claude Code.
python3 scripts/install_skill.py ~/.claude/skills
```

The installer copies the complete skill and licence, refuses to merge/overwrite an existing `ch2025` folder, and requires no account or network. Without Python, extract [the ZIP](releases/ch2025.zip) into the host's skills directory. See [installation, updates and removal](docs/installation.md).

In Codex, invoke `$ch2025`; in Claude Code, use `/ch2025`. Hosts may also select it for a matching question. Native behaviour still needs to be checked in each product. [OpenAI documentation](https://learn.chatgpt.com/docs/build-skills), [Claude Code documentation](https://code.claude.com/docs/en/skills).

## Optional discovery and data helper

Python 3.10+ is needed only for this helper. Run from the repository root:

```sh
# List official sources without a network call.
python3 skills/ch2025/scripts/ch2025.py sources --topic heat
python3 skills/ch2025/scripts/ch2025.py products

# Find station codes and discover published pathway/time summaries.
python3 skills/ch2025/scripts/ch2025.py stations --query Bern
python3 skills/ch2025/scripts/ch2025.py atlas --product pathways \
  --select emissionScenario=ssp245 --select timeOfYear=JJA

# Discover grid assets without downloading large daily files.
python3 skills/ch2025/scripts/ch2025.py grid \
  --parameter tas --gwl gwl3.0 --model clmcom-cclm4-cccma

# Discover one asset; no data file is saved yet.
python3 skills/ch2025/scripts/ch2025.py station \
  --station ber --parameter tas --gwl gwl3.0

# Download the original CSV and a provenance sidecar.
python3 skills/ch2025/scripts/ch2025.py station \
  --station ber --parameter tas --gwl gwl3.0 --download ./ch2025-data
```

Atlas discovery returns live controls, product-information links, selected state and available file/share URLs; it rejects silently changed or dropped selections. Grid discovery is metadata-only. Station downloads check complete synthetic-date sequences and numeric values, count missing cells, preserve originals/provenance, refuse overwrites, and default to a 25 MB file limit. The helper does not fetch a national archive or compute scientific statistics. [Data guidance](skills/ch2025/references/data.md) covers formats, units, calendars and alternatives. Daily GWL files use synthetic years 1–30; model reference series are not observed daily weather. [Official data documentation](https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios).

## Sources and credit

Use the report's prescribed scientific citation: **MeteoSwiss & ETH Zurich (2025): Climate CH2025 – Scientific Report. Federal Office of Meteorology and Climatology MeteoSwiss, Zurich.** [DOI](https://doi.org/10.18751/climate/scenarios/ch2025/sr/1.0/). Its imprint credits the authors, editors, supporting teams and institutions. For daily data, cite **MeteoSwiss & ETH Zurich (2025): Climate CH2025 – Daily Datasets**, [dataset DOI](https://doi.org/10.18751/climate/scenarios/ch2025/data/1.0/).

The skill requires inspected public evidence for precise claims. These are model instructions, not a citation validator or a guarantee against hallucinations. The helper enforces selection, file-integrity and provenance checks; it cannot verify that prose faithfully represents a source. Calculated results must identify inputs and methods. The package contains curated instructions and public links; it does not contain internal Confluence material, credentials or the local research archive. Evidence was reviewed on **2 November 2026**; current values, services and versions require current verification.

No ECMWF service, account, skill or MCP server is required by this package.

## Development and validation

```sh
python3 scripts/build_release.py
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

See the [package review](docs/package-review.md), [validation](docs/validation.md) and [evaluation scenarios](evaluation/scenarios.json). Recorded checks describe what was tested; they do not establish native execution in every model/product or perfect scientific answers.

## Licence and contributions

The new instructions and code use [0BSD](LICENSE): reuse, modify and redistribute them without crediting the skill authors. Scientific credit follows the report's imprint. Source data/graphics retain their own terms: CH2025 daily data are documented as CC BY 4.0. The skill licence does not remove those source-attribution requirements. [Attribution guidance](skills/ch2025/references/sources.md).

For a correction, include a public source, relevant section/product/version and an example question. Do not include private material or credentials. Official provider support remains separate from repository maintenance.
