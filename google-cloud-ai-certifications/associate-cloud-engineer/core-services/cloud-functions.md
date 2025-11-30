# Cloud Functions – Associate Cloud Engineer

_Last Updated: November 30, 2025_

## Overview

Google Cloud Functions provides serverless function execution (FaaS). Single function deployed; scales to thousands. 5–8% of ACE exam.

---

## Key Features

| Feature | Benefit |
|---------|---------|
| Serverless | No infrastructure; pay per invocation |
| Triggering | HTTP, Cloud Pub/Sub, Cloud Storage, Firestore, Stackdriver Logging, Cloud Tasks |
| Pricing | £0.40 per million invocations (generous free tier: 2M/month) |
| Languages | Python, Node.js, Go, Java, .NET, Ruby, PHP |
| Timeout | 60–540 seconds (9 minutes) |

---

## Gen 1 vs Gen 2

| Aspect | Gen 1 | Gen 2 |
|--------|-------|-------|
| Timeout | 60s | 540s (9 min) |
| Concurrency | Single request | Multiple concurrent |
| Cold start | ~1–2s | ~1s (faster) |
| Performance | Moderate | Better |
| Recommendation | Legacy | **Use for new functions** |

---

## HTTP Trigger (Most Common)

### Python Example
```python
# main.py
def hello_world(request):
    """HTTP Cloud Function"""
    return 'Hello, World!'

# Deploy
gcloud functions deploy hello_world \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1

# Invoke
curl https://REGION-PROJECT-ID.cloudfunctions.net/hello_world
```

### With Request Handling
```python
def process_request(request):
    """Process JSON request"""
    request_json = request.get_json(silent=True)
    name = request_json.get('name', 'World')
    return f'Hello, {name}!'

# Deploy (Gen 2)
gcloud functions deploy process_request \
  --runtime python39 \
  --trigger-http \
  --gen2 \
  --region us-central1
```

---

## Pub/Sub Trigger (Event-Driven)

Respond to Cloud Pub/Sub messages.

```python
# main.py
def process_message(event, context):
    """Triggered by Pub/Sub message"""
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(f'Processing: {pubsub_message}')

# Deploy
gcloud functions deploy process_message \
  --runtime python39 \
  --trigger-topic my-topic \
  --region us-central1

# Publish message
gcloud pubsub topics publish my-topic --message "Hello"
```

---

## Cloud Storage Trigger

Respond to file uploads/deletions.

```python
# main.py
def process_file(data, context):
    """Triggered by Cloud Storage event"""
    file_name = data['name']
    print(f'Processing file: {file_name}')

# Deploy
gcloud functions deploy process_file \
  --runtime python39 \
  --trigger-resource my-bucket \
  --trigger-event google.storage.object.finalize \
  --region us-central1

# Upload file (triggers function)
gsutil cp local-file.txt gs://my-bucket/
```

---

## Configuration

```bash
# Environment variables
gcloud functions deploy my-function \
  --set-env-vars KEY1=value1,KEY2=value2 \
  --runtime python39 \
  --trigger-http

# Memory (default 256MB)
gcloud functions deploy my-function \
  --memory 512MB \
  --runtime python39 \
  --trigger-http

# Timeout (default 60s)
gcloud functions deploy my-function \
  --timeout 300 \  # 5 minutes
  --runtime python39 \
  --trigger-http

# Service account (for IAM permissions)
gcloud functions deploy my-function \
  --service-account my-service-account@PROJECT.iam.gserviceaccount.com \
  --runtime python39 \
  --trigger-http
```

---

## Common ACE Exam Questions

**Q1:** New file uploaded to Cloud Storage. Need to process (resize, extract metadata). Best function trigger?
- A) HTTP (manual polling)
- B) Cloud Storage event trigger (automatic)
- C) Pub/Sub (overkill)
- D) Cloud Scheduler (cron)

**Answer:** B. Cloud Storage trigger fires automatically on file upload; no polling needed.

**Q2:** Function calls BigQuery to query data. Function fails with permission error. Fix?
- A) Grant BigQuery.DataViewer role to Cloud Functions service account
- B) Use default service account (universal permissions)
- C) Create API key
- D) Switch to Compute Engine

**Answer:** A. Cloud Functions runs under service account; grant specific IAM roles (BigQuery.DataViewer, Viewer, etc.).

**Q3:** HTTP function timeout is 1 hour, but Cloud Functions only supports 9 min (Gen 2). Workaround?
- A) Use Cloud Run (no timeout limit)
- B) Split into multiple functions (chained)
- C) Migrate to Compute Engine
- D) Increase timeout setting

**Answer:** A. Cloud Run ideal for long-running tasks (up to 15 min timeout, or indefinite with proper design). Cloud Functions max 540s.

---

## Cloud Functions vs Competitors

| Service | Timeout | Ideal For | Cost |
|---------|---------|-----------|------|
| Cloud Functions | 9 min | Simple event handlers | £0.40/M invocations |
| Cloud Run | 15 min | Containers, batch jobs | £0.00001667/request |
| App Engine | 60s | Web apps | £0.05/hour |
| Cloud Scheduler | N/A (trigger) | Cron jobs | £0.10 per job |

---

## Cost Breakdown (Monthly, GBP)

| Use Case | Invocations | Cost | Notes |
|----------|-------------|------|-------|
| Dev/test | 2M (free tier) | Free | Free tier generous |
| Production | 10M | £4 | £0.40 per M |
| + 512MB memory | 10M | +£1 | Memory adds cost |
| **Total** | **10M** | **£5** | Still very affordable |

---

## Best Practices

- Keep functions small & focused (single responsibility)
- Use environment variables for config (not hardcoded)
- Set appropriate memory (more = faster CPU, but costs more)
- Use Gen 2 for new functions (better performance)
- Handle errors gracefully (retry logic for event-triggered)

---

## Links

- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Function Triggers](https://cloud.google.com/functions/docs/calling/cloud-tasks)
- [Pricing](https://cloud.google.com/functions/pricing)