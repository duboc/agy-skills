# Agy Skills

A collection of reusable skills for Agy (`agy`). Each skill is self-contained and can be installed independently.

---

## Available Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [software-troubleshooter](skills/software-troubleshooter/) | Structured code inspection and troubleshooting with diagnostic reports | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- software-troubleshooter` |
| [adk-developer](skills/adk-developer/) | Build single-agent and multi-agent systems with Google's ADK (Python, Java, Go, TypeScript) | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- adk-developer` |
| [agent-engine-deploy](skills/agent-engine-deploy/) | Deploy, manage, and query ADK agents on Vertex AI Agent Engine | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- agent-engine-deploy` |
| [agent-engine-sessions-memory](skills/agent-engine-sessions-memory/) | Manage sessions and long-term memory for agents on Vertex AI Agent Engine | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- agent-engine-sessions-memory` |
| [agent-engine-ops](skills/agent-engine-ops/) | Monitor, trace, secure, and evaluate agents on Vertex AI Agent Engine | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- agent-engine-ops` |
| [zen-presenter](skills/zen-presenter/) | Generate MARP presentation decks following Presentation Zen principles with Google identity styling, self-contained HTML output, and optional PowerPoint export | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- zen-presenter` |
| [ai-studio-architect](skills/ai-studio-architect/) | Convert AI Studio Build mode prototypes to production on GCP with auto-generated infrastructure scripts | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- ai-studio-architect` |
| [clarity-presenter](skills/clarity-presenter/) | Generate MARP decks using SCQA narrative + assertion-evidence design with dual-perspective slides, Google identity styling, and optional PowerPoint export | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- clarity-presenter` |
| [developer-growth-analysis](skills/developer-growth-analysis/) | Analyze Agy session history to surface development patterns, friction points, and growth opportunities with curated resources | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- developer-growth-analysis` |
| [google-ads-funnel](skills/google-ads-funnel/) | Funnel-as-Code workflows for Google Ads account audits, spend analysis, creative testing, and conversion diagnostics via the Ads API | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- google-ads-funnel` |
| [using-git-worktrees](skills/using-git-worktrees/) | Create isolated git worktrees with smart directory selection, gitignore safety checks, dependency setup, and baseline test verification | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- using-git-worktrees` |
| [webapp-testing](skills/webapp-testing/) | Toolkit for testing local web applications using Playwright with server lifecycle management, screenshots, and console log capture | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- webapp-testing` |
| [writing-plans](skills/writing-plans/) | Generate detailed TDD implementation plans with atomic tasks, exact file paths, and complete code before writing any code | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- writing-plans` |
| [spring-boot-upgrader](skills/spring-boot-upgrader/) | Migrate Spring Boot applications to 4.0 with auto-detected migration paths, phased upgrade plans, and Jackson 3 migration | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- spring-boot-upgrader` |
| [ux-copywriter](skills/ux-copywriter/) | Write effective, accessible, and conversion-optimized microcopy for user interfaces | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- ux-copywriter` |
| [design-system-management](skills/design-system-management/) | Manage design tokens, component libraries, and pattern documentation for scalable, consistent UIs | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- design-system-management` |
| [design-critique](skills/design-critique/) | Evaluate designs for usability, visual hierarchy, consistency, and adherence to design principles | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- design-critique` |
| [feature-spec](skills/feature-spec/) | Write structured product requirements documents (PRDs) with problem statements, user stories, requirements, and success metrics | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- feature-spec` |
| [system-design](skills/system-design/) | Design systems, services, and architectures with explicit trade-off analysis | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- system-design` |
| [documentation](skills/documentation/) | Write and maintain technical documentation, READMEs, API docs, runbooks, and architecture docs | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- documentation` |
| [visual-explainer](skills/visual-explainer/) | Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- visual-explainer` |
| [html-to-pptx](skills/html-to-pptx/) | Convert MARP HTML slides into fully editable PowerPoint files with native text boxes, lists, tables, and embedded images | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- html-to-pptx` |
| [zen-pitch](skills/zen-pitch/) | Research a market or domain, build a requirements spine, and compile a persuasive Presentation Zen pitch deck | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- zen-pitch` |
| [technical-drawing](skills/technical-drawing/) | Create precise, dimensioned technical drawings in SVG with orthographic views, cotas, and FOV cones | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- technical-drawing` |
| [cloud-architecture-diagram](skills/cloud-architecture-diagram/) | Draw a deployed system as a Google Cloud reference architecture: official product icons, a numbered request path, hover explanations, and an optional stepped slideshow | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- cloud-architecture-diagram` |
| [app-security-audit](skills/app-security-audit/) | End-to-end attack-surface discovery, BFF proxy & CGNAT rate-limit auditing, Google Cloud & Gemini FinOps/quota checks, induced API-key error-log leak testing, async event-loop resilience, and LGPD/GDPR privacy assessments | `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh \| bash -s -- app-security-audit` |

### Database Migration (Sybase to Cloud Spanner)

Sybase migration skills have moved to their own repository: [sybase-migration-toolkit](https://github.com/duboc/sybase-migration-toolkit)

## Installation

### Method 1: One-liner with curl (Recommended)

The install script downloads only the requested skill from GitHub (no git clone needed).

**Workspace scope** (`.agents/skills/<name>/` in your current directory):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- <skill-name>
```

**User scope** (`~/.gemini/config/skills/<name>/` for global availability):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- <skill-name> --scope user
```

### Method 2: Manual download

1. Download or clone this repository.
2. Copy the desired skill folder into your skills directory:
   - **Workspace Scope:** `cp -r skills/software-troubleshooter .agents/skills/software-troubleshooter`
   - **User Scope:** `cp -r skills/software-troubleshooter ~/.gemini/config/skills/software-troubleshooter`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on creating and submitting new skills.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
