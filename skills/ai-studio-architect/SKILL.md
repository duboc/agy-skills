---
name: ai-studio-architect
description: Assess Google AI Studio prototypes and prepare evidence-based migration to Google Cloud production infrastructure. Use for prototype productionization, Cloud Run packaging, SDK/auth migration and scoped infrastructure scripts; not automatic provisioning from README keywords.
---

# AI Studio production architecture

## Inspect before mapping

Read the actual build scripts, package lockfile, application entry points,
API calls, auth flow, persistence and existing deployment configuration. Read
environment variable names from examples; do not print secret values. The
`scripts/parse-requirements.js` helper supplies discovery hints, not verified
requirements: words like user, files or async do not establish IAP, Storage or
Pub/Sub requirements.

Create an inventory with current behavior, evidence, proposed target and reason.
Preserve working auth, hosting and deployment conventions unless migration is
requested. Identify missing constraints that change cost, data location or user
access; resolve routine choices without repeated approvals.

## Select the smallest viable target

Cloud Run can host a unified frontend/backend, but it is not mandatory for every
prototype. Static hosting, existing backends and the user's chosen platform may
already fit. Tier labels are communication aids, not permission to create extra
projects, environments, VPCs or encryption infrastructure.

- Keep privileged model/API calls server-side; do not ship reusable secrets in
  a browser bundle. Verify existing backend behavior before moving code.
- Distinguish consumer sign-in, application sessions and workforce access.
  IAP is an option for appropriate access patterns, not a synonym for all auth.
- Use attached Cloud Run service identity and ADC for Google Cloud access when
  appropriate. Workload Identity Federation is relevant to external workloads;
  do not confuse it with the runtime's attached service account.
- Review current [Google Gen AI SDK guidance](https://github.com/googleapis/js-genai)
  for `@google/genai` and supported Vertex/Gemini API modes. Do not mechanically
  replace one older SDK with another without checking features and versions.
- Distinguish Google Search grounding from a Vertex AI Search datastore; inspect
  the actual tool/configuration before adding services.

Read `references/gcp-service-mapping.md` and
`references/ai-studio-stack-guide.md` for relevant patterns. Validate version-
sensitive examples against current official docs; historical exports do not
define the structure of every AI Studio project.

## Prepare infrastructure artifacts

Use `assets/init-gcp-template.sh` as a starting scaffold, not a ready production
deployment. Populate only verified required services and remove unused sections.
Preserve user-selected project and region; require concrete target values before
executing. Explicit `--project` arguments avoid changing global gcloud state.

Generated scripts must:

1. Validate inputs and prerequisites, distinguish permission errors from missing
   resources, and stop on ambiguous inspection failures.
2. Offer a dry run that prints intended actions without invoking cloud commands
   or reading secrets. Test it with a stub CLI before using real credentials.
3. Check existing resources/configuration before mutation. `--quiet` does not make
   an operation idempotent, and repeating a deploy can create a new revision.
4. Scope IAM to runtime needs and individual resources; preserve unrelated policy
   bindings. Public invocation must be an explicit architectural requirement.
5. Reference Secret Manager values without echoing them. Secret-backed runtime
   environment injection can be valid; the key concern is access and exposure,
   not a blanket ban on environment variables.
6. Print action status truthfully: a dry run is a plan, not completed provisioning.

Provide a Dockerfile/build config only for the selected runtime. Reuse the
existing package manager and lockfile. Identify rollback revision/config and any
data migration that a code rollback cannot reverse.

## Validate and deliver

Run syntax and dry-run checks, build the application, and exercise representative
auth, model, storage and failure paths locally where possible. Inspect the bundle
for accidentally embedded secrets using names/patterns without displaying values.

If deployment is requested, execute against the exact target within existing
authorization; then read configuration back and smoke-test the deployed service.
Generating scripts alone does not authorize provisioning. Report observed results,
unverified cloud behavior, dependency versions and rollback limitations separately.
