# Architecture Patterns – Professional ML Engineer

_Last Updated: November 30, 2025_

## Overview

This guide covers production ML architectures: real-time serving, batch prediction, feature engineering, multi-model routing, and multi-cloud strategies. Each pattern addresses trade-offs between latency, cost, accuracy, and complexity.

---

## Pattern 1: Real-Time Prediction (Low-Latency Online Serving)

### Use Case
Fraud detection, recommendation systems, clinical decision support. Requirement: <200ms latency per prediction.

### Architecture
```
User Request
    ↓
[API Gateway / Load Balancer]
    ↓
[Vertex AI Endpoint] ← Model Container (n1-standard-2, 2–4 replicas)
    ↓
Features from [Feature Store] (in-memory cache if needed)
    ↓
Prediction Response (JSON)
    ↓
Upstream Service
```

### Implementation on GCP
```bash
# 1. Deploy model to Vertex AI Endpoint
gcloud ai endpoints create --display-name "Fraud Detection"
gcloud ai endpoints deploy-model <ENDPOINT_ID> \
  --model=<MODEL_ID> \
  --machine-type n1-standard-2 \
  --min-replica-count 2 \
  --max-replica-count 10

# 2. Configure autoscaling
gcloud ai endpoints update <ENDPOINT_ID> \
  --enable-autoscaling \
  --max-replica-count 10 \
  --target-cpu-utilization 70

# 3. Send prediction
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://us-central1-aiplatform.googleapis.com/v1/projects/<PROJECT_ID>/locations/us-central1/endpoints/<ENDPOINT_ID>:predict \
  -d '{"instances": [{"amount": 500, "merchant_category": "food"}]}'
```

### Cost Breakdown (Monthly, GBP)
| Component | Cost | Notes |
|-----------|------|-------|
| Endpoint (2 n1-standard-2) | £43.80 | £21.90 per machine/month |
| Prediction API calls | £0–5.00 | £0.01 per 100 predictions |
| Feature Store queries | £5–15 | Depends on QPS |
| **Total** | **£50–65** | For 1M predictions/month |

### Pros & Cons
- ✅ Low latency (<200ms)
- ✅ Real-time monitoring/drift detection
- ❌ Expensive (constant compute cost)
- ❌ Complex auto-scaling setup
- ⚠️ Requires caching for high-frequency features

### Trade-offs
- **Accuracy vs Speed:** Full ensemble vs lightweight fast model?
- **Cost vs Latency:** More replicas = lower latency but higher cost
- **On-demand vs Pre-warmed:** Keep replicas running (expensive) vs cold-start (risky)

---

## Pattern 2: Batch Prediction (High-Throughput, Cost-Optimized)

### Use Case
Monthly marketing campaigns, nightly fraud scoring, weekly recommendations. Latency acceptable: hours to days.

### Architecture
```
Data Source (BigQuery, Cloud Storage)
    ↓
[Cloud Dataflow / Batch Job]
    ↓
Load Features [Feature Store]
    ↓
[Vertex AI Batch Prediction Job] (uses preemptible VMs for cost)
    ↓
Write Results to BigQuery / Cloud Storage
    ↓
Downstream (Marketing, fraud team, etc.)
```

### Implementation on GCP
```bash
# 1. Prepare input file (JSONL format, one prediction per line)
gsutil cp input.jsonl gs://your-bucket/batch-input/

# 2. Submit batch prediction job
gcloud ai batch-predict create \
  --display-name "Weekly Marketing Scores" \
  --model <MODEL_ID> \
  --input-paths gs://your-bucket/batch-input/input.jsonl \
  --output-path gs://your-bucket/batch-output/

# 3. Monitor job
gcloud ai batch-predict list

# 4. Retrieve results
gsutil cp -r gs://your-bucket/batch-output/predictions/* .
```

### Cost Breakdown (Monthly, GBP)
| Component | Cost | Notes |
|-----------|------|-------|
| Batch prediction (1M predictions) | £3–5 | Preemptible VMs; cheaper than online |
| Cloud Storage (input + output) | £2–5 | 100GB stored |
| BigQuery (load results) | £2–3 | £6.25 per TB scanned |
| **Total** | **£7–13** | For 1M predictions/month |

### Pros & Cons
- ✅ 60% cheaper than online serving
- ✅ Simple asynchronous workflow
- ❌ High latency (hours to days)
- ❌ Requires retooling for urgent predictions
- ✅ Naturally handles backpressure

### Trade-offs
- **Speed vs Cost:** Batch slower but 5–10× cheaper
- **Reusable Features:** Feature engineering shared with real-time

---

## Pattern 3: Feature Engineering Pipeline & Feature Store

### Use Case
Train models on historical data; serve pre-computed features to online endpoint or batch job. Ensures feature consistency: train = serve.

