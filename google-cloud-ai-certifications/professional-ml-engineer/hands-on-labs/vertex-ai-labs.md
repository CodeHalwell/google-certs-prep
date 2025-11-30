# Hands-on Labs – Vertex AI

_Last Updated: November 30, 2025_

**Difficulty:** Intermediate–Advanced  
**Estimated time:** 6–10 hours total

These labs reinforce key exam domains: AutoML, custom training, MLOps, model deployment, and production ML. Suggested sequence: 1 → 2 → 3 → (optional) 4 → 5.

---

## Lab 1: Vertex AI AutoML Tabular Classification
**Exam Domain:** Model Selection & Training (15%)  
**Time:** ~2 hours

### Scenario
Build a binary classification model (approve/reject loan applications) using Vertex AI AutoML, without writing code.

### Prerequisites
- [ ] Project with billing enabled
- [ ] Enable APIs: `gcloud services enable aiplatform.googleapis.com storage-api.googleapis.com`
- [ ] IAM: `roles/aiplatform.admin`, `roles/storage.admin`
- [ ] Sample dataset: Create or download Kaggle loan dataset (~30k rows)

### Key Steps
1. **Prepare dataset:**
   - Upload CSV to Cloud Storage (`gs://your-bucket/loan-data.csv`)
   - 80% training, 20% test split recommended
   - Columns: amount, credit_score, age, employment_years, approved (target)

2. **Create dataset in Vertex AI:**
   ```bash
   gcloud ai datasets create \
     --display-name "Loan Approval Dataset" \
     --metadata-schema-uri gs://google-cloud-aiplatform/schema/trainingData/tabular_classification.yaml \
     --import-paths gs://your-bucket/loan-data.csv
   ```

3. **Train AutoML model:**
   - Open Vertex AI > Datasets > select dataset
   - Create model > AutoML > Tabular classification
   - Set budget: 1 node-hour (£0.50–1.00)
   - Wait for training (10–30 min)

4. **Evaluate results:**
   - Check precision/recall/AUC metrics
   - Review feature importance (which columns matter most?)
   - Understand trade-off: precision vs recall for loan decisions

### Validation Checks
- Model trained successfully (status = "Ready")
- AUC > 0.75 (indicates good discrimination)
- Feature importance shows expected patterns (age, credit_score high importance)

### Cleanup
```bash
# Delete dataset (will prompt before deleting model)
gcloud ai datasets delete <DATASET_ID>
# Delete model
gcloud ai models delete <MODEL_ID>
```

**Exam Tips:**
- AutoML is "no code" but still requires data preparation
- Trade-off: ease-of-use vs customisation (vs custom training)
- Common misconception: AutoML always beats custom code (not true for niche domains)

---

## Lab 2: Vertex AI Custom Training with TensorFlow
**Exam Domain:** Custom Model Development (20%)  
**Time:** ~2.5 hours

### Scenario
Train a custom TensorFlow neural network for image classification, using Vertex AI custom training (not AutoML). Deploy to endpoint for real-time predictions.

### Prerequisites
- [ ] Clone/download lab code: `code-examples/vertex-ai-custom-training.py`
- [ ] APIs: `aiplatform.googleapis.com`, `artifactregistry.googleapis.com`, `compute.googleapis.com`
- [ ] IAM: `roles/aiplatform.admin`, `roles/storage.admin`, `roles/artifactregistry.admin`
- [ ] Docker installed locally (or use Cloud Shell)

### Key Steps
1. **Prepare training container:**
   ```bash
   # Build Docker image with training script
   docker build -t gcr.io/YOUR-PROJECT-ID/loan-trainer:latest .
   docker push gcr.io/YOUR-PROJECT-ID/loan-trainer:latest
   ```

2. **Submit custom training job to Vertex AI:**
   ```bash
   gcloud ai custom-jobs create \
     --display-name "TensorFlow Loan Model" \
     --config training_config.yaml
   ```

3. **Monitor training:**
   - Open Vertex AI > Training > select job
   - Metrics update in real time (loss, accuracy, validation loss)
   - Expected duration: 10–20 min on n1-standard-4 machine

4. **Export model:**
   - Model automatically saved to `gs://your-bucket/model/`
   - Format: SavedModel (TensorFlow native)

