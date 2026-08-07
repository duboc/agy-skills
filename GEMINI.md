# Agy Skills Project Context

## Project Overview
This repository contains a collection of reusable, self-contained skills for the [Gemini CLI](https://github.com/google-gemini/gemini-cli). Each skill provides specialized instructions and workflows for the Gemini CLI to execute specific tasks, ranging from code troubleshooting to generating presentations and managing deployments.

## Architecture & Structure
The project is organized into individual skill directories under the `skills/` folder. 

A standard skill directory structure looks like this:
```text
skills/<skill-name>/
├── SKILL.md              (required — entry point with YAML frontmatter)
├── README.md             (required — human-readable docs)
├── references/           (optional — templates, guides, cheat sheets)
│   └── *.md
└── scripts/              (optional — helper scripts the skill can invoke)
    └── *.sh
```

## Installation & Usage
Skills are not "built" or "run" like traditional software; instead, they are installed into the Gemini CLI environment.

- **Native Install:** `gemini skills install https://github.com/duboc/agy-skills.git --path skills/<skill-name>`
- **Script Install (Workspace):** `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- <skill-name>`
- **Script Install (User):** `curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- <skill-name> --scope user`

## Development Conventions
When contributing or modifying skills, strictly adhere to the following rules:

1. **Naming:** Use lowercase `kebab-case` for skill directory names.
2. **SKILL.md:** This is the core file that the Gemini CLI reads as a prompt. It MUST start with YAML frontmatter containing `name` and `description` fields.
    ```yaml
    ---
    name: <skill-name>
    description: <short description>
    ---
    ```
    The `name` in the frontmatter MUST match the directory name exactly.
3. **Scripts:** All executable helper scripts belong in the `scripts/` directory, must be executable (`chmod +x`), and must be portable across macOS and Linux. Do not use hardcoded absolute paths.
4. **References:** Place templates, markdown guides, and other reference materials in the `references/` directory.
5. **Documentation:** Every skill MUST have its own `README.md` with usage examples.
6. **Pull Requests:** Keep changes isolated (one skill per PR). When adding a new skill, remember to update the skills catalog table in the root `README.md`.

## AI Agent Instructions
- When asked to create or update a skill, always adhere to the `skills/<skill-name>/` structure.
- Ensure the `SKILL.md` frontmatter is perfectly formatted and the content acts as an effective prompt.
- After creating a new skill script, always make sure it is executable (`chmod +x`).
- Remember to update the root `README.md` to include any new skill you create in the available skills table.