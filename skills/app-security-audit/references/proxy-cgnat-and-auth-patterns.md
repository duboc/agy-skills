# Route Discovery, Edge Proxy, Credential-Swap & CGNAT/Wi-Fi Rate-Limiting Reference

Use these discovery commands, checklists, and production-ready patterns when executing **Phase 0, Phase 1, and Phase 2** (Attack-surface discovery, Google Cloud ingress mapping, BFF proxies, public registration endpoints, and operator consoles).

---

## 0. Automated Route, Proxy & Google Cloud Surface Discovery Playbook

Never rely solely on frontend navigation menus to decide what to audit. Attackers enumerate backend routers, OpenAPI schemas, Cloud Run `*.run.app` origins, and Kubernetes Ingress rules directly.

### A. Code-Level Route & Proxy Discovery Commands (`rg`)

Run these commands at the start of every audit to build a complete **Route & Proxy Differential Inventory**:

```bash
# 1. FastAPI / Starlette / Flask HTTP & WebSocket endpoints
rg -n "@(app|router|bp)\.(get|post|put|delete|patch|websocket|route)|app\.(include_router|mount)"

# 2. Next.js (App & Pages Router) & Express routes
rg -n "export async function (GET|POST|PUT|DELETE|PATCH)|app\.(get|post|put|delete|use)\("

# 3. Auto-generated documentation, metrics & debug/hardware endpoints often left enabled in prod
rg -n "docs_url|redoc_url|openapi_url|/metrics|/raw_feed|/calib_frame|/calib_feed|/seed|/debug"

# 4. BFF / Reverse-Proxy route matching & credential injection (look for dangerous prefix matches!)
rg -n "startsWith|startswith|posixpath\.normpath|X-Internal-Proxy-Token|X-App-Role|Authorization.*Bearer"

# 5. Google Cloud Run, GKE Ingress, and Public URL exposure
rg -n "run\.app|allow-unauthenticated|ingress\.yaml|gateway\.yaml|ClusterIP|LoadBalancer|NodePort"
```

### B. Building the Route & Proxy Differential Matrix
Cross-reference every discovered backend route against the BFF/Edge Proxy to spot **Shadow Endpoints** and **Credential-Swap Escalations**:

| Surface Layer | What to Map | Classic Vulnerability Uncovered |
|---|---|---|
| **Public Edge / SPA (`/register`, `/broadcast`)** | Public `GET`/`POST` routes, QR entry params (`?v=`), WebSocket viewers (`/ws/viewer`) | Missing `X-Forwarded-For` (Self-DoS), flat IP rate limits blocking Venue Wi-Fi/CGNAT, `POST` minting new device cookies |
| **Credential-Swapping BFF (`/operator`, `/api/ops/*`)** | Routes where the proxy validates a staff cookie (`OPERATOR_SESSION_COOKIE`) and injects `Authorization: Bearer MASTER_TOKEN` | Prefix allowlist (`path.startsWith('/api/admin/teams')`) exposing `DELETE`, `/regenerate?force=true`, `/assets`, or `/live-session` (`GEMINI_API_KEY` leak) |
| **Direct Cloud Origin (`https://*.run.app`)** | Cloud Run services deployed with `--allow-unauthenticated` and `--ingress=all` | JSON responses or image URLs leak `https://core-api-xyz.run.app`, letting attackers call the backend directly and bypass the edge proxy |
| **GKE / K8s Public Ingress (`ingress.yaml`)** | Path-based routing rules on External Application Load Balancers | Internal microservices (`/voice-worker-1..5`, `/vision-inference-api`, `WS /ws/ingest`) exposed to the public internet instead of `ClusterIP` |
| **Unlinked Hardware / Debug Routes** | `/raw_feed`, `/calib_frame`, `/openapi.json`, `/api/teams/refresh` | Unauthenticated `GET` requests that mutate camera/hardware state or trigger cluster-wide fanout |

---

## 1. Proxy Header Stripping & Self-DoS Prevention

