# Privacy (LGPD/GDPR), IDOR Oracles, Moderation Gates & Audit Report Template

Use these discovery commands, checklists, and the report template when executing **Phase 5 & Phase 6**.

---

## 0. Privacy, IDOR, Moderation & DOM XSS Discovery Playbook (`rg`)

Run these searches to locate UUID oracles, unmoderated broadcast/voice feeds, PII leaks, and DOM XSS sinks:

```bash
# 1. Locate 409/400/404 responses that might leak existing entity UUIDs (UUID Oracles)
rg -n "status_code=409|duplicate_|already_exists"

# 2. Locate PII fields (email, phone, document IDs, raw selfie paths) across serializers & UI tables
rg -n "email|phone|cpf|original_objects|selfie"

# 3. Locate all content moderation checks and compare against public/broadcast/voice endpoints
rg -n "moderation_status|approved|pending|rejected"

# 4. Locate DOM XSS sinks in vanilla JS and React components
rg -n "innerHTML|outerHTML|insertAdjacentHTML|dangerouslySetInnerHTML"
```

---

## 1. UUID Oracles in `409 Conflict` & IDOR Prevention

### The Failure Mode
To help frontend UIs recover from duplicate submissions, backends sometimes return the conflicting entity's UUID inside a `409 Conflict` error detail:
```python
# ❌ VULNERABLE: UUID Oracle!
raise HTTPException(status_code=409, detail=f"duplicate_team_name:{existing_team.id}")
```
Because team/entity names are publicly visible on leaderboards and TVs, any unauthenticated attacker can send `POST /api/teams` with `"name": "<Visible Team Name>"`, receive `409 duplicate_team_name:550e8400-e29b-...`, and immediately obtain the target's secret UUID to mount IDOR attacks (`POST /api/teams/{uuid}/photo`, `/regenerate`, `/calibrate`).

### Required Fix
- Never leak internal UUIDs in unauthenticated `409`, `400`, or `404` responses (`detail="duplicate_team_name"` only).
- Even if a UUID is known, require a cryptographic `X-Resource-Owner-Token` (`HMAC(APP_SIGNING_SECRET, f"owner:{team_id}")`) or admin Bearer token on all state-mutating endpoints (`POST /photo`, `PUT`, `DELETE`).

---

## 2. LGPD / GDPR Data Minimization, Orphaned PII & Input Bounds

### Audit Checklist
1. **Orphaned PII on Partial Transaction Failure & `O(N)` Uniqueness Scans**:
   - Check registration flows that create child records (`create_participant(name, email)`) *before* creating the parent record (`create_team(name)`).
   - If `create_team` fails with `409 duplicate_team_name`, the newly created `participant` documents (containing personal names and emails) remain orphaned in the database forever without consent or a parent team!
   - Also check whether uniqueness checks (`name_key_exists`) call `list_teams()` (performing an `O(N)` full-collection Firestore read scan on every registration!).
   - **Fix**: Query `FieldFilter("name_key", "==", name_key).limit(1)` and reserve/create the parent team *before* persisting `participant_records` (or immediately delete created `participant_id`s in `except DuplicateTeamName`).
2. **PII Leakage in Session Snapshots & Public/Operator APIs**:
   - When archiving finished sessions (`finish_session`) or returning `/api/queue`, `/api/stations`, `/api/search`, or `GET /api/admin/teams` (for `X-App-Role: operator`), strip `email` from `participants[]` and `original_objects` (raw selfie paths) from `assets`.
3. **Unbounded Search, Pydantic Lists & Binary Magic Bytes**:
   - Enforce `limit: int = Query(default=20, ge=1, le=50)` on `/api/search` so attackers cannot dump the database with `?q=a&limit=100000`.
   - Enforce `max_length` on Pydantic lists (`participants`, `frames`), validate image magic bytes (`\xff\xd8\xff` JPEG, `\x89PNG`, `RIFF....WEBP`) in `decode_frame`, and serve media with `X-Content-Type-Options: nosniff`.
