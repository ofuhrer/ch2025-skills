# Installation and compatibility

The canonical package is `skills/ch2025/`. Its `SKILL.md` contains standard YAML `name`/`description` metadata and Markdown instructions; supporting files use relative paths. This follows the [Agent Skills specification](https://agentskills.io/specification). Optional `agents/openai.yaml` supplies UI metadata for supporting OpenAI hosts, without imposing a dependency on other hosts.

This guide supplies the host-specific steps for an agent carrying out the [README installation prompt](../README.md#ask-your-agent-to-install-it), and for users who prefer manual setup. Check for an existing installation before choosing a route; verify the result and report any user action still needed.

## Chat with repository access

Ask ChatGPT, Claude or another capable chat:

> Use https://github.com/ofuhrer/ch2025-skills for this conversation. Read skills/ch2025/SKILL.md and only the references needed for my question. Use official sources for scientific claims.

If the chat can fetch GitHub content through its browsing or connected repository tools, no download, upload or copying is needed. A direct [SKILL.md link](https://github.com/ofuhrer/ch2025-skills/blob/main/skills/ch2025/SKILL.md) or [raw chat-instructions link](https://raw.githubusercontent.com/ofuhrer/ch2025-skills/main/chat/CH2025_CHAT.md) can help it reach the actual text. Ask it to identify which files it read if retrieval is unclear. Acknowledging a URL alone does not establish that its contents were retrieved.

This applies the guidance to the current conversation. It does not register a persistent native skill, supply execution tools or grant access to private repositories. Retrieval depends on the host, enabled tools and account/workspace settings.

If repository retrieval is unavailable, upload [CH2025_CHAT.md](../chat/CH2025_CHAT.md); paste its contents only if file upload is also unavailable. The generated file contains the core instructions and public starting links, with optional references linked rather than embedded. Without live access, use only dated evidence actually available in the conversation.

## Marketplace installation

Like [ECMWF's skill package](https://github.com/ecmwf/ecmwf-weather-skills#installation), this repository provides a marketplace and host-specific plugin manifests around the same canonical `skills/ch2025/` folder. It bundles no MCP server or account integration.

For **Codex**, run:

```sh
codex plugin marketplace add ofuhrer/ch2025-skills
codex plugin add ch2025@ch2025-skills
```

Start a new session and select CH2025 from the available skills/plugins. `codex plugin list --json` reports installed and available plugins. [Official plugin commands](https://learn.chatgpt.com/docs/developer-commands).

For **Claude Code**, run inside the chat:

```text
/plugin marketplace add ofuhrer/ch2025-skills
/plugin install ch2025@ch2025-skills
/reload-plugins
```

Invoke `/ch2025:ch2025` for the plugin's namespaced skill. A standalone copy instead uses `/ch2025`. [Official marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces), [plugin manifest reference](https://code.claude.com/docs/en/plugins-reference).

This is a repository-hosted marketplace, not automatic inclusion in either vendor's curated directory. Hosted ChatGPT/Claude plugin availability and import controls depend on the product and workspace; follow their current plugin UI. Adding a marketplace in a local CLI does not install it into every web account. [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).

Choose plugin installation or a standalone copy, not both. Codex installation is tested in an isolated temporary configuration; Claude's manifest follows its documented format, but native Claude installation has not been tested here.

## ChatGPT or Claude with native skills

Use [the skill ZIP](../releases/ch2025.zip) with the host's documented import facility, where available. It contains one top-level skill folder. Installation is separate in each host; a GitHub download does not register a skill everywhere.

OpenAI documents skills for ChatGPT/Codex, with standalone skills and plugin distribution having different availability: [Build skills](https://learn.chatgpt.com/docs/build-skills). Claude documents custom skills across products, with setup/tool access depending on the surface: [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). Check those current pages for account/workspace requirements. Native installation in every product has not been tested here.

## Get a checkout for standalone installation

If a checkout is not already available, clone the public repository:

```sh
git clone https://github.com/ofuhrer/ch2025-skills.git
cd ch2025-skills
```

The marketplace route above handles repository retrieval itself.

## Standalone Codex skill

From the checkout, run `python3 scripts/install_skill.py /path/to/project/.agents/skills` for a project or `python3 scripts/install_skill.py ~/.agents/skills` for personal use. Preserve the whole folder and avoid installing duplicate copies in different discovery locations. Invoke `$ch2025` or ask an applicable question. [Official OpenAI discovery locations](https://learn.chatgpt.com/docs/build-skills).

## Standalone Claude Code skill

From the checkout, run `python3 scripts/install_skill.py /path/to/project/.claude/skills` for a project or `python3 scripts/install_skill.py ~/.claude/skills` for personal use. Invoke `/ch2025` or ask an applicable question. [Official Claude Code documentation](https://code.claude.com/docs/en/skills).

## Other agents and updates

For a host supporting the Agent Skills standard, put the same folder in its documented location. Do not assume it recognises product-specific metadata/commands. Otherwise, use the standalone chat instructions. Format portability does not guarantee browsing, Python or native import support. [Standard format](https://agentskills.io/specification).

The core has no runtime dependency or required MCP/connector. The optional helper requires Python 3.10+ and HTTPS access to the public STAC/object store. Advanced analysis can use the user's established scientific libraries; none are installed automatically.

## Verify, update or remove

The installer copies the complete folder and licence; it never merges with an existing installation. It needs Python 3.10+ but no credentials. Alternatively, extract the ZIP into the chosen skills directory; retain its top-level `ch2025` folder. A successful copy is not proof that a host loaded it.

Open a new chat and invoke `$ch2025` (Codex) or `/ch2025` (Claude Code), for example: “Explain a 3-degree world in Switzerland and cite the official evidence.” Check that the host shows the skill and follows its source links. If absent, check its documented discovery location, workspace settings and duplicate names. Local Claude Code paths do not install a skill into Cowork/cloud sessions; use that surface's account-level setup.

To check the optional helper independently, run `python3 /path/to/installed/ch2025/scripts/ch2025.py products`; it should print eight product families without network access.

For an update, run `git pull --ff-only` in this checkout, move the installed `ch2025` folder to a backup **outside the host's skills directories**, then rerun the installer. This retains any local edits for comparison. To uninstall, remove only that installed `ch2025` folder and start a new chat. ZIP imports in hosted products use that product's update/removal controls.

When authoring, rebuild the generated chat file and ZIP with `python3 scripts/build_release.py`. Keep the folder name consistent with `name: ch2025`.

For plugin updates, refresh the marketplace and update/reinstall the plugin through the host. Codex provides `codex plugin marketplace upgrade ch2025-skills`; Claude Code provides `/plugin marketplace update ch2025-skills` and `/plugin update ch2025@ch2025-skills`. For removal use `codex plugin remove ch2025@ch2025-skills` or `/plugin uninstall ch2025@ch2025-skills`. These affect the plugin installation, not an independently copied standalone folder.