5. **Deploy to endpoint:**
   ```bash
   gcloud ai endpoints create --display-name "Loan Classifier"
   gcloud ai endpoints deploy-model <ENDPOINT_ID> \
     --model=<MODEL_ID> \
     --machine-type n1-standard-2 \
     --min-replica-count 1
   ```

6. **Test predictions:**
   ```python
   import vertexai
   from google.cloud.aiplatform.gapic.schema import predict_v1
   
   endpoint = vertexai.Endpoint(endpoint_name="<ENDPOINT_RESOURCE_NAME>")
   predictions = endpoint.predict(
       instances=[{"amount": 5000, "credit_score": 720, "age": 35}]
   )
   print(predictions)
   ```

### Validation Checks
- Training job completes with final loss < initial loss (model learning)
- Model exported to Cloud Storage
- Endpoint deployed (status = "Active")
- Prediction returns JSON with approval probability

### Cleanup
```bash
gcloud ai endpoints undeploy-model <ENDPOINT_ID> --model=<MODEL_ID>
gcloud ai endpoints delete <ENDPOINT_ID>
gcloud ai models delete <MODEL_ID>
```

**Exam Tips:**
- Custom training more flexible but slower to develop
- Key concepts: Docker, training loops, hyperparameter tuning, distributed training
- Endpoint cost varies: min-replica-count drives baseline cost (£0.30–1.00/hour)

---

## Lab 3: MLOps – Vertex AI Pipelines
**Exam Domain:** MLOps & Governance (15%)  
**Time:** ~2.5 hours

### Scenario
Build an automated ML pipeline: data ingestion → training → evaluation → conditional deployment (only if metric > threshold).

### Prerequisites
- [ ] Code: `code-examples/vertex-ai-pipeline.py` (Kubeflow pipeline)
- [ ] APIs: `aiplatform.googleapis.com`, `cloudbuild.googleapis.com`
- [ ] IAM: `roles/aiplatform.admin`, `roles/storage.admin`

### Key Steps
1. **Define pipeline in Python:**
   ```python
   from kfp import dsl
   from kfp.v2.dsl import component
   
   @component
   def load_data(output_data: dsl.Output[dsl.Dataset]):
       import pandas as pd
       df = pd.read_csv('gs://bucket/data.csv')
       df.to_csv(output_data.path)
   
   @dsl.pipeline
   def loan_pipeline(project_id: str):
       data = load_data()
       # Next: train, evaluate, conditionally deploy
   ```

2. **Compile pipeline:**
   ```bash
   python pipeline.py  # generates pipeline.json
   ```

3. **Run pipeline on Vertex AI:**
   ```bash
   gcloud ai pipelines run \
     --region us-central1 \
     --template-path pipeline.json \
     --pipeline-name "Loan Approval Pipeline"
   ```

4. **Monitor execution:**
   - Open Vertex AI > Pipelines > select pipeline run
   - View DAG (directed acyclic graph) of tasks
   - Inspect logs for each component
   - Total time: 15–30 min

5. **Trigger re-run:**
   - Change data or hyperparameters
   - Re-run pipeline; compare metrics to previous run
   - Automate with Cloud Scheduler (cron job)

### Validation Checks
- Pipeline DAG displays all 4–5 components
- Each component has green checkmark (success)
- Model metric (e.g., AUC) logged to Vertex AI Experiments
- Can schedule re-runs without manual intervention

### Cleanup
```bash
# Pipeline runs are immutable; view in history
# Delete pipeline definition
gcloud ai pipelines delete <PIPELINE_ID>
```

**Exam Tips:**
- Pipelines = reproducibility + automation
- Key pattern: data → train → evaluate → deploy (conditional)
- Common misconception: Pipeline = always run end-to-end (in fact, conditional steps possible)
- Cost: Pay for compute only; orchestration free

---

## Lab 4: Model Monitoring & Drift Detection
**Exam Domain:** Production ML Systems (10%)  
**Time:** ~1.5 hours (optional advanced lab)

### Scenario
Deploy model to endpoint; generate predictions; detect when input distribution shifts (data drift) and trigger retraining.

### Prerequisites
- [ ] Endpoint from Lab 2 still active
- [ ] APIs: `monitoring.googleapis.com`
- [ ] Sample prediction data (to simulate drift)