### Architecture
```
Raw Data (Events, CRM, logs)
    ↓
[Vertex AI Feature Store]
  - Offline store (BigQuery): historical feature snapshots
  - Online store (Cloud Firestore): real-time feature lookup
    ↓
[Training Pipeline]
  - Fetch features from offline store
  - Join with labels
  - Train model
    ↓
[Prediction]
  - Real-time: lookup online store
  - Batch: lookup offline store
```

### Implementation on GCP
```bash
# 1. Create Feature Store
gcloud ai feature-stores create my-feature-store \
  --location us-central1

# 2. Create feature entity type (e.g., "customer")
gcloud ai feature-groups create customers \
  --location us-central1 \
  --feature-store my-feature-store

# 3. Add features (e.g., purchase_count, last_purchase_date)
gcloud ai features create purchase_count \
  --parent projects/<PROJECT>/locations/us-central1/featureStores/my-feature-store/entityTypes/customers \
  --value-type INT64 \
  --description "Total purchases"

# 4. Ingest features (batch)
bq load \
  --source_format=CSV \
  projects/<PROJECT>/datasets/features.customers \
  gs://your-bucket/customer-features.csv

# 5. Serve features in prediction
endpoint.predict(instances=[{
  "customer_id": "cust_123",
  "purchase_count": <fetch from Feature Store>
}])
```

### Cost Breakdown (Monthly, GBP)
| Component | Cost | Notes |
|-----------|------|-------|
| Feature Store (online lookup) | £10–30 | Per 1M lookups |
| BigQuery (offline storage) | £5–10 | £6.25 per TB scanned |
| **Total** | **£15–40** | For active feature set |

### Pros & Cons
- ✅ Consistency between train and serve
- ✅ Single source of truth for features
- ❌ Operational complexity (another database)
- ✅ Enables rapid model experimentation

---

## Pattern 4: Multi-Model Serving (Ensemble, Routing, A/B)

### Scenario 1: Ensemble (Combine predictions)
```
Input
  ↓
[Model A] → Fraud probability: 0.3
[Model B] → Fraud probability: 0.4
[Model C] → Fraud probability: 0.45
  ↓
[Ensemble Logic] (average, weighted, voting)
  ↓
Final prediction: 0.38 (fraud unlikely)
```

### Scenario 2: Routing (Pick best for request)
```
Request (e.g., "premium customer")
  ↓
[Decision Logic]
  - If premium → Model A (high-accuracy, slower)
  - Else → Model B (fast, lower accuracy)
  ↓
Prediction
```

### Scenario 3: Canary (Gradual rollout)
```
Request
  ↓
[Traffic Split]
  - 95% → Model v1 (proven)
  - 5% → Model v2 (new)
  ↓
Monitor metrics:
  - v1: latency 50ms, error rate 0.1%
  - v2: latency 60ms, error rate 0.05% (better!)
  ↓
After 1 day, shift to 50/50
After 1 week, 100% v2
```

### Implementation on GCP
```bash
# Deploy multiple models to same endpoint with traffic split
gcloud ai endpoints deploy-model <ENDPOINT_ID> \
  --model=<MODEL_A_ID> \
  --display-name "Model A (main)"

gcloud ai endpoints deploy-model <ENDPOINT_ID> \
  --model=<MODEL_B_ID> \
  --display-name "Model B (canary)" \
  --traffic-split "0=95,1=5"  # 95% A, 5% B

# Monitor
gcloud ai endpoints describe <ENDPOINT_ID>

# Gradually increase traffic to B
gcloud ai endpoints update-deployed-model <ENDPOINT_ID> \
  --deployed-model-id <MODEL_B_DEPLOYED_ID> \
  --traffic-split "0=50,1=50"
```

### Cost Breakdown (Multi-Model)
| Scenario | Cost (Monthly, GBP) | Notes |
|----------|-------------------|-------|
| Ensemble (3 models, 1 endpoint) | £43.80 | Same endpoint, 3x compute per prediction |
| Routing (2 models, 1 endpoint) | £43.80 | Shared endpoint; intelligent dispatch |
| Canary (2 models, 1 endpoint) | £43.80 | Same cost; gradual rollout safer |

---

## Pattern 5: Hybrid & Multi-Cloud Architecture

### Scenario: Customer wants cloud flexibility + cost optimization
```
GCP (Primary)
├─ Vertex AI Training (experimentation)
├─ BigQuery (data warehouse)
├─ Feature Store (dev/test)

AWS (Secondary)
├─ SageMaker (for team trained on AWS)
├─ S3 (data sharing)

Azure (Compliance)
├─ Azure ML (HIPAA-compliant for healthcare)
├─ Cosmos DB (patient records)

Orchestration
├─ Cross-cloud model registry (W&B, Databricks)
├─ Data sync via ETL (Dataflow → S3/Cosmos)
└─ Prediction routing: GCP primary, AWS/Azure failover
```

