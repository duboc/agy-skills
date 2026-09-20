# Application, Google Cloud & Generative AI Security Audit (`app-security-audit`)

Perform end-to-end attack-surface discovery, route & BFF proxy mapping, Google Cloud & GenAI FinOps auditing, induced API-key error-log leak testing, async event-loop resilience checks, and LGPD/GDPR privacy assessments for Cloud Run, GKE, Vertex AI / Gemini, operator console, kiosk, and live-event applications.

---

## Features

- **Phase 0 Automated Attack-Surface Discovery**: Ready-to-run `ripgrep` (`rg`) playbooks to inventory every FastAPI/Flask/Next.js/Express route, BFF reverse-proxy rule, Cloud Run `--allow-unauthenticated` origin (`*.run.app`), GKE public `Ingress`, Firestore/GCS surface, and Vertex AI / Gemini SDK sink.
- **Topology Calibration (Anti-Overengineering)**: Calibrates controls to real physical device footprints (managed operator tablets, self-service kiosks, 8-hour unattended broadcast TVs) and network topology (shared venue Wi-Fi NAT & mobile 4G/5G CGNAT) so security defenses never self-DoS legitimate traffic.
- **BFF Proxy, Credential-Swap & 4D CGNAT Rate Limiting**: Prevents `X-Forwarded-For` stripping self-DoS, blocks prefix-based credential-swap privilege escalations (`posixpath.normpath` + `(Method, Exact Regex)` allowlists + `X-App-Role: operator`), and implements 4-dimensional CGNAT-safe rate limiting (`GET`-minted signed device cookie + `X-Device-Session` fallback, canonical email cooldown, split IP Burst vs Sustained buckets, and QR presence tokens).
- **AI FinOps, Quota DoS & Induced Gemini API Key Error-Log Leak Testing**:
  - Protects multi-call Gemini / Imagen / Live API pipelines against Denial-of-Wallet (`X-Resource-Owner-Token`, terminal state locks, attempt caps, semaphores).
  - Eliminates IAM `signBlob` & GCE Metadata Server quota exhaustion via thread-safe in-memory Signed URL TTL caching and OAuth credential reuse.
  - Prevents & tests **Gemini API Key (`?key=AIza...` / `x-goog-api-key`) leakage in induced error logs and stack traces** (`httpx.HTTPStatusError`, `install_secret_redaction`, `SecretRedactingFilter`, `sanitize_exception`, and `pytest` `caplog` fault-injection recipes).
  - Defends Visual & Live Audio/TTS pipelines against multi-modal prompt injection and client-payload early-return bypasses.
- **Async Event-Loop & 8h+ Kiosk/Broadcast Resilience**: Detects FastAPI `async def` synchronous I/O freezes, hidden `GET` hardware mutations, `POST` auto-retry toggle bugs, dual-screen `auto-finish` races, 30 fps `activeBlobUrl`/`loadingBlobUrl` memory leaks, `?mode=audio` WebSocket bandwidth waste, and zombie viewer queues.
- **LGPD/GDPR Privacy, UUID Oracles & End-to-End Moderation**: Eliminates `409 Conflict` UUID oracles, orphaned participant PII, unmoderated fallback/voice leaks (`Team #XXXX` masking), cross-station contamination, and `.innerHTML` DOM XSS.

---

## Skill Structure

```text
app-security-audit/
├── SKILL.md                                                 # Main 7-phase discovery & security audit workflow
├── README.md                                                # Skill overview, structure, and usage examples
└── references/
    ├── proxy-cgnat-and-auth-patterns.md                     # Route discovery, BFF credential swaps, 4D CGNAT rate limits, WebSocket auth
    ├── ai-finops-async-and-kiosk-resilience.md              # GenAI FinOps, signBlob cache, Gemini error-log key redaction + pytest recipe, async def & 8h+ TV leaks
    └── privacy-idor-moderation-and-report-template.md       # UUID oracles, LGPD/GDPR minimization, moderation gates & deliverable template
```

---

## Usage Examples

Trigger this skill by asking:
- *"Run a full security audit and attack-surface discovery on this repository."*
- *"Map all exposed routes, BFF proxy rules, Cloud Run origins, and Gemini API calls in this project."*
- *"Audit our `/register` and `/operator` endpoints for CGNAT Wi-Fi rate-limit issues and proxy privilege escalation."*
- *"Add a fault-injection test that induces a Gemini API error and verifies the `AIza...` API key never leaks in application logs or error responses."*
- *"Faça uma avaliação de segurança completa (Cloud Run, Gemini, proxy, LGPD e resiliência de painéis/kiosk)."*

---

## Installation

### Workspace Scope

Install to `.agents/skills/app-security-audit/` in your current project:

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- app-security-audit
```

### User Scope (Global)

Install to `~/.gemini/config/skills/app-security-audit/` for availability across all projects:

```bash
curl -fsSL https://raw.githubusercontent.com/duboc/agy-skills/main/scripts/install.sh | bash -s -- app-security-audit --scope user
```