4. **Operator UI DOM Minimization**:
   - Do not render raw `{participant.email}` in operator queue/table rows (`ResourceAdminTable.tsx`) where tablets are visible to bystanders or broadcast cameras.

---

## 3. End-to-End Content Moderation, Cross-Station Isolation & Sticky State Cleanup

### The Failure Mode
In live-event and broadcast applications, user-generated team names, participant names, avatars, and AI-generated crests require moderation (`moderation_status == "approved"`). Moderating only the primary scoreboard endpoint fails when:
1. **Unfiltered Secondary, Voice & Fallback Feeds**:
   - `/api/public/calls` ("Next Called Team" banner) or `/api/stations` returns unmoderated team names/crests.
   - `prompt_context._entity_block` feeds unapproved team names or participant first names into the **Gemini Live Audio** loudspeaker voice pipeline!
   - When a physical station (`station-1`) goes idle, the broadcast TV (`/broadcast`) falls back to `candidate_stations = [target_station, "sandbox-sim"]`, accepts calls for *other* stations from `/api/public/calls` (missing `call.get("station_id") == target_station`), or pulls `pending` teams from the global `/api/queue`!
2. **Sticky Frontend/Backend Global Variables**:
   - Broadcast code stores `if t1.get("crest_url"): TEAM_1_CREST_URL = t1.get("crest_url")` when a team has a valid crest, but **fails to reset `TEAM_1_CREST_URL = ""` (`null`)** when the next team's crest is pending/rejected or empty. Result: Team B plays on TV wearing Team A's crest!
3. **DOM XSS via `.innerHTML`**:
   - Injecting `teamName`, `subTitle` (`banner_text`), `predictionLabel`, `predictedWinner`, or `sourceLabel` into `.innerHTML` without HTML entity escaping (`escHtml`) allows `<img src=x onerror=...>` payloads to execute inside operator consoles or broadcast TVs.

### Required Fix Pattern
```python
def safe_public_team_identity(team: dict) -> dict:
    """Apply uniformly across /api/public/sessions, /api/public/calls, prompt_context, and load_session_entities."""
    is_approved = team.get("moderation_status") == "approved"
    short_id = str(team.get("team_id") or team.get("id") or "")[-4:].upper()
    return {
        **team,
        "name": team["name"] if is_approved else f"Team #{short_id}",
        "crest_url": (team.get("crest_url") or team.get("logo_url")) if is_approved else None,
        "photo_url": team.get("photo_url") if is_approved else None,
        "participants": [
            {**p, "name": p["name"] if is_approved else f"Participant {idx + 1}"}
            for idx, p in enumerate(team.get("participants", []))
        ],
    }
```

```javascript
// Always escape dynamic strings before .innerHTML interpolation
function escHtml(val) {
  return String(val ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Always assign crest URL unconditionally so missing/unapproved crests clear the previous session's crest
window.TEAM_1_CREST_URL = (team1 && team1.crest_url) ? team1.crest_url : null;
window.TEAM_2_CREST_URL = (team2 && team2.crest_url) ? team2.crest_url : null;
```

---

## 4. Deliverable Template: Security Audit & Hardening Specification

Structure every comprehensive audit report using this exact template:

```markdown
# 🛡️ Security & Operational Resilience Audit: [Component / Surface Name]

- **Date**: YYYY-MM-DD
- **Target Surface**: [Frontend / Edge Proxy / Backend Service / Google Cloud / GenAI Pipeline]
- **Deployment & Network Topology**: [e.g., 1 managed tablet, shared venue Wi-Fi + 4G CGNAT behind Next.js/FastAPI BFF proxy on Cloud Run / GKE]
- **Overall Risk Posture**: [Critical / High / Moderate — 1-sentence executive summary]

---

## 1. Operational Calibration & Attack-Surface Map
- **Physical Footprint**: [How many devices/screens, who controls them]
- **Network Reality**: [Shared NAT/CGNAT constraints, proxy chain, direct `*.run.app` / GKE Ingress exposure]
- **Anti-Overengineering Calibration**: [What enterprise bloat was deliberately excluded and why]

### Discovered Route, Proxy & Google Cloud Surface Inventory
| Route / Surface | Exposure Layer (`Public` / `BFF Proxy` / `*.run.app` / `GKE Ingress`) | Auth & Rate-Limit Control | Downstream GCP / GenAI Trigger | Risk Verdict |
|---|---|---|---|---|
| `POST /api/register` | Public via `edge-bff` | 4D Rate Limit + `X-Device-Session` | Firestore write + Vertex AI / Gemini | [Pass / P0 / P1] |
| `/operator/api/*` | Credential-Swap BFF (`OPERATOR_SESSION_COOKIE` -> `MASTER_TOKEN`) | `posixpath.normpath` + `(Method, Regex)` + `X-App-Role: operator` | Admin & Station APIs | [Pass / P0 / P1] |

---

## 2. Skeptical Code Verification Table
*Every claim verified against exact repository files and line numbers.*

| # | Claim / Hypothesis | Evidence Inspected (`file:lines`) | What the Code Actually Shows | Verdict & Corrected Severity |
|---|---|---|---|---|
| 1 | [Claim] | [`path/to/file.py#L10-L45`](path/to/file.py#L10-L45) | [Exact code behavior] | **Confirmed P0 / Nuanced P1 / Refuted** |

---

## 3. Prioritized Findings & Hardening Specification

### 🚨 P0 — Critical Blockers (Exploit, Self-DoS, Quota Outage, or Secret Leak)

#### [P0-1] [Finding Title]
- **Vulnerability & Impact**: [Concrete attack scenario or self-inflicted outage mechanism]
- **Affected Files**: [`path/to/file.py`](path/to/file.py)
- **Remediation Pattern**:
  ```python
  # Exact drop-in replacement code
  ```

### ⚠️ P1 — High-Priority Resilience & Privacy Controls (Event-Day Stability & LGPD/GDPR)

#### [P1-1] [Finding Title]
- **Vulnerability & Impact**: [...]
- **Affected Files**: [...]
- **Remediation Pattern**: [...]

### 🔒 P2 — Defense-in-Depth & Long-Run Polish (8h+ Leaks & Edge Hardening)

#### [P2-1] [Finding Title]
- **Vulnerability & Impact**: [...]
- **Affected Files**: [...]
- **Remediation Pattern**: [...]

---

## 4. Automated Security & Resilience Verification Matrix

| Test ID | Category | Scenario / Attack Vector | Expected HTTP Status & Invariant |
|---|---|---|---|
| `SEC-01` | Proxy / Self-DoS | 30 users behind 1 CGNAT IP submit within 5 min | `201 Created` for all 30; `X-Forwarded-For` preserved |
| `SEC-02` | Bot / Device Lock | `curl` `POST` without `GET`-minted device cookie | `403 Forbidden` (`missing_device_session_reload_page`) |
| `SEC-03` | Privilege Escalation | Operator cookie calls `DELETE` or `/live-session` | `403 Forbidden` at edge proxy allowlist |
| `SEC-04` | Quota / Event Loop | 20 rapid calls to signed URL endpoint | Zero extra `signBlob` RPCs after cache warm; loop latency < 15ms |
| `SEC-05` | LGPD / Moderation | Unapproved team on active station & idle fallback | Name masked as `Team #XXXX`, crest cleared, no `email` in JSON |
| `SEC-06` | Secret Leak in Error Logs | Induce Gemini `400`/`429`/`500` error (`?key=AIza...` in URL / `x-goog-api-key` header) | Zero `AIza[0-9A-Za-z_-]{35}` or `key=` tokens in HTTP response, `photo_error` DB field, or `caplog.text` |
```