### The Failure Mode
When a public application is served behind an edge proxy or BFF (`edge-bff`, Next.js API route, Nginx, Cloudflare Worker), the proxy makes an internal HTTP request to the backend (`http://api:8000` or Cloud Run internal URL).
- **Bug 1 (Self-DoS)**: If the proxy does not append `X-Forwarded-For`, `request.client.host` on the backend resolves to the proxy container's single internal IP (`10.x.x.x`). Any per-IP rate limiter on the backend will count **every user in the world as a single IP** and lock out the entire application after 5–30 requests.
- **Bug 2 (Broken Custom Auth)**: If the proxy only forwards `Cookie` and `Content-Type`, custom security headers sent by the browser (`X-Venue-Token`, `X-Resource-Owner-Token`, `X-Device-Session`, `X-Kiosk-Token`) are silently stripped at the edge.

### Required Fix Pattern (Edge Proxy Forwarding)

```python
# Edge Proxy / BFF forwarding helper
FORWARDED_SECURITY_HEADERS = (
    "X-Venue-Token",
    "X-Resource-Owner-Token",
    "X-Device-Session",
    "X-Kiosk-Token",
)

def build_upstream_headers(request: Request, internal_proxy_token: str) -> dict[str, str]:
    headers = {
        "X-Internal-Proxy-Token": internal_proxy_token,
    }
    # 1. Preserve client IP chain for downstream rate limiters
    client_ip = request.client.host if request.client else "unknown"
    prior_xff = request.headers.get("x-forwarded-for")
    headers["X-Forwarded-For"] = f"{prior_xff}, {client_ip}" if prior_xff else client_ip

    # 2. Explicitly forward custom security headers
    for hdr in FORWARDED_SECURITY_HEADERS:
        val = request.headers.get(hdr)
        if val:
            headers[hdr] = val
    return headers
```

---

## 2. Direct Backend Origin Bypass (`*.run.app` Exposure)

### The Failure Mode
Even when an edge proxy enforces authentication or rate limiting, cloud platforms (e.g., Cloud Run `https://core-api-xyz.run.app`) often expose a public URL by default, and backend responses (such as image URLs or JSON metadata) frequently leak this origin URL to the browser. An attacker can inspect the Network tab and hit `https://core-api-xyz.run.app/api/...` directly, bypassing the edge proxy entirely.

### Required Fix Pattern (Mutual Proxy Token + Safe Client IP Extraction)

```python
import hmac
from fastapi import Header, HTTPException, Request

def verify_edge_proxy(
    request: Request,
    x_internal_proxy_token: str = Header(default=""),
) -> str:
    """Reject direct backend calls that bypassed the edge proxy and return real client IP."""
    if not INTERNAL_PROXY_TOKEN or not hmac.compare_digest(x_internal_proxy_token, INTERNAL_PROXY_TOKEN):
        raise HTTPException(status_code=403, detail="direct_backend_access_forbidden")
    # Only trust X-Forwarded-For AFTER proving the request came from our trusted proxy
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        # Leftmost IP added by the outer ingress/LB is the true client IP
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
```

---

## 3. 4-Dimensional Rate Limiting (Venue Wi-Fi & 4G/5G CGNAT Safe)

### Why Flat Per-IP Limits Fail in Real Life
At live events, stadiums, conferences, offices, or on mobile 4G/5G networks (Carrier-Grade NAT / CGNAT), **50 to 500 legitimate users share 1 public IPv4 address**. A naive `5 requests / 10 minutes per IP` rule blocks legitimate user #6 with `429 Too Many Requests`.

Conversely, shared registration kiosks submit dozens of registrations from a **single browser and single IP**.

### The 4-Dimensional Rate-Limiting Architecture

