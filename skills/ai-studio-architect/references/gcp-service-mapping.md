# GCP Service Mapping Reference

Detailed configuration reference for each GCP service used when migrating AI Studio projects to production.

## Service Configurations

### Vertex AI (Gemini)

**API**: `aiplatform.googleapis.com`

**IAM Roles**:
| Role | Scope | Description |
|------|-------|-------------|
| `roles/aiplatform.user` | Service Account | Invoke models, run predictions |
| `roles/aiplatform.admin` | Admin users only | Manage models, endpoints, datasets |

**SDK Migration**:
```
Client-side (AI Studio):  @google/generative-ai
Server-side (Production): @google-cloud/vertexai
```

**Code Change Pattern**:
```typescript
// BEFORE: AI Studio (client-side, API key)
import { GoogleGenerativeAI } from '@google/generative-ai';
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });

// AFTER: Production (server-side, Service Account)
import { VertexAI } from '@google-cloud/vertexai';
const vertexAI = new VertexAI({ project: 'PROJECT_ID', location: 'us-central1' });
const model = vertexAI.getGenerativeModel({ model: 'gemini-2.0-flash' });
```

**gcloud Commands**:
```bash
# Enable API
gcloud services enable aiplatform.googleapis.com

# Grant role to service account
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/aiplatform.user"

# Test model access
gcloud ai models list --region=us-central1
```

---

### Cloud Run

**API**: `run.googleapis.com`

**IAM Roles**:
| Role | Scope | Description |
|------|-------|-------------|
| `roles/run.invoker` | Public or service-to-service | Invoke the service |
| `roles/run.developer` | CI/CD pipeline | Deploy new revisions |
| `roles/run.admin` | Admin users only | Full management |

**Deployment Options**:

| Option | Command | Use Case |
|--------|---------|----------|
| Source deploy | `gcloud run deploy --source=.` | Quick deploy from source (builds container automatically) |
| Container deploy | `gcloud run deploy --image=IMAGE` | Deploy pre-built container |
| YAML deploy | `gcloud run services replace service.yaml` | Declarative configuration |

**Recommended Dockerfile (Multi-stage)**:
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

EXPOSE 8080
ENV PORT=8080
CMD ["node", "dist/server.js"]
```

**gcloud Commands**:
```bash
# Enable API
gcloud services enable run.googleapis.com

# Deploy from source
gcloud run deploy $SERVICE_NAME \
  --source=. \
  --region=$REGION \
  --service-account=$SA_EMAIL \
  --allow-unauthenticated \
  --set-env-vars="PROJECT_ID=$PROJECT_ID"

# Deploy with container
gcloud run deploy $SERVICE_NAME \
  --image=gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --region=$REGION \
  --service-account=$SA_EMAIL

# Get service URL
gcloud run services describe $SERVICE_NAME \
  --region=$REGION \
  --format="value(status.url)"
```

---

### Cloud Firestore

**API**: `firestore.googleapis.com`

**IAM Roles**:
| Role | Scope | Description |
|------|-------|-------------|
| `roles/datastore.user` | Service Account | Read/write documents |
| `roles/datastore.viewer` | Read-only access | Read documents only |
| `roles/datastore.owner` | Admin | Full access including indexes |

**Database Modes**:
| Mode | Use Case |
|------|----------|
| Native | Mobile/web apps, real-time sync, offline support |
| Datastore | Server-side batch operations, legacy Datastore apps |

**gcloud Commands**:
```bash
# Enable API
gcloud services enable firestore.googleapis.com

# Create database (Native mode)
gcloud firestore databases create \
  --location=$REGION \
  --type=firestore-native

# Create composite index
gcloud firestore indexes composite create \
  --collection-group=users \
  --field-config=field-path=name,order=ascending \
  --field-config=field-path=created,order=descending

# Export data (backup)
gcloud firestore export gs://$BUCKET/backups/$(date +%Y%m%d)
```

---

### Cloud Storage

**API**: `storage.googleapis.com`

**IAM Roles**:
| Role | Scope | Description |
|------|-------|-------------|
| `roles/storage.objectViewer` | Read-only | View and download objects |
| `roles/storage.objectAdmin` | Read/write | Full object CRUD |
| `roles/storage.admin` | Admin | Manage buckets and objects |

**Bucket Types**:
| Type | Use Case | Storage Class |
|------|----------|---------------|
| Assets bucket | User uploads, images | Standard |
| Static hosting | SPA frontend files | Standard |
| Backup bucket | Database exports | Nearline/Coldline |

**CORS Configuration** (`cors.json`):
```json
[
  {
    "origin": ["https://your-domain.com"],
    "method": ["GET", "PUT", "POST", "DELETE", "OPTIONS"],
    "responseHeader": ["Content-Type", "Authorization", "X-Requested-With"],
    "maxAgeSeconds": 3600
  }
]
```

**gcloud Commands**:
```bash
# Enable API
gcloud services enable storage.googleapis.com

# Create bucket
gcloud storage buckets create gs://$BUCKET_NAME \
  --location=$REGION \
  --uniform-bucket-level-access

# Apply CORS
gcloud storage buckets update gs://$BUCKET_NAME \
  --cors-file=cors.json

# Make bucket public (for static hosting)
gcloud storage buckets add-iam-policy-binding gs://$BUCKET_NAME \
  --member="allUsers" \
  --role="roles/storage.objectViewer"

