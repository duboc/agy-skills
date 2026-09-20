# Declarative JSON Schema & Google Engineering Archetypes

This reference defines the JSON schema consumed by `scripts/build_gdoc_spec.py` and the 4 standard multi-tab archetypes used for Google-style engineering documentation.

---

## 1. Complete JSON Schema (`spec.json`)

```json
{
  "title": "📖 [Document Title]",
  "tabs": [
    {
      "title": "📌 1. [Tab Title]",
      "blocks": [
        {
          "type": "title",
          "title": "Main Heading Inside Tab",
          "subtitle": "Subtitle / Context Line • Environment or Scope",
          "metadata": [
            {"label": "Status", "value": "DRAFT / HOMOLOGAÇÃO", "style": "badge_amber"},
            {"label": "Version", "value": "v1.0", "style": "badge_blue"},
            {"label": "Target", "value": "Production Cutover Ready", "style": "badge_green"}
          ]
        },
        {
          "type": "callout",
          "theme": "amber",
          "title": "⚠️ Callout Banner Title",
          "lines": [
            "• Bullet or line 1 inside the shaded callout box.",
            "• Bullet or line 2 highlighting critical invariants or environment cutover rules."
          ]
        },
        {
          "type": "heading",
          "level": 1,
          "text": "1. Section Heading (H1 has bottom accent rule)"
        },
        {
          "type": "paragraph",
          "segments": [
            ["Regular text followed by ", "normal"],
            ["bold emphasis", "bold"],
            [", an inline ", "normal"],
            ["code_pill()", "code"],
            [", an HTTP badge ", "normal"],
            [" POST ", "badge_blue"],
            [", a status badge ", "normal"],
            [" HTTP 200 ", "badge_green"],
            [", or a ", "normal"],
            ["clickable link", "link", "https://example.com"]
          ]
        },
        {
          "type": "bullets",
          "items": [
            [
              ["Step 1 (", "bold"],
              ["POST /api/v1/resource", "code"],
              ["): Description of step 1.", "normal"]
            ],
            [
              ["Zero-Blocking Fallback: ", "bold"],
              ["Never block user journeys on non-critical upstream failures.", "normal"]
            ]
          ]
        },
        {
          "type": "table",
          "header_bg": "#1E3A8A",
          "headers": ["Column 1 (Rendered Bold/Code)", "Column 2", "Column 3"],
          "rows": [
            ["id_or_param_1", "string", "Detailed explanation of parameter 1"],
            ["id_or_param_2", "boolean", "Detailed explanation of parameter 2"]
          ]
        },
        {
          "type": "code_block",
          "label": "JSON / TypeScript / Python / cURL — Block Label",
          "code": "{\n  \"key\": \"value\"\n}"
        }
      ]
    }
  ]
}
```

### Supported Block Types & Styles

| Block `type` | Required Fields | Optional Fields | Visual Rendering in Google Docs |
| :--- | :--- | :--- | :--- |
| `title` | `title` | `subtitle`, `metadata` | `22pt Google Sans Bold` + `11.5pt` subtitle + bottom border rule + optional status badge bar |
| `heading` | `level` (`1..3`), `text` | — | `H1` (`16.5pt` navy `#1E3A8A` + bottom border), `H2` (`13.5pt`), `H3` (`11.5pt`) |
| `callout` | `title`, `lines` (`string[]`) | `theme` (`amber` \| `blue` \| `green` \| `red`) | Continuous shaded box with `3.5pt` solid left accent bar and `10pt` horizontal indent |
| `paragraph` | `segments` or `text` | `bullet` (`bool`), `space_above`, `space_below` | Rich inline typography with inline pills and hyperlinks |
| `bullets` | `items` (`list` of segment lists or strings) | — | Bulleted list supporting mixed bold, inline `code`, and badges per bullet |
| `table` | `headers` (`string[]`), `rows` (`string[][]`) | `header_bg` (default `#1E3A8A`) | Native table with dark navy header, white bold text, `#F8FAFC` zebra rows, and `Roboto Mono` first column for IDs |
| `code_block` | `label`, `code` | — | Dark `#334155` header pill + `#F8FAFC` shaded container + `#3B82F6` left border + `Roboto Mono 9.5pt` + muted comment lines (`//`, `#`) |

---

## 2. The 4 Google Engineering Spec Archetypes

Choose the multi-tab layout that matches the engineering problem domain:

### Archetype A: API & Partner Integration Spec (External/Internal Consumers)
Best when specifying REST/gRPC endpoints, webhooks, hardware totem/kiosk integrations, or BFF contracts.
- **Tab 1 (`📌 1. Visão Geral & Ambientes` / `Overview & Environments`)**:
  - Environment Status Callout (`Amber` if Staging/Testing URL will change at Go-Live; mandate `.env` parameterization).
  - End-to-End Architecture & Core Invariants (e.g., Zero-Blocking UX fallback, idempotency, routing rules such as App URL vs. Admin URL).
  - Environment Matrix Table (`Dev/Staging`, `Production`, `Prohibited Routes`).
  - Authentication Table (Headers, Bearer tokens, mTLS/API Keys) & Official Enum/ID Catalog Table.
- **Tab 2 (`🔌 2. Especificação da API` / `API Contracts & Schemas`)**:
  - Step-by-step Endpoints with `badge_blue` (`POST`/`GET`), Summary Table, Request Body (`code_block`), Success/Error Response Payloads (`code_block`), and UX/Business Rule Callouts (`green` for UX tips, `amber` for edge-case handling).
- **Tab 3 (`💻 3. Exemplos de Código` / `Reference Code & SDKs`)**:
  - Environment configuration snippet (`.env`) with fallback defaults.
  - Copy-pasteable, production-safe reference implementations in **JavaScript/TypeScript (`fetch`)**, **Python (`requests`)**, and **cURL**.
- **Tab 4 (`✅ 4. Checklist & Homologação` / `QA & Cutover Plan`)**:
  - End-to-End Test Cases Table (`CT-01`..`CT-05`: Happy path, unregistered/fallback path, artifact recording, async/late binding, network timeout resilience).
  - Production Cutover Checklist Table (`⬜ Pendente` items for `.env` switch, smoke testing, public asset reachability).

---

### Archetype B: Google Design Doc / RFC (System Architecture)
Best when proposing a new service, distributed system architecture, data pipeline, or cross-team technical RFC.
- **Tab 1 (`📌 1. Contexto, Escopo & Goals`)**:
  - Metadata Bar (`Author`, `Status: DRAFT/IN REVIEW`, `Reviewers`).
  - Executive Summary & Problem Statement.
  - Explicit **Goals** vs. **Non-Goals** Table (crucial Google engineering discipline).
- **Tab 2 (`🏗️ 2. Arquitetura & Modelo de Dados`)**:
  - High-Level System Components & Data Flow steps.
  - Storage / Database Schema Table & State Machine transitions.
  - Internal API / Protobuf / Event Schemas (`code_block`).
- **Tab 3 (`⚖️ 3. Alternativas & Trade-offs`)**:
  - Comparative Decision Matrix Table (`Option A (Chosen)` vs. `Option B` vs. `Do Nothing` across Latency, Cost, Complexity, and Operational Risk).
  - Failure Modes, Rate Limiting, and Quota/Capacity Estimation.
- **Tab 4 (`🛡️ 4. Segurança, Observabilidade & Rollout`)**:
  - Security & Privacy (IAM, PII/LGPD, AuthN/AuthZ).
  - SLIs, SLOs, Metrics & Alerts Table.
  - Phased Rollout & Rollback Plan.

---

### Archetype C: Product & Engineering Feature Spec (PRD + Tech Spec)
Best when bridging Product Management requirements with Engineering execution.
- **Tab 1 (`📌 1. Problema, Personas & Métricas`)**: Context, Target Users, North Star & Guardrail Metrics Table, MoSCoW Scope Table (`Must`, `Should`, `Won't`).
- **Tab 2 (`🎨 2. Jornada de UX & Critérios de Aceite`)**: User Flows, Given/When/Then Acceptance Criteria Table, UI Copy & Empty/Error States.
- **Tab 3 (`⚙️ 3. Especificação Técnica & Contratos`)**: Backend/Frontend architecture, API payloads, Analytics/Telemetry Events Table.
- **Tab 4 (`🚀 4. Feature Flags, QA & Lançamento`)**: Rollout stages (`Dev` ➔ `Dogfood` ➔ `10%` ➔ `100%`), A/B Test setup, QA Sign-off Checklist.

---

### Archetype D: Operational Runbook & Cutover Playbook
Best for live-event operations, production migrations, or on-call incident response.
- **Tab 1 (`📌 1. Topologia, Contatos & SLAs`)**: Architecture overview, Environment URLs, Escalation Matrix Table.
- **Tab 2 (`🔄 2. Procedimento de Cutover / Deploy`)**: Pre-flight checks, Timed Step-by-Step Execution commands (`code_block`), Smoke Verification.
- **Tab 3 (`🚨 3. Diagnóstico & Troubleshooting`)**: Symptom ➔ Root Cause ➔ Mitigation Table, Quick Diagnostic `cURL`/CLI commands.
- **Tab 4 (`⏪ 4. Plano de Rollback & Checklist`)**: Immediate Rollback Triggers, Step-by-Step Rollback commands, Post-Mortem template.