| Layer | Identifier | Threshold | Purpose & Edge-Case Handling |
|---|---|---|---|
| **L1: Signed Device Session** | `HttpOnly` cookie (`__Host-dev_sid`) + `X-Device-Session` header fallback (signed with `APP_SIGNING_SECRET`) | `3 submissions / 15 min` per device | Isolates each phone on shared Wi-Fi/CGNAT. **Must be minted ONLY on `GET`**, never on `POST`! Bypassed if valid `X-Kiosk-Token` header is present. |
| **L2: Canonical Identity** | Normalized email (`email.strip().lower()`) or phone | `2 registrations / 30 min` per identity | Prevents re-registering the same person across multiple devices. |
| **L3: Split Per-IP Buckets** | Trusted client IP | **Burst**: `6 req / 10s`<br>**Sustained**: `30 req / 5 min` | **Burst** stops automated `curl` scripts immediately; **Sustained** allows 30 human groups on the same venue Wi-Fi/CGNAT to register smoothly. |
| **L4: Physical Presence + Global Cap** | QR token (`?v=<token>` -> `X-Venue-Token`) + `asyncio.Semaphore(6)` | Valid rotating token + max 6 concurrent pipelines | Blocks remote internet attackers who haven't scanned the physical venue QR code and caps cloud spend. |

### Critical Loophole to Avoid: Never Mint Device Sessions on `POST`
If a middleware mints a new device session whenever a request arrives without a cookie, an attacker running `for i in {1..500}; do curl -X POST ...; done` (without `-b cookies.txt`) gets a **brand-new `device_id` on every `POST`** and completely bypasses Layer 1!

```python
import hashlib
import hmac
import os
import secrets
import time
from fastapi import HTTPException, Request

APP_SIGNING_SECRET = os.environ.get("APP_SIGNING_SECRET", "")
DEVICE_TTL_SECONDS = 3600 * 12

def mint_device_session(secret: str = APP_SIGNING_SECRET) -> str:
    """Call ONLY on initial GET /register page load."""
    device_id = secrets.token_urlsafe(16)
    ts = str(int(time.time()))
    payload = f"{device_id}.{ts}"
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:32]
    return f"{payload}.{sig}"

def require_device_session_on_post(request: Request, secret: str = APP_SIGNING_SECRET, kiosk_secret: str = "") -> str:
    """Call on POST /api/register. NEVER mint a new token here."""
    # 1. Shared Kiosk Exemption
    kiosk_hdr = request.headers.get("x-kiosk-token", "")
    if kiosk_secret and kiosk_hdr and hmac.compare_digest(kiosk_hdr, kiosk_secret):
        return f"kiosk:{hashlib.sha256(kiosk_hdr.encode()).hexdigest()[:12]}"

    # 2. Check HttpOnly cookie first, then X-Device-Session fallback (for iOS/Android QR WebViews)
    token = request.cookies.get("app_dev_sid") or request.headers.get("x-device-session", "")
    if not token:
        raise HTTPException(status_code=403, detail="missing_device_session_reload_page")

    parts = token.split(".")
    if len(parts) != 3:
        raise HTTPException(status_code=403, detail="invalid_device_session")
    device_id, ts_str, sig = parts
    if not device_id:
        raise HTTPException(status_code=403, detail="invalid_device_session")
    expected_sig = hmac.new(secret.encode(), f"{device_id}.{ts_str}".encode(), hashlib.sha256).hexdigest()[:32]
    if not hmac.compare_digest(sig, expected_sig):
        raise HTTPException(status_code=403, detail="forged_device_session")
    try:
        issued_at = int(ts_str)
    except ValueError as exc:
        raise HTTPException(status_code=403, detail="malformed_device_session_timestamp") from exc
    now = int(time.time())
    if now - issued_at > DEVICE_TTL_SECONDS or issued_at > now + 60:
        raise HTTPException(status_code=403, detail="expired_device_session")
    return device_id

def canonical_email(raw_email: str) -> str:
    """Normalize email for Layer-2 cooldown so user+1@example.com or u.s.e.r@example.com cannot bypass limits."""
    clean = (raw_email or "").strip().lower()
    if "@" not in clean:
        return clean
    local, domain = clean.split("@", 1)
    local = local.split("+", 1)[0]
    if domain in ("gmail.com", "googlemail.com"):
        local = local.replace(".", "")
        domain = "gmail.com"
    return f"{local}@{domain}"
```

