# Validation

The repository separates executable checks from behavioural evaluation. A passing format check does not establish scientific correctness or identical behaviour in every host.

## Repeatable local checks

```sh
python3 scripts/build_release.py
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

The helper tests use small synthetic transport/format fixtures, not fake scientific findings. They verify actual returned-asset selection, missing assets, source-preserving downloads, synthetic dates, overwrite refusal, size limits, invalid content and partial-file cleanup. Repository checks validate standard frontmatter, local documentation links, source-registry consistency and exact agreement of generated chat/ZIP artifacts with the canonical files.

Repository checks also verify marketplace/plugin paths and agreement with the canonical skill name, version and licence. The ZIP packages only the skill folder and its licence. The compact chat version is generated from the same core, with optional references linked instead of embedded. The local source-gathering archive is excluded from both the package and version control.

[GitHub Actions](../.github/workflows/checks.yml) runs the offline tests and repository checks on Python 3.10 and 3.13 for pushes and pull requests. It checks the committed chat/ZIP artifacts without rebuilding them, so stale generated files fail CI. Live service checks remain opt-in. See [workflow runs](https://github.com/ofuhrer/ch2025-skills/actions/workflows/checks.yml).

## Live contracts

```sh
python3 scripts/check_live.py --download --output evaluation/runs/live.json
```

This compares the registry against the live atlas catalogue and exercises all atlas families, explicit pathway/language selections, dropped-selection rejection, station lookup, grid discovery and one bounded CSV download. Omit `--download` for metadata only. Outputs are saved only when requested; the station check uses a temporary directory. Failures remain failures and return a nonzero exit code; upstream changes require inspection, not weakening assertions to recover a green result. This is an opt-in network check, separate from offline CI.

## What is enforced

The helper mechanically rejects unavailable/changed selections, missing atlas realizations, incomplete or malformed daily CSVs, wrong station/GWL metadata, invalid ZIP payload signatures, oversize files and overwrites. It preserves original bytes and source/hash/inspection sidecars, rolling back its new files on write failure. These are transport/format checks, not scientific validation of every value or NetCDF variable.

Citation relevance, faithful interpretation and abstention from unsupported claims are instructions to the model. They cannot be guaranteed by a Markdown skill or tests of the helper. No regex for the presence of a URL establishes that a claim is true. Assess actual answers against inspected evidence using the scenarios below; keep unexecuted scenarios distinct from passes.

## Behavioural checks

[scenarios.json](../evaluation/scenarios.json) contains novice, multilingual, expert, unavailable-tool and scientific-interpretation requests with observable checks. Run the skill as the user would, record the actual answer/actions/sources, and assess whether the response meets those checks. Do not give an evaluating agent the intended answer in advance. Use a temporary directory for download examples.

Cross-product validation must be performed in each product. Standard-format checks and testing in Codex do not demonstrate successful native installation in Claude, ChatGPT or all other agents. The ordinary-chat version is a fallback, still subject to host tools and instruction priority.

## Recorded results

See [the validation record](../evaluation/RESULTS.md) for the actual checks completed for this draft. Future changes to retrieval, citations or scientific behaviour should rerun the affected checks and update that record.
