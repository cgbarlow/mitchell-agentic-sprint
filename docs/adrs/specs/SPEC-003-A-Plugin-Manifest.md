# SPEC-003-A: Plugin Manifest and Marketplace Declaration

| Field | Value |
|-------|-------|
| **Specification ID** | SPEC-003-A |
| **Parent ADR** | [ADR-003](../ADR-003-Sibling-Plugin-Shape.md) |
| **Version** | 1.0 |
| **Status** | Active |
| **Last Updated** | 2026-05-08 |

---

## Overview

Defines the shape of `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` for `mitchell-agentic-sprint`. The shapes mirror campaign-mode's manifests, with MAS-specific identification and the campaign-mode + six-animals dependency declaration in the marketplace file.

## `plugin.json`

```json
{
  "name": "mitchell-agentic-sprint",
  "description": "AI-led 6-step sprint that walks an AI builder through validating one idea — vertical, buyers, framework, positioning — to a sales deck, outreach plan, and pre-seed investor deck. Adversarial by default. Output is artifacts, not product.",
  "version": "0.1.0",
  "author": {
    "name": "Chris Barlow"
  }
}
```

Field rules:
- `name` matches the repo name and the marketplace plugin entry
- `version` follows SemVer (Protocol 5/6); pre-release builds use `0.1.0.dev0` or similar in `pyproject.toml` only — `plugin.json` carries the published version
- `author` may also list Scott Mitchell as a contributing author once a stable release pattern is set; v0.1.0 lists Chris as the implementing author

## `marketplace.json`

Optional — only required if MAS is published as its own marketplace entry. For v0.1.0 we declare it because MAS depends on two plugins from different marketplaces (campaign-mode + six-animals) and the manifest is the cleanest way to express that.

```json
{
  "name": "mitchell-agentic-sprint-marketplace",
  "metadata": {
    "description": "Mitchell Agentic Sprint plugin and its prerequisites (campaign-mode + six-animals).",
    "version": "0.1.0"
  },
  "owner": {
    "name": "Chris Barlow",
    "url": "https://github.com/cgbarlow"
  },
  "plugins": [
    {
      "name": "six-animals",
      "description": "Six psychologically-grounded team role agents (Bear, Cat, Owl, Puppy, Rabbit, Wolf) plus Simon as educator/supervisor. Prerequisite for MAS advisory layer.",
      "source": {
        "source": "url",
        "url": "https://github.com/cgbarlow/simons-six-animals.git"
      },
      "author": { "name": "Dr. Simon McCallum" },
      "license": "CC-BY-SA-4.0",
      "keywords": ["team-roles", "collaboration", "animals", "agents"]
    },
    {
      "name": "campaign-mode",
      "description": "Quest-based extension for AI-assisted work. Three NPC agents (Gandalf, Dragon, Guardian) provide mentorship, adversarial testing, and quality gates. Prerequisite for MAS NPC infrastructure.",
      "source": {
        "source": "url",
        "url": "https://github.com/cgbarlow/campaign-mode.git"
      },
      "author": { "name": "Chris Barlow" },
      "license": "CC-BY-SA-4.0",
      "keywords": ["quest", "campaign", "npcs", "mentorship", "adversarial-testing", "quality-gates"]
    },
    {
      "name": "mitchell-agentic-sprint",
      "description": "AI-led 6-step sprint that walks an AI builder through validating one idea to investor-conversation-ready artifacts. Adversarial by default.",
      "source": {
        "source": "url",
        "url": "https://github.com/cgbarlow/mitchell-agentic-sprint.git"
      },
      "author": { "name": "Chris Barlow" },
      "license": "CC-BY-SA-4.0",
      "keywords": ["sprint", "validation", "buyer-interviews", "investor-deck", "anti-sycophancy"]
    }
  ]
}
```

## Pinned dependency versions

For v0.1.0 we tested against:

| Plugin | Version | Verified |
|---|---|---|
| campaign-mode | 0.4.8 | 2026-05-08 |
| six-animals | 0.1.2 | 2026-05-08 |

Future MAS versions must document compatibility shifts in CHANGELOG.md.

## Acceptance criteria

This spec is fulfilled when:
- `.claude-plugin/plugin.json` exists in the repo root with the structure above
- `.claude-plugin/marketplace.json` exists with both prerequisite plugins listed
- `gh repo view cgbarlow/mitchell-agentic-sprint` description matches `plugin.json` description
- A user can install MAS, campaign-mode, and six-animals via the marketplace and have all three resolve