### Physical QR Token Hygiene (Preventing Referer & Screenshot Leaks)
When embedding `?v=<venue_token>` (or `?token=`) in a physical QR code or TV URL:
1. On page load, JS reads `new URLSearchParams(location.search).get('v')`, saves it to `sessionStorage.setItem('venue_token', v)`, and **immediately scrubs the URL bar** with `window.history.replaceState({}, '', location.pathname)` + `<meta name="referrer" content="no-referrer">` so screenshots or `Referer` headers on external image loads never leak the token.
2. Subsequent `fetch()` calls send `headers: { 'X-Venue-Token': sessionStorage.getItem('venue_token') }`.

---

## 4. Credential-Swap Escalation, `posixpath.normpath` & Role-Scoped UI/Backend (`X-App-Role`)

### The Failure Mode
Edge proxies often authenticate an operator with a lower-privilege session cookie (`OPERATOR_SESSION_COOKIE`, role `staff`) and then proxy requests to internal backends by injecting the **Master Admin Bearer Token** (`Authorization: Bearer ${API_AUTH_TOKEN}`).

If the proxy guards routes with **prefix matching** (e.g. `path.startsWith("/api/admin/teams")` or `path.startsWith("/api/ops/capture/api/devices")`) or fails to normalize dot-segments (`..`):
1. **Destructive Admin Sub-Routes & Raw PII Exposed**: Any operator with the `OPERATOR` password can call `DELETE /api/admin/teams/{id}`, `POST /api/admin/teams/{id}/regenerate?force=true` (unlimited GenAI spend), `POST /api/admin/teams/unretire-all`, or `GET /api/admin/teams/{id}/assets` (signing URLs for raw user selfies).
2. **Accidental Live-Event Sabotage via Shared React Components**: Mounting a shared `<ResourceAdminTable />` component in `/operator` without `mode="operator"` renders `Delete Team`, batch `Force Regenerate Selected`, and `SeedDemoEntities` buttons on a floor tablet during a busy live event.
3. **Secret Exfiltration via Internal Sub-Routes**: Under `/api/ops/capture/api/devices/{id}/live-session`, if the proxy forwards requests using `INTERNAL_DEVICE_TOKEN`, an operator can fetch the raw `GEMINI_API_KEY` from the upstream `device-controller` service!

### Required Fix Pattern: `posixpath.normpath` + `(Method, Compiled Regex)` Allowlist + `X-App-Role`
1. **Always normalize the path with `posixpath.normpath`** before checking the allowlist AND use the normalized path when forwarding upstream (blocking `/api/stations/../admin/teams/123/assets`).
2. **Inject `X-App-Role: operator`** so the backend enforces role-specific business invariants:
   - On `POST /api/admin/teams/{id}/regenerate`: force `payload.force = False` when `X-App-Role == "operator"` (only retry `failed` assets).
   - On `POST /api/stations/{id}/finish`: force `score = None, metrics = None` (always use authoritative telemetry score) and reject mutations on `station_id == "sandbox-sim"`.
   - On `POST /api/ops/capture/api/devices/{id}/command`: restrict `name in ("start_session", "stop_session", "extend_session")` (`1 <= seconds <= 300`) on physical stations `station-1..4`.

