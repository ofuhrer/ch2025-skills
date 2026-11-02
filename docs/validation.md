# Validation

The repository separates executable checks from behavioural evaluation. A passing format check does not establish scientific correctness or identical behaviour in every host.

## Repeatable local checks

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py
python3 scripts/check_repository.py
```

The helper tests use small synthetic transport/format fixtures, not fake scientific findings. They verify actual returned-asset selection, missing assets, source-preserving downloads, synthetic dates, overwrite refusal, size limits, invalid content and partial-file cleanup. Repository checks validate standard frontmatter, local documentation links, source-registry consistency and exact agreement of generated chat/ZIP artifacts with the canonical files.

The ZIP packages only the skill folder and its licence. The self-contained chat version is generated from the same core/reference text. The local source-gathering archive is excluded from both the package and version control.

An optional [GitHub Actions example](github-actions.example.yml) runs the checks on Python 3.10 and 3.13. To enable it, add it as `.github/workflows/checks.yml` using an account/token authorised to manage workflows. It is supplied as an example and is not active CI in this initial repository. The publishing sign-in lacked the GitHub `workflow` scope; account permissions were not changed.

## Behavioural checks

[scenarios.json](../evaluation/scenarios.json) contains novice, multilingual, expert, unavailable-tool and scientific-interpretation requests with observable checks. Run the skill as the user would, record the actual answer/actions/sources, and assess whether the response meets those checks. Do not give an evaluating agent the intended answer in advance. Use a temporary directory for download examples.

Cross-product validation must be performed in each product. Standard-format checks and testing in Codex do not demonstrate successful native installation in Claude, ChatGPT or all other agents. The ordinary-chat version is a fallback, still subject to host tools and instruction priority.

## Recorded results

See [the validation record](../evaluation/RESULTS.md) for the actual checks completed for this draft. Future changes to retrieval, citations or scientific behaviour should rerun the affected checks and update that record.
