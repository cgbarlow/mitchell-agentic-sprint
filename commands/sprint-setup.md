---
description: One-time pre-flight setup for a Mitchell Agentic Sprint. Verifies campaign-mode + six-animals are installed, offers to install the Mitchell profile (re-skins Gandalf as 🧢 Mitchell), optionally onboards the NotebookLM MCP bolt-on, and records the chosen configuration to .sprint/setup.md.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Sprint Setup

`/sprint-setup` is a one-time pre-flight per project. It verifies the prerequisite plugins are installed, offers to install the Mitchell profile so the framing mentor (campaign-mode's Gandalf) appears as 🧢 Mitchell during the Sprint, and optionally onboards the NotebookLM MCP bolt-on. Run this once before your first `/sprint-start`.

The Sprint runs without the NotebookLM bolt-on — choosing to skip is fine and explicitly supported. Skip if you don't want to authenticate to Google or you're working without internet.

Follow these steps in order.

## Step 1: Verify prerequisite plugins (`campaign-mode`, `six-animals`)

Per [ADR-003](../docs/adrs/ADR-003-Sibling-Plugin-Shape.md), MAS depends on `campaign-mode` and `six-animals`. Both must be installed for the Mini Council orchestration and the Discovery / Vertical / Framework flows that invoke `gandalf-agent`.

Use Bash to check whether the plugins are visible to Claude Code. Two acceptable forms:

- Marketplace install: `claude plugin list` shows both `campaign-mode` and `six-animals`
- Clone install: `${HOME}/.claude/plugins/` (or the project's `.claude/plugins/`) contains both directories

Use Bash:

```bash
ls "${HOME}/.claude/plugins/" 2>/dev/null
```

(If neither path resolves, instruct the user how to install both.)

**If both plugins are present:** record the versions and continue to Step 2.

**If either is missing:** tell the user (use plain language, do not reference command flags they didn't ask for):

> Mitchell Agentic Sprint depends on **campaign-mode** and **six-animals**. One or both is missing.
>
> Install in a Claude Code session:
>
> ```
> /plugin marketplace add cgbarlow/skills
> /plugin install six-animals@cgbarlow-skills
> /plugin install campaign-mode@cgbarlow-skills
> ```
>
> Then re-run `/sprint-setup`.

Stop here.

## Step 2: Install the Mitchell profile (offer; default yes)

The Sprint's framing mentor is campaign-mode's Gandalf NPC. By default, MAS re-skins Gandalf as **🧢 Mitchell** — Scott Mitchell as the founder-mentor persona, asking the questions he'd ask in a real conversation. This matches the product's framing without changing Gandalf's core role (mentor, frames, doesn't rescue).

The profile pack ships at `${CLAUDE_PLUGIN_ROOT}/profile-packs/mitchell-agentic-sprint/gandalf.md`. Installing copies it to `.campaign/profiles/gandalf.md` in the user's project — the path that campaign-mode's `gandalf-agent` reads at invocation time per its SKILL.md.

### Step 2.1: Check for existing profile

Use Glob to check whether `.campaign/profiles/gandalf.md` already exists in the user's project root.

**If it exists:** read its frontmatter `skin-name` and surface to the user via `AskUserQuestion`:

> A Gandalf profile already exists at `.campaign/profiles/gandalf.md` (\`skin-name: {existing}\`).
>
> The Mitchell Agentic Sprint ships a **🧢 Mitchell** profile that fits the product's framing. Want to switch to it for this project?

Options:
1. **Keep the existing profile** — make no changes; record `gandalf-profile: preexisting ({existing skin-name})` in setup.md
2. **Overwrite with Mitchell** — back up the existing profile to `.campaign/profiles/gandalf.md.bak.{date}`, then install Mitchell
3. **Cancel setup** — stop here; no other changes

**If it does not exist:** use `AskUserQuestion`:

> The Sprint installs a **🧢 Mitchell** profile by default — re-skins Gandalf as Scott Mitchell, the founder-mentor persona. You can decline if you want the default Gandalf appearance.

Options:
1. **Install Mitchell (Recommended)** — copy the profile pack file to `.campaign/profiles/gandalf.md`
2. **Skip — keep default Gandalf** — make no changes; record `gandalf-profile: declined`

### Step 2.2: Apply the choice

If the user picked install or overwrite:

```bash
mkdir -p .campaign/profiles
# If overwriting, back up first:
[ -f .campaign/profiles/gandalf.md ] && mv .campaign/profiles/gandalf.md .campaign/profiles/gandalf.md.bak.$(date +%Y-%m-%d)
cp "${CLAUDE_PLUGIN_ROOT}/profile-packs/mitchell-agentic-sprint/gandalf.md" .campaign/profiles/gandalf.md
```

Confirm to the user:

> 🧢 Mitchell profile installed to `.campaign/profiles/gandalf.md`. The Discovery / Vertical / Framework framing voice will appear as **🧢 Mitchell** for this project.

Continue to Step 3.

## Step 3: Choose NotebookLM MCP path

Use `AskUserQuestion`:

> **NotebookLM MCP bolt-on (optional, recommended).**
>
> The Sprint can use Google NotebookLM as a synthesis layer for Steps 3–6 (theme map, expert framework, positioning whitespace, audio overview). It improves quality on those steps and aligns with the concept's "verbatim quotes only" rule.
>
> The bolt-on requires:
> - One Python install (`pip install notebooklm-mcp-cli`)
> - One browser-based Google login (`nlm login`)
> - One MCP config command (`nlm setup add claude-code`)
>
> Without the bolt-on, the Sprint uses Claude-only synthesis for Steps 3–5; Step 6's audio overview is unavailable. Everything else works.

Options:

1. **Install the bolt-on now (Recommended)** — proceed to Step 4
2. **Skip and use Claude-only synthesis** — proceed to Step 5
3. **I already configured it** — proceed to Step 4 (the verify path is the same)

## Step 4: Onboard or verify NotebookLM MCP

Run a quick verification first:

```bash
which nlm 2>/dev/null && nlm login --check 2>&1
```

**If `nlm` is on PATH and `nlm login --check` reports authenticated:** the bolt-on is configured. Continue to Step 5.

**If `nlm` is missing:**

Tell the user (use the appropriate command for their tooling):

> Install `notebooklm-mcp-cli`. One of:
>
> ```bash
> # via pip (universal)
> pip install notebooklm-mcp-cli
>
> # via uv (recommended if you use uv)
> uv tool install notebooklm-mcp-cli
>
> # via pipx
> pipx install notebooklm-mcp-cli
> ```
>
> Then run `nlm login` to complete the browser-based handshake. Cookies persist locally; re-run `/sprint-setup` once authenticated.

Use Bash to attempt installation only if the user explicitly confirms the install command via `AskUserQuestion`. **Do not auto-install** — the install touches their global tool environment and they should approve consciously.

After the install, instruct the user to run:

```bash
nlm login            # browser-based; one-time
nlm setup add claude-code   # configures Claude Code MCP
nlm doctor           # diagnose any remaining issues
```

The user runs `nlm setup add claude-code` themselves — Claude Code's MCP config is per-user. Once complete, the user sets the `MAS_NOTEBOOKLM_MCP=1` signal in their shell or Claude Code settings so MAS commands pick it up.

Verify:

```bash
nlm doctor
```

**If `nlm doctor` is clean:** continue to Step 5.

**If issues remain:** surface the doctor output to the user. Common issues: cookies expired (re-run `nlm login`), MCP config not picked up by Claude Code (restart Claude Code), profile mismatch (`nlm login --profile <name>`).

## Step 5: Record setup decisions

Use Bash to ensure `.sprint/` exists:

```bash
mkdir -p .sprint
```

Use the Write tool to create `.sprint/setup.md` with this content (substituting values):

```markdown
---
schema-version: 1
campaign-mode: {version, e.g. 0.4.8}
six-animals: {version, e.g. 0.1.2}
gandalf-profile: {installed | declined | preexisting}
gandalf-skin-name: {Mitchell | <existing skin-name> | null}
notebooklm-mcp: {available | unavailable | declined}
notebooklm-version: {version-or-null}
date: {today's date}
---

# Sprint Setup

This file records the prerequisites and bolt-on decisions for this project's Sprint. It is read by step commands to decide whether to route synthesis through NotebookLM or fall back to Claude-only.

## Plugins

- campaign-mode: {version}
- six-animals: {version}

## Gandalf NPC profile

**Status: {installed | declined | preexisting}**
**Active skin-name: {Mitchell | <existing> | none — default Gandalf}**

{If installed:}
The Mitchell profile is active. Discovery / Vertical / Framework framing appears as **🧢 Mitchell**. The profile lives at `.campaign/profiles/gandalf.md`. Remove that file to revert to the default Gandalf appearance.

{If declined:}
The user declined the Mitchell profile. The framing voice appears as the default 🧙 Gandalf. Re-run `/sprint-setup` and pick "Install Mitchell" if you change your mind.

{If preexisting:}
A Gandalf profile was already present at `.campaign/profiles/gandalf.md`. The user kept it. Re-run `/sprint-setup` and pick "Overwrite with Mitchell" to switch.

## NotebookLM MCP bolt-on

**Status: {available | unavailable | declined}**

{If available:}
The bolt-on is configured. Steps 3–6 will route synthesis through NotebookLM where it adds value.

{If unavailable:}
The bolt-on is not currently configured. The Sprint will use Claude-only synthesis for Steps 3–5. Step 6's audio overview is unavailable. Re-run `/sprint-setup` to configure later — the Sprint state is unaffected by this choice.

{If declined:}
The user explicitly declined the NotebookLM bolt-on for this project. The Sprint will use Claude-only synthesis. Re-run `/sprint-setup` and pick "Install the bolt-on now" if you change your mind.

## Re-running setup

This file is rewritten every time `/sprint-setup` runs. The Sprint state in `.sprint/sprint.md` is not modified by setup. The Mitchell profile at `.campaign/profiles/gandalf.md` is not removed by re-running setup — manage it manually if you want to revert.
```

## Step 6: Confirm and exit

Tell the user:

> Setup complete. Configuration recorded in `.sprint/setup.md`.
>
> {If everything green (campaign-mode + six-animals + Mitchell profile + notebooklm-mcp):} You're ready to start a Sprint via `/sprint-start`. Mitchell will frame Discovery; the full bolt-on suite is active.
>
> {If campaign-mode + six-animals + Mitchell profile present, notebooklm-mcp missing:} You're ready to start a Sprint via `/sprint-start`. Mitchell will frame Discovery; synthesis steps will use Claude-only mode.
>
> {If campaign-mode + six-animals present, Mitchell profile declined:} You're ready to start a Sprint via `/sprint-start`. Default 🧙 Gandalf will frame Discovery.

Use `AskUserQuestion`:

1. **Start a Sprint now** — invoke `/sprint-start`
2. **Done — exit setup** — return to normal conversation

---

## Injected Context

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Plugin shape spec (SPEC-003-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-003-A-Plugin-Manifest.md`
- NotebookLM integration spec (SPEC-006-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-006-A-NotebookLM-MCP.md`
- ADR-006 (NotebookLM rationale): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/ADR-006-NotebookLM-MCP-Integration.md`
- Mitchell profile pack: !`echo ${CLAUDE_PLUGIN_ROOT}/profile-packs/mitchell-agentic-sprint/gandalf.md`