```python
import posixpath
import re
from fastapi import HTTPException

# Explicitly enumerate ONLY the exact (HTTP_METHOD, REGEX) pairs the operator UI needs.
OPERATOR_ROUTE_ALLOWLIST: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("GET",    re.compile(r"^/api/queue$")),
    ("POST",   re.compile(r"^/api/queue$")),
    ("DELETE", re.compile(r"^/api/queue/[a-zA-Z0-9_-]+$")),
    ("GET",    re.compile(r"^/api/stations$")),
    ("POST",   re.compile(r"^/api/stations/station-[1-4]/(?:call|confirm|no-show|swap-sides|finish|release)$")),
    ("GET",    re.compile(r"^/api/search$")),
    ("GET",    re.compile(r"^/api/ops/snapshots/station-[1-4]$")),
    ("GET",    re.compile(r"^/api/ops/capture/api/devices$")),  # Blocks /live-session secret leak!
    ("POST",   re.compile(r"^/api/ops/capture/api/devices/[a-zA-Z0-9_-]+/command$")),
    ("GET",    re.compile(r"^/api/admin/teams(?:/[a-zA-Z0-9_-]+/sessions)?$")),  # Blocks DELETE and /assets!
    ("POST",   re.compile(r"^/api/admin/teams/[a-zA-Z0-9_-]+/(?:moderation|regenerate)$")),
)

def normalize_and_assert_operator_route(method: str, raw_path: str) -> str:
    """Normalize path to prevent '..' traversal bypasses and verify (Method, Exact Regex)."""
    if not raw_path.startswith("/") or "\\" in raw_path or ".." in raw_path.split("/"):
        raise HTTPException(status_code=403, detail="path_traversal_forbidden")
    clean_path = posixpath.normpath(raw_path)
    if not clean_path.startswith("/"):
        clean_path = "/" + clean_path

    m = method.upper()
    for allowed_method, pattern in OPERATOR_ROUTE_ALLOWLIST:
        if m == allowed_method and pattern.match(clean_path):
            return clean_path
    raise HTTPException(status_code=403, detail=f"operator_route_forbidden:{m}:{clean_path}")
```

---

## 5. Public Kubernetes Ingress & WebSocket Ingest Hardening (`WS /ws/ingest`)

### Audit Checklist
1. **Remove Internal AI / Voice Worker Pods from Public Ingress (`ingress.yaml` / `gateway.yaml`)**:
   - Check if `/voice-worker-1..5` (where `POST /announce` clears the audio queue and speaks arbitrary `banner_text` over the venue speakers!) or `/vision-inference-api` (vLLM GPU/TPU inference) are exposed on the public Ingress. Keep pod-to-pod traffic strictly on internal ClusterIP DNS (`*.svc.cluster.local`).
2. **Authenticate WebSocket Publishers (`WS /ws/ingest`) Before `ws.accept()`**:
   - Verify `Authorization: Bearer <STREAM_INGEST_TOKEN>` using `hmac.compare_digest` **before** calling `await ws.accept()` (closing with `code=1008` on mismatch), and verify `header.device_id == settings.expected_device_id` on incoming camera frame envelopes so external scripts cannot inject fake live video or audio onto the TVs.

---

## 6. Active Verification & Penetration Testing Recipes (`curl`)

Run these non-destructive verification commands against staging or local deployments to prove Phase 2 controls work:

```bash
# 1. Verify Direct Backend Origin Bypass Protection (*.run.app)
curl -i https://core-api-xyz.run.app/api/queue
# Expected: 403 Forbidden {"detail": "direct_backend_access_forbidden"}

# 2. Verify POST /api/register Rejects Cookie-less Bot Loops (Layer-1 Device Lock)
curl -i -X POST https://app.example.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Team"}'
# Expected: 403 Forbidden {"detail": "missing_device_session_reload_page"}

# 3. Verify Operator Proxy Blocks Path Traversal & Destructive Admin Routes
curl -i -X DELETE https://app.example.com/operator/api/admin/teams/123 \
  -H "Cookie: OPERATOR_SESSION_COOKIE=<valid_staff_cookie>"
# Expected: 403 Forbidden {"detail": "operator_route_forbidden:DELETE:/api/admin/teams/123"}

curl -i "https://app.example.com/operator/api/stations/../admin/teams/123/assets" \
  -H "Cookie: OPERATOR_SESSION_COOKIE=<valid_staff_cookie>"
# Expected: 403 Forbidden {"detail": "path_traversal_forbidden"}
```
