# Package review — v0.3.0

Reviewed **2 November 2026**, against v0.2.0 (`644d917`). The package contains one installable skill, `ch2025`, with optional references and a standard-library helper.

## Findings and decisions

| Question | Assessment and implemented improvement |
|---|---|
| Are CH2025 information and data sources covered? | Yes at the published product-class level: topic pages, brochure, video, scientific report, phenomena overview, eight atlas families, DAILY-LOCAL, DAILY-GRIDDED, specialist guides, hydrological extensions, launch material and previous scenarios. Observation and adaptation sources are explicitly separate. Coverage does not mean every individual file or sectoral impact is available or tested. No new source family was missing from v0.2.0. |
| Is installation/use straightforward? | The portable folder and ZIP were sound, but copying over an existing directory could nest or merge installations. Added an installer that copies the complete skill and licence, refuses existing targets, and works in paths containing spaces. Documented verification, backup/update and removal. No account, MCP server or third-party Python dependency is required. Native hosted-product imports remain untested. |
| Does it work? | All eight live atlas routes, station lookup, grid discovery, explicit pathway/language selections and a complete Bern CSV passed the repeatable live checks. A separate real ZIP download also passed. Fixed truncated/header-only CSV acceptance, invalid ZIP payload acceptance, missing atlas realizations, conflicting CLI selections and orphaned data after provenance-write failure. |
| Are sources enforced and hallucinations suppressed? | The skill now explicitly requires inspected evidence for precise claims and omission of unsupported values. Returned selections, file structure, source metadata and provenance are checked in code. Citation relevance and faithful prose remain model behaviour, not mechanically guaranteed. The README and validation guide now make that boundary explicit. |
| Does it follow comparable GitHub skills? | It uses standard frontmatter, a self-contained skill folder, conditional references, executable helpers, source attribution and separate offline/live/behavioural checks. The comparisons below support these choices; their service-specific permissions, dependencies and workflow prescriptions are unnecessary here. |
| Is it concise enough for capable models? | Reduced SKILL.md from 1,170 to 597 whitespace-delimited words (49%); the chat file from 5,662 to 642 (89%). Removed the redundant answer-pattern reference, shortened the discovery description, and retained scientific constraints that change decisions. Added core/chat size budgets to repository checks. Counts are reproducible size proxies, not tokenizer measurements. |

## Coverage evidence and limits