### Implementation Strategy
```bash
# 1. Train on GCP (powerful GPUs)
gcloud ai training submit pytorch --config training.yaml

# 2. Export to model registry (accessible to AWS/Azure)
gsutil cp model.tar gs://shared-bucket/models/
aws s3 cp s3://shared-bucket/models/model.tar .

# 3. Deploy on AWS for US West (latency)
sagemaker create-endpoint --model-name loan-classifier

# 4. Deploy on Azure for healthcare (HIPAA)
az ml model create --name loan-classifier-hipaa \
  --path model/ \
  --type custom

# 5. Route traffic
Request → Geo-latency check → Best endpoint (GCP/AWS/Azure)
```

### Cost Breakdown (Multi-Cloud Setup)
| Cloud | Service | Monthly Cost (GBP) | Use Case |
|-------|---------|-------------------|----------|
| GCP | Vertex AI + BigQuery | £200–300 | Training, experimentation |
| AWS | SageMaker + S3 | £100–150 | US West serving, team preference |
| Azure | Azure ML + Cosmos | £150–200 | Healthcare (HIPAA) |
| **Total** | Multi-cloud | **£450–650** | 1M predictions/month across clouds |

### Pros & Cons
- ✅ Flexibility (use best tool per workload)
- ✅ Vendor lock-in mitigation
- ✅ Geo-latency optimization
- ❌ Operational complexity (3 dashboards, 3 teams)
- ❌ Data sync overhead
- ⚠️ Cost visibility harder

---

## Pattern Selection Guide

| Requirement | Best Pattern | Reasoning |
|-------------|--------------|-----------|
| <100ms latency | Real-Time Online | Endpoint always active |
| <£10/month cost | Batch Prediction | Preemptible VMs |
| 1000 QPS, <50ms | Real-Time Online + Caching | Add Redis for hot features |
| Monthly campaign | Batch Prediction | No need for real-time |
| A/B testing new model | Canary Deployment | Safe gradual rollout |
| High accuracy required | Ensemble | Combine multiple models |
| GDPR + HIPAA compliance | Multi-Cloud (Azure primary) | Regulatory-approved infrastructure |
| Experimentation speed | Feature Store + GCP Training | Centralized, fastest iteration |

---

## Cost Optimization Tips

1. **Use preemptible VMs for batch (50% savings)**
   ```bash
   gcloud ai batch-predict ... --machine-type n1-standard-4 --use-preemptible
   ```

2. **Enable autoscaling on endpoints (scale down during off-hours)**
   ```bash
   gcloud ai endpoints update <ID> --min-replica-count 1 --max-replica-count 10
   ```

3. **Cache hot features locally (reduce Feature Store queries)**
   ```python
   # Instead of Feature Store lookup every time
   cache = {"customer_123": {"purchase_count": 50}}  # Redis
   ```

4. **Batch small requests (amortize overhead)**
   ```bash
   # Instead of 1000 predictions = 1000 API calls
   # Send 100 batches of 10 = 100 API calls
   ```

5. **Use shared endpoints for multiple models (vs separate endpoints)**
   ```bash
   # Cost: 1 endpoint (shared) vs 3 endpoints (separate)
   ```

---

## Exam Questions

**Q1:** Which architecture minimizes latency for recommendation system?
- A) Batch prediction  
- B) Real-time online serving
- C) Feature engineering only  
- D) Multi-cloud ensemble

**Answer:** B. Real-time online serving (<200ms with Vertex AI Endpoint).

**Q2:** Customer wants <£10/month for 1M predictions, latency OK (1 hour). Recommend:
- A) Real-time endpoint
- B) Batch prediction with preemptible VMs
- C) Ensemble serving
- D) Feature Store + BigQuery

**Answer:** B. Batch prediction with preemptible VMs costs ~£7–10/month.

**Q3:** How to safely deploy new model without risk?
- A) Immediate 100% traffic switch
- B) A/B testing with traffic split (5% → 50% → 100%)
- C) Train on test data only
- D) Use single endpoint, no monitoring

**Answer:** B. Canary deployment (traffic split) allows safe rollout with monitoring.

---

## References

- [Vertex AI Endpoints Documentation](https://cloud.google.com/vertex-ai/docs/predictions/online-predictions)
- [Batch Prediction Guide](https://cloud.google.com/vertex-ai/docs/predictions/batch-predictions)
- [Feature Store Best Practices](https://cloud.google.com/vertex-ai/docs/featurestore/latest/overview)
- [MLOps Architecture Patterns](https://cloud.google.com/architecture/mlops-with-vertex-ai)

---

**Next:** Review `exam-domains.md` for domain-specific study checklist; then take `practice-exam.md`.