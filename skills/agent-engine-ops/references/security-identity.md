# Security & Identity Reference

Detailed guide for agent identity, IAM, encryption, and network security on Vertex AI Agent Engine.

## Agent Identity

### Overview

Agent identity gives each deployed agent a unique principal in Google Cloud IAM. This enables:
- Fine-grained access control per agent
- Audit logging tied to specific agents
- Principle of least privilege for agent resource access

### Provisioning Agent Identity

When you deploy an agent to Agent Engine, it runs under a service account. You can configure which service account the agent uses:

```python
import vertexai
from vertexai.agent_engines import AdkApp

client = vertexai.Client(
    project="your-project-id",
    location="us-central1",
)

# Deploy with default service account
agent_engine = client.agent_engines.create(
    agent_engine=adk_app,
    display_name="identity-agent",
    requirements=["google-cloud-aiplatform[adk,agent_engines]"],
)
```

### Service Account Roles

The agent's service account needs appropriate roles based on what resources it accesses:

| Resource | Required Role | Description |
|----------|-------------|-------------|
| Vertex AI | `roles/aiplatform.user` | Query models, use AI services |
| Cloud Storage | `roles/storage.objectViewer` | Read files from GCS |
| BigQuery | `roles/bigquery.dataViewer` | Query BigQuery tables |
| Secret Manager | `roles/secretmanager.secretAccessor` | Read secrets |
| Cloud SQL | `roles/cloudsql.client` | Connect to Cloud SQL |
| Firestore | `roles/datastore.user` | Read/write Firestore |
| Pub/Sub | `roles/pubsub.publisher` | Publish messages |

### Granting Roles

```bash
# Grant a role to the agent's service account
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:AGENT_SA@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer"

# Grant with condition (e.g., specific bucket only)
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:AGENT_SA@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer" \
    --condition="expression=resource.name.startsWith('projects/_/buckets/my-agent-bucket'),title=agent-bucket-only"
```

## IAM Policies

### Allow Policies

Standard IAM allow policies grant access to Agent Engine resources:

```bash
# Grant agent management access
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="user:developer@example.com" \
    --role="roles/aiplatform.admin"

# Grant query-only access
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="user:enduser@example.com" \
    --role="roles/aiplatform.user"
```

### Deny Policies

Deny policies override allow policies for additional security:

```bash
# Create a deny policy to prevent agent deletion by non-admins
gcloud iam policies create deny-agent-delete \
    --attachment-point="cloudresourcemanager.googleapis.com/projects/PROJECT_ID" \
    --kind=denypolicies \
    --policy-file=deny-policy.json
```

**deny-policy.json:**

```json
{
  "displayName": "Deny agent deletion",
  "rules": [
    {
      "denyRule": {
        "deniedPermissions": [
          "aiplatform.googleapis.com/reasoningEngines.delete"
        ],
        "deniedPrincipals": [
          "principalSet://goog/public:all"
        ],
        "exceptionPrincipals": [
          "principal://goog/subject/admin@example.com"
        ]
      }
    }
  ]
}
```

### Principal Access Boundary (PAB)

Limit the resources a principal can access, even if they have broader IAM roles:

```bash
# Create a Principal Access Boundary policy
gcloud iam principal-access-boundary-policies create agent-boundary \
    --organization=ORG_ID \
    --details-enforcement-version=1 \
    --details-rules='[{
      "description": "Agent can only access specific project",
      "resources": ["//cloudresourcemanager.googleapis.com/projects/agent-project"],
      "effect": "ALLOW"
    }]'
```

## OAuth Integration

### Configuring OAuth for External Services

When agents need to access external services on behalf of users:

**Step 1: Configure OAuth consent screen**

```bash
# Set up OAuth consent screen in Google Cloud Console
# APIs & Services > OAuth consent screen
# Configure scopes, authorized domains, test users
```

**Step 2: Store client credentials**

```python
from google.cloud import secretmanager

def store_oauth_credentials(client_id: str, client_secret: str):
    """Store OAuth credentials in Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    project = "your-project-id"

    # Store client ID
    client.add_secret_version(
        request={
            "parent": f"projects/{project}/secrets/oauth-client-id",
            "payload": {"data": client_id.encode("UTF-8")},
        }
    )

    # Store client secret
    client.add_secret_version(
        request={
            "parent": f"projects/{project}/secrets/oauth-client-secret",
            "payload": {"data": client_secret.encode("UTF-8")},
        }
    )
```

**Step 3: Implement token exchange in agent tools**

```python
from google.cloud import secretmanager
import requests

def get_oauth_token(auth_code: str) -> str:
    """Exchange authorization code for access token."""
    sm_client = secretmanager.SecretManagerServiceClient()
    project = "your-project-id"

    client_id = sm_client.access_secret_version(
        name=f"projects/{project}/secrets/oauth-client-id/versions/latest"
    ).payload.data.decode("UTF-8")

    client_secret = sm_client.access_secret_version(
        name=f"projects/{project}/secrets/oauth-client-secret/versions/latest"
    ).payload.data.decode("UTF-8")

    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": auth_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": "https://your-app.com/callback",
        },
    )
    return response.json()["access_token"]
```

## API Key Management

### Storing Keys in Secret Manager

