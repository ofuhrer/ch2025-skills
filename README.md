# CH2025 Swiss Climate — Agent Skills

Ask about Switzerland's climate in everyday language, find an official figure or report, or obtain climate data for an expert workflow. This repository provides a portable skill grounded in **Climate CH2025** and supporting official MeteoSwiss, NCCS and FOEN sources, with **official sources beside substantive climate claims**.

The skill serves both the general public and researchers, consultants and developers. It adapts the depth to the question, explains uncertainty, and distinguishes observations, conditional projections and adaptation guidance. Authority belongs to the cited sources; this repository is not an official MeteoSwiss/NCCS/FOEN publication or endorsement.

## Start here

### Use it in this conversation

Ask ChatGPT, Claude or another chat with repository access:

> Use https://github.com/ofuhrer/ch2025-skills for this conversation. Follow its CH2025 guidance and cite official sources when answering my climate questions.

The agent can fetch the instructions and relevant references directly. No upload or installation is needed for this route.

### Ask your agent to install it

For use across conversations, ask Codex, Claude Code or another skills-compatible agent:

> Install the CH2025 skills from https://github.com/ofuhrer/ch2025-skills for this agent. Follow docs/installation.md, using the marketplace where supported or the standalone skill otherwise. Preserve existing installations, avoid duplicate copies, and verify that CH2025 is available. Tell me how to invoke it and whether I need to start a new session.

For a project-specific installation, add “Install for this project only.” The agent handles the commands and paths; if the host requires a user action, it should explain that step.

If your chat cannot access the repository, upload [the compact chat instructions](chat/CH2025_CHAT.md). Hosts with manual skill import can use [the skill ZIP](releases/ch2025.zip). Detailed commands, compatibility, updates and removal are in [the installation guide](docs/installation.md).

## What you can ask

- “What does a 3-degree world mean for Switzerland? Explain simply.”
- “Warum können die Sommer trockener werden und Starkregen trotzdem zunehmen?”
- “Que disent les scénarios CH2025 sur la chaleur en ville ? Cite les sources officielles.”
- “Find the official snow scenarios for my region and explain their limits.”
- “Get Bern/Zollikofen daily mean temperatures for GWL3.0 and describe the calendar and ensemble.”
- “Which published ensemble sub-selection fits a drought impact study?”

See [simple examples](examples/README.md), [the skill instructions](skills/ch2025/SKILL.md), and [public sources](skills/ch2025/references/sources.md).

The skill now selects among **all eight atlas families**: maps, altitude bands, station indicators, seasonal/extreme changes, GWL comparisons, emission-scenario/time comparisons, annual cycles and ensemble selection. It also routes less-certain topics such as hail, fog, wind and fire weather through the official phenomena overview. [Which product fits my question?](skills/ch2025/references/products.md) [In-depth source-coverage review](docs/source-review.md).

## Data workflows

Ask your agent, for example:

> Find Bern/Zollikofen daily mean temperature data for GWL3.0. Download the original CSV into my workspace, save its source provenance, and explain the units, calendar and model coverage.

The optional Python helper discovers published products and checks station downloads. It needs Python 3.10+ but no API keys or third-party packages. The agent can use the [data guidance](skills/ch2025/references/data.md) and [worked examples](examples/README.md) for commands. Ordinary explanations do not require Python.

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

GitHub Actions runs these offline tests and package checks on Python 3.10 and 3.13 for every push and pull request. [View CI runs](https://github.com/ofuhrer/ch2025-skills/actions/workflows/checks.yml).

See the [package review](docs/package-review.md), [validation](docs/validation.md) and [evaluation scenarios](evaluation/scenarios.json). Recorded checks describe what was tested; they do not establish native execution in every model/product or perfect scientific answers.

## Licence and contributions

The new instructions and code use [0BSD](LICENSE): reuse, modify and redistribute them without crediting the skill authors. Scientific credit follows the report's imprint. Source data/graphics retain their own terms: CH2025 daily data are documented as CC BY 4.0. The skill licence does not remove those source-attribution requirements. [Attribution guidance](skills/ch2025/references/sources.md).

For a correction, include a public source, relevant section/product/version and an example question. Do not include private material or credentials. Official provider support remains separate from repository maintenance.