Re-read the current [official product overview](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios.html), [dataset page](https://www.meteoswiss.admin.ch/climate/climate-change/swiss-climate-scenarios/reports-data-and-graphs-of-climate-change-scenarios/climate-ch2025-datasets.html) and [Open Data documentation](https://opendatadocs.meteoswiss.ch/c-climate-data/c8-c9-climate-scenarios). The MeteoSwiss HTML needed template-text extraction; navigation-only text was not accepted as evidence. The daily-data page still lists hydrological Switzerland's precipitation grid and foreign partner-station series as request-only, and points to the atlas for derived indicators. The public helper correctly does not promise access to those request-only files.

The [source review](source-review.md) records the detailed product matrix and v0.2.0 research; [sources.md](../skills/ch2025/references/sources.md) and [products.md](../skills/ch2025/references/products.md) remain the runtime discovery guides. The current review did not re-read the entire scientific report, watch launch recordings, test every combination of atlas controls or download national grids. Historical broken-link notes remain dated, not assertions about current global availability. A station result is not a canton average, an old CH2018 sheet is not CH2025, and hazard evidence alone cannot establish sectoral impacts.

## Comparison with published skills

Inspected current upstream source, pinned here for reproducibility:

| Reference | Relevant pattern | CH2025 decision |
|---|---|---|
| [EUMETSAT EUMDAC skill](https://github.com/eumetsat/skills/blob/b2ce103f45e295df856807df88206412703d1e5c/skills/eumdac/SKILL.md) | Explicit tool/service scope, commands, intent-based references, bounded discovery and honest validation status | Retain the helper and focused reference routing. Avoid copying account-management rules and confirmation gates for services CH2025 does not use. |
| [EUMETSAT validation](https://github.com/eumetsat/skills/blob/b2ce103f45e295df856807df88206412703d1e5c/docs/validation.md) | Separate structural, CLI and behavioural checks; disclose an unavailable private validation tool | Keep checks runnable with public tools and Python's standard library. Do not imply helper tests establish model behaviour. |
| [ECMWF Open Data skill](https://github.com/ecmwf/ecmwf-weather-skills/blob/559ba8fdfe522591037625ae3dc943d5d07e09d0/plugins/ecmwf-weather/skills/ecmwf-open-data/SKILL.md) | Retrieval helpers, scientific pitfalls, attribution, explicit failure handling and conditional references | Adopt the same separation of deterministic retrieval from interpretation. No need to copy forecast defaults, earthkit requirements or a bundled MCP. |
| [ECMWF authoring/testing conventions](https://github.com/ecmwf/ecmwf-weather-skills/blob/559ba8fdfe522591037625ae3dc943d5d07e09d0/AGENTS.md) | Provider-neutral instructions, canonical files, offline/live checks and fresh-agent evaluations | Keep one canonical skill; generate distribution artifacts. Add a repeatable live check and retain behavioural scenarios without labelling unexecuted trials as passes. |
| [Agent Skills specification](https://agentskills.io/specification) | Standard metadata and progressive disclosure | Preserve the portable format; keep optional host UI metadata separate. |

These are design comparisons, not a claim that either upstream package is an ideal brevity benchmark. CH2025 needs fewer operational rules than authenticated satellite/forecast tooling. Upstream text was inspected as reference material; it was not copied into the distributable package or invoked as task instructions.

Installation locations were verified against [OpenAI's official skill documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code's skill documentation](https://code.claude.com/docs/en/skills). Filesystem installation and isolated ZIP execution were tested; native host registration was not.

ECMWF use: skills — none applied (upstream files reviewed for comparison); MCP — not used.

## Verification and remaining work

[Validation results](../evaluation/RESULTS.md) record 25 passing offline tests, 15 passing live checks, the separate ZIP probe, skill validation and lint. The CSV probe preserved 24 model columns, 10,950 synthetic days and 750 missing cells. No raw national grid was downloaded.

The smaller chat file deliberately links optional detail, so it has less offline scientific context. The native ZIP still contains all four references. Neither format guarantees truthful model output; model-level citation/abstention scenarios and native hosted imports need their own trials. Existing independent v0.1.0 trials are historical evidence, not a fresh evaluation of v0.3.0.

At review time, GitHub Actions was supplied as an example because the publishing credential lacked `workflow` scope. The workflow has since been moved to [the active CI configuration](../.github/workflows/checks.yml); see [workflow runs](https://github.com/ofuhrer/ch2025-skills/actions/workflows/checks.yml) for execution results. No credential or account settings were changed by this review.


## Distribution follow-up

The original review underweighted two convenient routes. ECMWF also distributes its skills through [Codex and Claude marketplaces](https://github.com/ecmwf/ecmwf-weather-skills#installation), and a chat with repository access can fetch these instructions directly from a URL. CH2025 now includes `.claude-plugin/marketplace.json` plus Claude and Codex plugin manifests pointing to the existing canonical skills folder. The README leads with repository-link use and marketplace commands; upload/copy and standalone-folder installation remain fallbacks. This is a repository-hosted marketplace, not a curated-directory submission.

Codex marketplace registration, installation and discovery were verified in an isolated temporary configuration. Native Claude installation remains untested. A user-supplied shared ChatGPT conversation demonstrated repository-link use without uploading instructions; its visible acknowledgement and sourced follow-up answers establish that usage route, not a complete audit of retrieval traces or scientific correctness. Personal conversation details are not included here.
