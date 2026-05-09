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
> **Where to install it:** the install must happen on your **own machine** in a regular terminal. The package (`notebooklm-mcp-cli`) requires Python ≥3.11 — Cowork's sandbox runs Python 3.10, so the install **cannot** run inside Cowork. CLI users on a host with Python ≥3.11 can install in-session. Once installed locally and \`nlm setup add claude-code\` is run, Cowork's MCP integration picks up the server automatically when you next open it.
>
> Without the bolt-on, the Sprint uses Claude-only synthesis for Steps 3–5; Step 6's audio overview is unavailable. Everything else works.

Options:

1. **I want the bolt-on — show me the install instructions** — proceed to Step 4
2. **Skip and use Claude-only synthesis** — proceed to Step 5
3. **I already configured it** — proceed to Step 5 (no install work needed)

## Step 4: NotebookLM install instructions

Tell the user (do NOT auto-install in Cowork — it will fail with a Python version error):

> Run these in a regular terminal on **your own machine** — not in Cowork's sandbox (which runs Python 3.10 and cannot install `notebooklm-mcp-cli`, which requires Python ≥3.11).
>
> ```bash
> # 1. Install the unified CLI + MCP server (one of these)
> pip install "notebooklm-mcp-cli>=0.6.6"
> # or: uv tool install notebooklm-mcp-cli
> # or: pipx install notebooklm-mcp-cli
>
> # 2. One-time browser-based Google login
> nlm login
>
> # 3. Wire up Claude's MCP integration
> nlm setup add claude-code
>
> # 4. Verify
> nlm doctor
> ```
>
> Cookies persist locally; you only run \`nlm login\` once. After \`nlm setup add claude-code\` completes, **restart Claude Cowork / Claude Code** to pick up the new MCP server.
>
> **CLI users on a Python ≥3.11 host**: if you'd like, I can run steps 1, 3, and 4 in this session via Bash. Step 2 (\`nlm login\`) you must run yourself — it opens a browser.

If Bash is available **and** Python ≥3.11 is on PATH **and** the user explicitly confirms via `AskUserQuestion`, attempt the install. Verify Python first:

```bash
python3 --version 2>&1 | grep -E "Python 3\.(1[1-9]|[2-9][0-9])"
```

If that grep matches (Python 3.11+), proceed:

```bash
pip install "notebooklm-mcp-cli>=0.6.6"
```

Otherwise stop and tell the user to install on their own machine instead — Python is too old in this environment.

Then prompt the user to run `nlm login` themselves. After they confirm completion, run:

```bash
nlm setup add claude-code
nlm doctor
```

Surface any `nlm doctor` output.

After the user confirms install completion (or that they've done it out-of-band):

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