```python
from google.cloud import secretmanager

def create_secret(project_id: str, secret_id: str, secret_value: str):
    """Create a new secret in Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"

    # Create the secret
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )

    # Add the secret version
    client.add_secret_version(
        request={
            "parent": secret.name,
            "payload": {"data": secret_value.encode("UTF-8")},
        }
    )

def get_secret(project_id: str, secret_id: str) -> str:
    """Retrieve a secret from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

### Using Secrets in Agent Tools

```python
from google.adk.tools import ToolContext
from google.cloud import secretmanager

# Cache the secret manager client
_sm_client = None

def _get_sm_client():
    global _sm_client
    if _sm_client is None:
        _sm_client = secretmanager.SecretManagerServiceClient()
    return _sm_client

def _get_api_key(secret_id: str) -> str:
    """Retrieve API key from Secret Manager (cached client)."""
    client = _get_sm_client()
    name = f"projects/your-project/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def call_external_api(query: str, tool_context: ToolContext) -> dict:
    """Call an external API using a securely stored key."""
    api_key = _get_api_key("external-api-key")
    response = requests.get(
        "https://api.example.com/search",
        params={"q": query},
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return response.json()
```

### Secret Rotation

```bash
# Add a new version (rotates the secret)
echo -n "new-api-key-value" | gcloud secrets versions add my-secret --data-file=-

# Disable the old version
gcloud secrets versions disable OLD_VERSION_ID --secret=my-secret

# Destroy the old version (permanent)
gcloud secrets versions destroy OLD_VERSION_ID --secret=my-secret
```

## CMEK Encryption

### Customer-Managed Encryption Keys

CMEK provides control over encryption keys used for Agent Engine data:

**Step 1: Create a Cloud KMS key**

```bash
# Create a key ring
gcloud kms keyrings create agent-keyring \
    --location=us-central1

# Create an encryption key
gcloud kms keys create agent-key \
    --keyring=agent-keyring \
    --location=us-central1 \
    --purpose=encryption \
    --rotation-period=90d
```

**Step 2: Grant access to the key**

```bash
# Grant the Vertex AI service agent access to the key
gcloud kms keys add-iam-policy-binding agent-key \
    --keyring=agent-keyring \
    --location=us-central1 \
    --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-aiplatform.iam.gserviceaccount.com" \
    --role="roles/cloudkms.cryptoKeyEncrypterDecrypter"
```

**Step 3: Deploy with CMEK**

The CMEK configuration is applied at the Vertex AI platform level, covering all Agent Engine resources in the project.

### What CMEK Protects

| Data | Encrypted With |
|------|---------------|
| Agent code and config | CMEK |
| Session data | CMEK |
| Memory Bank data | CMEK |
| Staging bucket objects | CMEK (if bucket configured with CMEK) |
| Logs | Default Google encryption (configure separately) |

## Private Service Connect (PSC)

### Overview

PSC creates private connectivity between your VPC and Agent Engine, keeping traffic off the public internet.

### Setting Up PSC Interface

**Step 1: Create a PSC endpoint**

```bash
# Reserve an internal IP address
gcloud compute addresses create agent-engine-psc \
    --region=us-central1 \
    --subnet=your-subnet \
    --addresses=10.0.1.100

# Create the PSC endpoint
gcloud compute forwarding-rules create agent-engine-psc-endpoint \
    --region=us-central1 \
    --network=your-vpc \
    --address=agent-engine-psc \
    --target-service-attachment=projects/PROJECT_ID/regions/us-central1/serviceAttachments/aiplatform-attachment
```

**Step 2: Configure DNS peering**

```bash
# Create DNS peering zone
gcloud dns managed-zones create agent-engine-dns \
    --dns-name="us-central1-aiplatform.googleapis.com." \
    --visibility=private \
    --networks=your-vpc \
    --description="DNS peering for Agent Engine PSC"

# Add record set pointing to PSC endpoint
gcloud dns record-sets create us-central1-aiplatform.googleapis.com. \
    --zone=agent-engine-dns \
    --type=A \
    --rrdatas=10.0.1.100
```

**Step 3: Verify connectivity**

```bash
# From a VM in your VPC
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "https://us-central1-aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/us-central1/reasoningEngines"
```

### PSC Architecture

```
Your VPC                        Google Cloud
┌──────────────┐               ┌──────────────────┐
│  Application │──PSC Endpoint─│  Agent Engine     │
│  (VM/GKE)    │               │  (Reasoning       │
│              │               │   Engine)         │
└──────────────┘               └──────────────────┘
     Private IP                    No public IP
     (10.0.1.100)                  traffic
```

### PSC Benefits

| Benefit | Description |
|---------|-------------|
| No public internet | Traffic stays within Google's network |
| Reduced attack surface | No public endpoints to protect |
| Lower latency | Direct private connectivity |
| Compliance | Meets data residency and privacy requirements |
| Firewall control | Standard VPC firewall rules apply |

## Security Checklist

| Category | Check | Priority |
|----------|-------|----------|
| Identity | Agent has dedicated service account | High |
| Identity | Service account has minimal required roles | High |
| Secrets | API keys stored in Secret Manager | High |
| Secrets | No secrets in environment variables | High |
| Secrets | Secret rotation configured | Medium |
| Access | IAM deny policies for destructive operations | Medium |
| Access | Principal Access Boundary configured | Medium |
| Encryption | CMEK enabled for sensitive data | Medium |
| Network | PSC configured for private access | Medium |
| Network | VPC firewall rules restrict access | Medium |
| Auth | OAuth configured for user-facing agents | Conditional |
| Audit | Cloud Audit Logs enabled | High |
| Audit | Log exports to SIEM configured | Medium |
