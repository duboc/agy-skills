# AI Studio Architect

A Agy skill for converting Google AI Studio Build mode prototypes into production-grade infrastructure on Google Cloud Platform.

## What It Does

This skill reads your AI Studio project, identifies all infrastructure requirements, and generates complete GCP deployment scripts. It handles the full migration path:

1. **Project scanning** — Reads README.md, package.json, source files, and environment variables to detect infrastructure needs.
2. **Service mapping** — Maps detected patterns to GCP services: Vertex AI, Cloud Run, Firestore, Cloud Storage, Secret Manager, and more.
3. **Automatic tier detection** — Determines the deployment tier (Starter/Standard/Production/Enterprise) from the scan results. No questions asked — hosting is always Cloud Run (unified), AI calls always go through a server-side proxy.
4. **Script generation** — Produces an idempotent `init-gcp.sh` with all `gcloud` commands, API enablement, IAM bindings, and resource creation.
5. **SDK migration** — Guides the migration from `@google/generative-ai` (client-side) to `@google-cloud/vertexai` (server-side).
6. **Additional artifacts** — Generates Dockerfile, cloudbuild.yaml, CORS configs, and Terraform files based on the detected tier.

## When Does It Activate?

The skill activates when you ask Agy to deploy AI Studio projects or set up GCP infrastructure. It scans the project, auto-detects the right deployment tier, and generates everything — no setup questions required.

| Trigger | Example |
|---------|---------|
| Deploy AI Studio project | "Deploy this AI Studio app to Google Cloud" |
| Generate GCP infrastructure | "Generate a gcloud setup script for this project" |
| Migrate to production | "Convert this prototype to production on GCP" |
| Set up Cloud Run | "Set up Cloud Run and Vertex AI for this app" |
| Scan for requirements | "Scan this README and tell me what GCP services I need" |

## Topics Covered

| Area | Details |
|------|---------|
| **AI Studio Stack** | React/Angular + TypeScript + Vite + Tailwind + Agy API |
| **Service Detection** | Pattern matching for Firestore, Storage, Vertex AI, Cloud Run, Secret Manager, Auth, Pub/Sub, Cloud Build |
| **Auto Tier Detection** | Automatically selects Starter, Standard, Production, or Enterprise based on scan results |
| **SDK Migration** | `@google/generative-ai` to `@google-cloud/vertexai` code transformation |
| **Infrastructure Scripts** | Idempotent `init-gcp.sh` with dry-run support |
| **IAM & Security** | Least-privilege Service Accounts, Workload Identity, Secret Manager |
| **CI/CD** | Cloud Build pipelines with GitHub triggers |
| **Deployment Tiers** | Starter, Standard, Production, Enterprise |
| **Frontend Hosting** | Cloud Run (unified) or Cloud Storage + CDN |

## Installation

### Option A: Agy native

```bash
agy skills install https://github.com/duboc/agy-skills.git --path skills/ai-studio-architect
```

### Option B: One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- ai-studio-architect
```

For user-scope installation (available across all projects):

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- ai-studio-architect --scope user
```

### Option C: Manual

```bash
cp -r skills/ai-studio-architect ~/.gemini/config/skills/ai-studio-architect
```

## Usage Examples

Once installed, the skill activates when you ask Agy to deploy or migrate AI Studio projects.

### Scan and deploy an AI Studio export

```
I exported this project from AI Studio Build mode. Scan it and set up
everything I need on Google Cloud to run it in production.
```

### Generate infrastructure script from README

```
Read the README.md in this project and generate an init-gcp.sh script
with all the gcloud commands I need.
```

### Migrate Agy API calls to Vertex AI

```
This app uses @google/generative-ai with an API key. Help me migrate
it to use Vertex AI with a Service Account on Cloud Run.
```

### Production-tier deployment

```
Set up a production deployment for this AI Studio app with Cloud Build
CI/CD, monitoring, and a staging environment.
```

### Quick scan with the helper script

```
Run the parse-requirements script on this project and tell me what
GCP services are needed.
```

## Included References

| File | Description |
|------|-------------|
| **gcp-service-mapping.md** | Detailed GCP service configurations with gcloud commands, IAM roles, and code examples for Vertex AI, Cloud Run, Firestore, Storage, Secret Manager, Cloud Build, and Monitoring |
| **ai-studio-stack-guide.md** | Complete AI Studio Build mode stack documentation with migration patterns for geminiService.ts, environment variables, static assets, AI grounding, and GCP-native production stack |

## Included Scripts

| File | Description |
|------|-------------|
| **parse-requirements.js** | Node.js scanner that reads project files and detects GCP service requirements. Outputs summary, JSON, or shell script format |

### Script Usage

```bash
# Summary report (default)
node scripts/parse-requirements.js --path /path/to/project

# JSON output (for programmatic use)
node scripts/parse-requirements.js --path /path/to/project --format json

# Shell script with API enable commands
node scripts/parse-requirements.js --path /path/to/project --format shell
```

## Included Assets

| File | Description |
|------|-------------|
| **init-gcp-template.sh** | Base template for the generated `init-gcp.sh` with sections for project setup, API enablement, Service Account, Firestore, Storage, Secret Manager, Cloud Run, and output summary |
