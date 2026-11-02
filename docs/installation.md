# Installation and compatibility

The canonical package is `skills/ch2025-swiss-climate/`. Its `SKILL.md` contains standard YAML `name`/`description` metadata and Markdown instructions; supporting files use relative paths. This follows the [Agent Skills specification](https://agentskills.io/specification). Optional `agents/openai.yaml` supplies UI metadata for supporting OpenAI hosts, without imposing a dependency on other hosts.

## Ordinary chat

1. Open [CH2025_CHAT.md](../chat/CH2025_CHAT.md).
2. Upload the file to your chat, or paste its contents as instructions.
3. Say: “Use these CH2025 instructions for my Swiss climate questions. What does a 3-degree world mean for Switzerland?”

The generated file includes the core instructions, references and public links. A chat that cannot read uploads may require pasted text. The host decides tool availability and instruction priority; uploading a document does not create a system-level instruction or guarantee adherence. Current values and exact product retrieval need live tools or supplied public evidence. No terminal or Python is needed for explanations.

## ChatGPT or Claude with native skills

Use [the skill ZIP](../releases/ch2025-swiss-climate.zip) with the host's documented import facility, where available. It contains one top-level skill folder. Installation is separate in each host; a GitHub download does not register a skill everywhere.

OpenAI documents skills for ChatGPT/Codex, with standalone skills and plugin distribution having different availability: [Build skills](https://learn.chatgpt.com/docs/build-skills). Claude documents custom skills across products, with setup/tool access depending on the surface: [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). Check those current pages for account/workspace requirements. Native installation in every product has not been tested here.

## Codex

For project use, copy the folder to `.agents/skills/ch2025-swiss-climate/`. For personal use, use `~/.agents/skills/ch2025-swiss-climate/`. Preserve the whole folder and avoid installing duplicate copies in different discovery locations. Invoke `$ch2025-swiss-climate` or ask an applicable question. [Official OpenAI discovery locations](https://learn.chatgpt.com/docs/build-skills).

## Claude Code

For project use, copy the folder to `.claude/skills/ch2025-swiss-climate/`. For personal use, use `~/.claude/skills/ch2025-swiss-climate/`. Invoke `/ch2025-swiss-climate` or ask an applicable question. [Official Claude Code documentation](https://code.claude.com/docs/en/skills).

## Other agents and updates

For a host supporting the Agent Skills standard, put the same folder in its documented location. Do not assume it recognises product-specific metadata/commands. Otherwise, use the standalone chat instructions. Format portability does not guarantee browsing, Python or native import support. [Standard format](https://agentskills.io/specification).

The core has no runtime dependency or required MCP/connector. The optional helper requires Python 3.10+ and HTTPS access to the public STAC/object store. Advanced analysis can use the user's established scientific libraries; none are installed automatically.

To update, fetch repository changes and deliberately replace your installed copy. When authoring, rebuild the generated chat file and ZIP with `python3 scripts/build_release.py`. Keep the folder name consistent with `name: ch2025-swiss-climate`.
