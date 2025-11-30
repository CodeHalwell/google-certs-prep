# Cloud Run – Associate Cloud Engineer

_Last Updated: November 30, 2025_

## Overview

Cloud Run provides serverless container execution. Deploy container image; scales to zero; pay per request. Fast-growing service (5–10% of ACE exam).

---

## Key Features

| Feature | Benefit |
|---------|---------|
| Serverless | No server management; auto-scaling 0 to thousands |
| Containers | Deploy any language (Dockerfile) |
| Pay-per-request | £0.00001667 per request (free tier: 2M requests/month) |
| Fast cold start | ~100ms (vs App Engine ~1–5s) |
| 15-minute timeout | Ideal for batch jobs, webhooks |

---

## Deployment

### From Container Registry
```bash
# Build & push to Artifact Registry
gcloud builds submit --tag us-docker.pkg.dev/PROJECT-ID/REPO-NAME/IMAGE-NAME:TAG

# Deploy to Cloud Run
gcloud run deploy my-service \
  --image us-docker.pkg.dev/PROJECT-ID/REPO-NAME/IMAGE-NAME:TAG \
  --platform managed \
  --region us-central1 \
  --port 8080

# View deployed service
gcloud run services list

# Get invoke URL
gcloud run services describe my-service --region us-central1 --format='value(status.url)'
```

### Docker Example
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask
CMD exec python app.py

# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Cloud Run!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

---

## Deployment Options

### 1. Fully Managed (Recommended)
- Google manages everything (infrastructure, OS, runtime)
- Cost: £0.00001667/request (free tier: 2M/month)
- Scaling: 0 to 1000 instances

```bash
gcloud run deploy my-service \
  --image gcr.io/PROJECT-ID/my-service \
  --platform managed \
  --region us-central1
```

### 2. Cloud Run for Anthos (on GKE)
- Your managed Kubernetes cluster
- More control; higher operational overhead
- Cost: Compute Engine costs only (no per-request charge)

---

## Environment & Configuration

```bash
# Set environment variables
gcloud run deploy my-service \
  --image gcr.io/PROJECT-ID/my-service \
  --set-env-vars KEY1=value1,KEY2=value2 \
  --region us-central1

# Set memory & CPU
gcloud run deploy my-service \
  --image gcr.io/PROJECT-ID/my-service \
  --memory 512Mi \
  --cpu 1 \
  --region us-central1

# Set max concurrent requests
gcloud run deploy my-service \
  --image gcr.io/PROJECT-ID/my-service \
  --concurrency 100 \
  --region us-central1

# Set timeout (max 15 minutes = 900 seconds)
gcloud run deploy my-service \
  --image gcr.io/PROJECT-ID/my-service \
  --timeout 600 \
  --region us-central1
```

---

## Scaling & Concurrency

- **Concurrency:** Max requests per instance before spinning new instance
  - Default: 80 concurrent requests per instance
  - High concurrency (e.g., 1000): fewer instances, lower cost
  - Low concurrency (e.g., 10): more instances, higher latency isolation
  
- **Cold start:** ~100ms (instance startup time)
- **Min instances:** Keep instances warm (£0.025/hour each)

```bash
# Keep 5 instances warm for low-latency
gcloud run deploy my-service \
  --image gcr.io/PROJECT-ID/my-service \
  --min-instances 5 \
  --region us-central1
```

---

## Common ACE Exam Questions

**Q1:** Batch job (1-hour execution, then done). Deployment choice?
- A) App Engine Standard (60s timeout)
- B) Cloud Run (15-min timeout, pay-per-request)
- C) GKE (complex, overkill)
- D) Compute Engine (always running, expensive)

**Answer:** B. Cloud Run supports 15-min timeout; pay only when running. Batch jobs ideal use case.

**Q2:** Service hits sudden traffic spike (100→10,000 requests/min). Scaling?
- A) App Engine (slower cold start)
- B) Cloud Run (fast cold start ~100ms)
- C) GKE (manual scaling)
- D) All equally fast

**Answer:** B. Cloud Run coldstarts in ~100ms; App Engine ~1–5s; GKE requires pre-provisioned nodes.

**Q3:** Production webhook costs too high (£0.0002/request). Optimisation?
- A) Switch to App Engine (cheaper per-request)
- B) Increase min_instances (always running, baseline cost)
- C) Increase memory (process faster, fewer instances)
- D) Migrate to Compute Engine (simpler cost model)

**Answer:** C (likely) or batch into fewer requests. Min_instances adds baseline cost; App Engine similar pricing; Compute Engine expensive if 24/7.

---

## Cloud Run vs Competitors

| Service | Startup | Timeout | Cost Model | Best For |
|---------|---------|---------|-----------|----------|
| Cloud Run | ~100ms | 15 min | Per-request | Webhooks, batch jobs, spiky traffic |
| App Engine | ~1–5s | 60s | Per-instance/request hybrid | Web apps, always-on |
| GKE | ~5s | Unlimited | Compute-based | Complex apps, custom orchestration |
| Compute Engine | N/A | Unlimited | Hourly VM | Always-on workloads, legacy |

---

## Cost Breakdown (Monthly, GBP)

| Scenario | Requests | Cost | Notes |
|----------|----------|------|-------|
| Dev/test (1M requests) | 1M | Free | Within free tier |
| Production (100M requests) | 100M | £1.67 | £0.00001667 per request |
| + 5 min instances | - | £1.45 | £0.025/hour × 5 × 24 × 30 |
| **Total** | **100M** | **£3.12** | Very cheap for scale |

---

## Best Practices

- Use Cloud Run for burst traffic (spikes, webhooks)
- Container image should listen on $PORT environment variable
- Health checks built-in (liveness probe every 30s)
- Use Artifact Registry (not deprecated Docker Hub)

---

## Links

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Quickstarts](https://cloud.google.com/run/docs/quickstarts)