### Key Steps
1. **Enable model monitoring:**
   ```bash
   gcloud ai endpoints update <ENDPOINT_ID> \
     --enable-model-monitoring \
     --model-monitoring-alert-threshold 0.15  # 15% drift triggers alert
   ```

2. **Send predictions (simulate production traffic):**
   ```python
   # Simulate 100 predictions with shifted data distribution
   for i in range(100):
       amount = 10000 + random.randint(-2000, 2000)  # Shifted to higher amount
       prediction = endpoint.predict(instances=[{"amount": amount, ...}])
   ```

3. **Monitor drift in Vertex AI:**
   - Open Monitoring dashboard
   - View metrics: input drift % by feature
   - Alert fires if threshold exceeded

4. **Trigger retraining:**
   - When drift detected, run pipeline from Lab 3 automatically (via Cloud Function)
   - Retrain on new data; re-evaluate; conditional deploy

### Validation Checks
- Monitoring enabled on endpoint
- Drift metrics visible in dashboard
- Alert fired when threshold exceeded

**Exam Tips:**
- Data drift = model performance degrades over time
- Solution: monitor + retrain
- Cost: Monitoring adds ~£0.30/month per model

---

## Lab 5: A/B Testing & Canary Deployment
**Exam Domain:** Deployment & Governance (10%)  
**Time:** ~1.5 hours (optional advanced lab)

### Scenario
Deploy new model version (v2) alongside existing (v1); route 20% traffic to v2; compare metrics; gradually increase traffic.

### Prerequisites
- [ ] Two model versions deployed to same endpoint

### Key Steps
1. **Deploy second model version (canary):**
   ```bash
   gcloud ai endpoints deploy-model <ENDPOINT_ID> \
     --model=<MODEL_V2_ID> \
     --traffic-split "0=80,1=20"  # 80% to v1, 20% to v2
   ```

2. **Monitor metrics for both versions:**
   - Latency: v1 vs v2
   - Accuracy: if ground truth available, compare
   - Cost: v2 might use more compute

3. **Shift traffic gradually:**
   ```bash
   # After 1 hour, increase to 50/50
   gcloud ai endpoints update-config <ENDPOINT_ID> \
     --traffic-split "0=50,1=50"
   
   # After 4 hours, go 100% v2 (if metrics good)
   gcloud ai endpoints update-config <ENDPOINT_ID> \
     --traffic-split "0=0,1=100"
   ```

4. **Rollback if issues:**
   ```bash
   # Quick rollback to v1 if v2 has errors
   gcloud ai endpoints update-config <ENDPOINT_ID> \
     --traffic-split "0=100,1=0"
   ```

### Validation Checks
- Traffic split configured correctly
- Metrics dashboard shows both model versions
- Ability to rollback quickly (< 1 min)

**Exam Tips:**
- A/B testing = safer production deployment
- Canary = small % to new version first
- Shadow mode = send copies to new model, don't use for predictions (even safer)

---

## Lab Progression & Exam Alignment

| Lab | Exam Domain | Key Skill | Time |
|-----|-------------|-----------|------|
| 1. AutoML Tabular | Model Selection | No-code training | 2h |
| 2. Custom Training | Custom Models | Docker + TensorFlow | 2.5h |
| 3. Pipelines | MLOps | Automation + CI/CD | 2.5h |
| 4. Monitoring (opt) | Production ML | Drift detection | 1.5h |
| 5. A/B Testing (opt) | Safe Deployment | Canary + rollback | 1.5h |

**Total time:** 5 hours (core), 10 hours (with optional)

---

## Lab Resources

- **Official:** [Google Cloud Skills Boost Labs](https://www.cloudskillsboost.google/catalog)
- **Code examples:** `../code-examples/` (all labs use scripts here)
- **Troubleshooting:**
  - Enable APIs before running labs
  - Check IAM roles (use `gcloud auth list` to verify)
  - Budget alert? Check endpoint hourly cost and delete if not needed

## Post-Lab Actions

- [ ] Complete all 5 labs (or core 3)
- [ ] Document findings: Which was hardest? Which concept needs review?
- [ ] Refactor: Can you automate lab setup with a script?
- [ ] Share: Run lab with colleague; explain key steps
- [ ] Build: Apply pattern to your own project (customer data, internal ML task)

---

**Next:** Review `architecture-patterns.md` for production system design; then attempt `practice-exam.md`.