---
description: Pre-flight configuration for a Mitchell Agentic Sprint. Verifies prerequisites, installs the Mitchell profile, and registers the NotebookLM MCP bolt-on if available. Works in both Claude Cowork (no terminal) and Claude Code CLI. Auto-invoked by /sprint-start on first run; call directly only to re-configure.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Sprint Setup

Pre-flight per project. **You don't normally need to run this directly** — `/sprint-start` calls it automatically on the first run in a new project. Call `/sprint-setup` directly only when you want to **re-configure** an existing project.

This command is designed to work in **both Claude Cowork (no shell) and Claude Code CLI**. Where the CLI can run install commands in-session via Bash, Cowork users complete those installs in their own terminal *outside* Cowork. The setup command guides both paths.

The Sprint runs without the NotebookLM bolt-on — choosing to skip is fine and explicitly supported. Skip if you don't want to authenticate to Google or you're working without internet.

## Step 1: Acknowledge prerequisites

The Sprint depends on **campaign-mode** and **six-animals** per [ADR-003](../docs/adrs/ADR-003-Sibling-Plugin-Shape.md). If you installed `mitchell-agentic-sprint` via the [`cgbarlow/skills`](https://github.com/cgbarlow/skills) marketplace, both dependencies are already in place because the marketplace lists them.

There is no portable way to verify plugin installation from inside a slash command (Cowork has no shell, and `${HOME}/.claude/plugins/` is not project-relative). Trust the marketplace install. If a later step fails because `gandalf-agent` is not found, install the prerequisites via:

```
/plugin marketplace add cgbarlow/skills
/plugin install six-animals@cgbarlow-skills
/plugin install campaign-mode@cgbarlow-skills
/reload-plugins
```

Continue to Step 2.

## Step 2: Install the Mitchell profile (offer; default install)

The Sprint's framing mentor is campaign-mode's Gandalf NPC. By default, MAS re-skins Gandalf as **🧢 Mitchell** — Scott Mitchell as the founder-mentor persona, asking the questions he'd ask in a real conversation.

The profile pack ships at `${CLAUDE_PLUGIN_ROOT}/profile-packs/mitchell-agentic-sprint/gandalf.md`. Installing copies it to `.campaign/profiles/gandalf.md` in the user's project — the path that campaign-mode's `gandalf-agent` reads at invocation per its Speaker Identification section.

### Step 2.1: Check for existing profile

Use Glob to check whether `.campaign/profiles/gandalf.md` already exists in the user's project root.

**If it exists:** read its frontmatter `skin-name` (use the Read tool). Surface to the user via `AskUserQuestion`:

> A Gandalf profile already exists at `.campaign/profiles/gandalf.md` (\`skin-name: {existing}\`).
>
> The Mitchell Agentic Sprint ships a **🧢 Mitchell** profile that fits the product's framing. Want to switch to it for this project?

Options:
1. **Keep the existing profile** — make no changes; record `gandalf-profile: preexisting ({existing skin-name})` in setup.md
2. **Overwrite with Mitchell** — back up the existing profile (Read the existing file → Write to `.campaign/profiles/gandalf.md.bak.{YYYY-MM-DD}`), then install Mitchell
3. **Cancel setup** — stop here; no other changes

**If it does not exist:** use `AskUserQuestion`:

> The Sprint installs a **🧢 Mitchell** profile by default — re-skins Gandalf as Scott Mitchell, the founder-mentor persona. You can decline if you want the default Gandalf appearance.

Options:
1. **Install Mitchell (Recommended)** — Read the profile pack and Write it to `.campaign/profiles/gandalf.md`
2. **Skip — keep default Gandalf** — make no changes; record `gandalf-profile: declined`

### Step 2.2: Apply the choice (Cowork-compatible — no Bash required)

If the user picked install or overwrite:

1. **(Optional, only if Bash is available)** Ensure the directory exists:

   ```bash
   mkdir -p .campaign/profiles
   ```

   In Cowork or any environment without Bash, skip this — the Write tool creates parent directories automatically.

2. **(Only if overwriting)** Read the existing `.campaign/profiles/gandalf.md`, then Write it to `.campaign/profiles/gandalf.md.bak.{YYYY-MM-DD}`.

3. Read `${CLAUDE_PLUGIN_ROOT}/profile-packs/mitchell-agentic-sprint/gandalf.md`.

4. Write that content to `.campaign/profiles/gandalf.md`.

Confirm to the user:

> 🧢 Mitchell profile installed to `.campaign/profiles/gandalf.md`. The Discovery / Vertical / Framework framing voice will appear as **🧢 Mitchell** for this project.

Continue to Step 3.

## Step 3: Choose NotebookLM MCP path

Use `AskUserQuestion`:

> **NotebookLM MCP bolt-on (optional, recommended).**
>
> The Sprint can use Google NotebookLM as a synthesis layer for Steps 3–6 (theme map, expert framework, positioning whitespace, audio overview). It improves quality on those steps and aligns with the concept's "verbatim quotes only" rule.
>
> **Where to install it:** `notebooklm-mcp-cli` requires Python ≥3.11. Cowork's sandbox runs Python 3.10, **but** [`uv`](https://docs.astral.sh/uv/) can provision Python 3.11 on demand inside the sandbox by downloading prebuilt binaries — so an in-Cowork install via `uv tool install notebooklm-mcp-cli` usually works. The setup command tries that first. If the sandbox blocks it (network restrictions, filesystem permissions), fall back to installing on your own machine in a regular terminal. CLI users on a Python ≥3.11 host can install via plain pip in-session. After install, **restart Claude Cowork or Claude Code** to pick up the new MCP server.
>
> Without the bolt-on, the Sprint uses Claude-only synthesis for Steps 3–5; Step 6's audio overview is unavailable. Everything else works.

Options:

1. **Install it now** — proceed to Step 4 (Claude attempts the install in this session via `uv`; falls back to host-machine instructions if the sandbox blocks it)
2. **Skip — use Claude-only synthesis** — proceed to Step 5
3. **I already have it configured** — proceed to Step 5 (no install work needed)

## Step 4: NotebookLM install — try `uv` first

The recommended install path uses [`uv`](https://docs.astral.sh/uv/) because uv provisions Python 3.11 itself by downloading prebuilt binaries — sidestepping Cowork's Python 3.10 sandbox limitation. It also works fine on plain Python ≥3.11 hosts (CLI sessions).

### Step 4.1: Attempt the install

If Bash is available, ask the user via `AskUserQuestion` whether to run the install in-session (the user must run `nlm login` themselves regardless — it opens a browser). If they confirm, run:

```bash
# Install uv if it's not already there (idempotent)
command -v uv >/dev/null 2>&1 || pip install --quiet uv

# Install the unified CLI + MCP server. uv provisions Python 3.11
# automatically if the host Python is older.
uv tool install "notebooklm-mcp-cli>=0.6.6"
```

If `uv tool install` succeeds, continue to Step 4.2.

**If `uv tool install` fails** (network blocks, sandbox restrictions, or any other error), surface the error to the user and fall back to host-machine install. Tell them:

> The in-session install didn't work — likely Cowork's sandbox blocks something `uv` needs (downloading the Python 3.11 binary, or running it). Run these on **your own machine** in a regular terminal instead:
>
> ```bash
> # one of (in order of preference):
> uv tool install "notebooklm-mcp-cli>=0.6.6"
> # or, on a Python ≥3.11 host:
> pip install "notebooklm-mcp-cli>=0.6.6"
> # or:
> pipx install notebooklm-mcp-cli
> ```

If Bash is **not** available (Cowork without sandbox, or restricted CLI), skip the in-session attempt and go straight to the host-machine instructions above.

### Step 4.2: Login + MCP wire-up

The user runs these themselves — `nlm login` opens a browser and the user has to authenticate to Google:

```bash
nlm login                      # browser-based; one-time
nlm setup add claude-code      # wires up Claude's MCP integration
nlm doctor                     # verify
```

After `nlm setup add claude-code` completes, **restart Claude Cowork or Claude Code** to pick up the new MCP server. Cookies persist locally; subsequent sessions use the saved login.

### Step 4.3: Confirm

After the user reports completion:

Use `AskUserQuestion`:

> Confirm install status:

Options:
1. **Done — all steps completed and `nlm doctor` is clean** — record `notebooklm-mcp: available`
2. **I'll come back to this later** — record `notebooklm-mcp: unavailable`; the Sprint will use Claude-only synthesis until the user re-runs `/sprint-setup` after install
3. **Skip — I don't want the bolt-on** — record `notebooklm-mcp: declined`

Continue to Step 5.

## Step 5: Record setup decisions

Use the Write tool to create `.sprint/setup.md` (Write creates parent directories automatically). Substitute the values from the user's choices:

```markdown
---
schema-version: 1
campaign-mode: 0.4.8                                     # pinned compat as of 2026-05-08
six-animals: 0.1.2                                       # pinned compat as of 2026-05-08
gandalf-profile: {installed | declined | preexisting}
gandalf-skin-name: {Mitchell | <existing skin-name> | null}
notebooklm-mcp: {available | unavailable | declined}
notebooklm-version: {version-or-null}
date: {today's date}
---

# Sprint Setup

This file records the prerequisites and bolt-on decisions for this project's Sprint. It is read by step commands to decide whether to route synthesis through NotebookLM or fall back to Claude-only.

## Plugins

- campaign-mode: 0.4.8 (pinned)
- six-animals: 0.1.2 (pinned)

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

## Step 6: Confirm and exit (skip if invoked from /sprint-start)

If invoked directly (not from `/sprint-start`), tell the user:

> Setup complete. Configuration recorded in `.sprint/setup.md`.
>
> {If everything green (Mitchell profile + notebooklm-mcp):} You're ready to start a Sprint via `/sprint-start`. Mitchell will frame Discovery; the full bolt-on suite is active.
>
> {If Mitchell profile present, notebooklm-mcp missing or declined:} You're ready to start a Sprint via `/sprint-start`. Mitchell will frame Discovery; synthesis steps will use Claude-only mode.
>
> {If Mitchell profile declined:} You're ready to start a Sprint via `/sprint-start`. Default 🧙 Gandalf will frame Discovery.

Use `AskUserQuestion`:

1. **Start a Sprint now** — invoke `/sprint-start`
2. **Done — exit setup** — return to normal conversation

If invoked from `/sprint-start` (the auto-setup path), skip this confirmation entirely — `/sprint-start` will continue with its own next step.

---

## Injected Context

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Plugin shape spec (SPEC-003-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-003-A-Plugin-Manifest.md`
- NotebookLM integration spec (SPEC-006-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-006-A-NotebookLM-MCP.md`
- ADR-006 (NotebookLM rationale): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/ADR-006-NotebookLM-MCP-Integration.md`
- Mitchell profile pack: !`echo ${CLAUDE_PLUGIN_ROOT}/profile-packs/mitchell-agentic-sprint/gandalf.md`