# Upload files
gcloud storage cp -r ./dist/* gs://$BUCKET_NAME/
```

---

### Secret Manager

**API**: `secretmanager.googleapis.com`

**IAM Roles**:
| Role | Scope | Description |
|------|-------|-------------|
| `roles/secretmanager.secretAccessor` | Service Account | Read secret values |
| `roles/secretmanager.admin` | Admin | Create and manage secrets |

**Common Secrets for AI Studio Apps**:
| Secret Name | Source | Description |
|-------------|--------|-------------|
| `gemini-api-key` | AI Studio | API key (if not using SA auth) |
| `database-url` | Firestore | Connection string (if needed) |

**gcloud Commands**:
```bash
# Enable API
gcloud services enable secretmanager.googleapis.com

# Create a secret
echo -n "your-api-key" | gcloud secrets create gemini-api-key \
  --data-file=- \
  --replication-policy="automatic"

# Grant access to service account
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/secretmanager.secretAccessor"

# Access secret value (for verification)
gcloud secrets versions access latest --secret=gemini-api-key

# Update secret value
echo -n "new-value" | gcloud secrets versions add gemini-api-key --data-file=-
```

---

### Cloud Build (CI/CD)

**API**: `cloudbuild.googleapis.com`

**IAM Roles**:
| Role | Scope | Description |
|------|-------|-------------|
| `roles/cloudbuild.builds.builder` | Cloud Build SA | Run builds |
| `roles/run.developer` | Cloud Build SA | Deploy to Cloud Run |

**cloudbuild.yaml Template**:
```yaml
steps:
  # Install dependencies
  - name: 'node:20'
    entrypoint: 'npm'
    args: ['ci']

  # Run tests
  - name: 'node:20'
    entrypoint: 'npm'
    args: ['test']

  # Build the application
  - name: 'node:20'
    entrypoint: 'npm'
    args: ['run', 'build']

  # Build container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/$_SERVICE_NAME', '.']

  # Push container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/$_SERVICE_NAME']

  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - '$_SERVICE_NAME'
      - '--image=gcr.io/$PROJECT_ID/$_SERVICE_NAME'
      - '--region=$_REGION'
      - '--service-account=$_SA_EMAIL'
      - '--allow-unauthenticated'

substitutions:
  _SERVICE_NAME: my-app
  _REGION: us-central1
  _SA_EMAIL: my-app-sa@PROJECT_ID.iam.gserviceaccount.com

options:
  logging: CLOUD_LOGGING_ONLY
```

**gcloud Commands**:
```bash
# Enable API
gcloud services enable cloudbuild.googleapis.com

# Connect GitHub repo
gcloud builds repositories create my-repo \
  --remote-uri=https://github.com/user/repo.git \
  --connection=my-connection \
  --region=$REGION

# Create trigger
gcloud builds triggers create github \
  --name="deploy-on-push" \
  --repo-name=my-repo \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml

# Manual build
gcloud builds submit --config=cloudbuild.yaml
```

---

### Identity-Aware Proxy (IAP)

**API**: `iap.googleapis.com`

**IAM Roles**:
| Role | Scope | Description |
|------|-------|-------------|
| `roles/iap.httpsResourceAccessor` | Users/groups | Access IAP-protected resources |
| `roles/iap.admin` | Admin | Configure IAP settings and policies |
| `roles/iap.settingsAdmin` | Admin | Manage IAP settings |

**gcloud Commands**:
```bash
# Enable API
gcloud services enable iap.googleapis.com

# Enable IAP on a Cloud Run service (requires a load balancer)
gcloud iap web enable --resource-type=cloud-run \
  --service=$SERVICE_NAME \
  --region=$REGION

# Grant access to a user
gcloud iap web add-iam-policy-binding \
  --member="user:user@example.com" \
  --role="roles/iap.httpsResourceAccessor" \
  --resource-type=cloud-run \
  --service=$SERVICE_NAME \
  --region=$REGION

# Grant access to a group
gcloud iap web add-iam-policy-binding \
  --member="group:team@example.com" \
  --role="roles/iap.httpsResourceAccessor" \
  --resource-type=cloud-run \
  --service=$SERVICE_NAME \
  --region=$REGION
```

---

### Cloud Monitoring and Logging

**APIs**: `logging.googleapis.com`, `monitoring.googleapis.com`

**IAM Roles**:
| Role | Scope | Description |
|------|-------|-------------|
| `roles/logging.logWriter` | Service Account | Write logs |
| `roles/monitoring.metricWriter` | Service Account | Write custom metrics |
| `roles/monitoring.viewer` | Dashboard users | View metrics and dashboards |

**gcloud Commands**:
```bash
# Enable APIs
gcloud services enable logging.googleapis.com monitoring.googleapis.com

# Create uptime check for Cloud Run service
gcloud monitoring uptime create \
  --display-name="$SERVICE_NAME health" \
  --uri="$SERVICE_URL/health" \
  --check-interval=300

# View recent logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME" \
  --limit=50 \
  --format="table(timestamp, severity, textPayload)"
```

## API Enable Cheat Sheet

Quick copy-paste for enabling all APIs at once:

```bash
# Starter tier
gcloud services enable \
  run.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com

# Standard tier
gcloud services enable \
  run.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com \
  storage.googleapis.com \
  firestore.googleapis.com

# Production tier
gcloud services enable \
  run.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com \
  storage.googleapis.com \
  firestore.googleapis.com \
  cloudbuild.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com

# Enterprise tier (add to Production)
gcloud services enable \
  compute.googleapis.com \
  servicenetworking.googleapis.com \
  cloudkms.googleapis.com \
  accesscontextmanager.googleapis.com
```
