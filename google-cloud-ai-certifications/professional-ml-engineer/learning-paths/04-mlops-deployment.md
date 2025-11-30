# Learning Path 04 – MLOps & Deployment

_Last Updated: November 30, 2025_

**Difficulty:** Advanced  
**Estimated time:** 10–14 hours

MLOps is the discipline of applying DevOps principles to machine learning. This path covers automating model training, deployment, monitoring, and retraining.

## CI/CD for ML

### Traditional CI/CD

**Standard software:** Code changes → run tests → build → deploy.

**ML twist:** Model training is non-deterministic. Same code + same data can produce slightly different models each time (due to random initialisation, GPU variance, etc.).

**Solution:** Version everything:
- Code (Git)
- Data (dataset versions, hash of training set)
- Model (save with metadata: hyperparameters, accuracy, training date)

### Git-Based Workflow

```bash
# Developer commits code changes
git commit -m "Improve feature engineering for customer churn model"
git push origin feature/churn-v2

# GitHub Actions (or Cloud Build) triggers:
# 1. Run linting, unit tests
# 2. Train model on validation dataset
# 3. Compare new model accuracy vs baseline
# 4. If accuracy > threshold, automatically merge and tag release
```

**Benefits:**
- Reproducible: run same code, get same model (given same seed)
- Traceable: know exactly which code/data produced production model
- Safe: test model before deploying

### Cloud Build + Vertex AI Training

Use Google Cloud's managed CI/CD:

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/churn-model', '.']
  
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/churn-model']
  
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - run
      - --filename=training-job.yaml
      - --location=us-central1
```

**Workflow:** Code commit → Cloud Build builds Docker image → pushes to Artifact Registry → submits Vertex AI training job.

## Vertex AI Pipelines

### What It Is

Orchestration tool (built on Kubeflow) for automating multi-step ML workflows.

### Components of a Pipeline

1. **Data Ingestion:** Fetch from BigQuery, Cloud Storage, APIs
2. **Preprocessing:** Clean, transform, engineer features
3. **Training:** Submit Vertex AI training job
4. **Evaluation:** Assess accuracy, fairness, drift
5. **Conditional Logic:** "If accuracy > 90%, proceed; else stop"
6. **Deployment:** Push model to endpoint

### Simple Pipeline Example (Pseudocode)

```python
from kfp import dsl
from kfp.v2 import compiler

@dsl.component
def load_data(project: str) -> dsl.Output[dsl.Model]:
    """Load data from BigQuery"""
    # Load 1M rows, return as a serialized dataset
    pass

@dsl.component
def train_model(dataset: dsl.Input[dsl.Model]) -> dsl.Output[dsl.Model]:
    """Train XGBoost model"""
    # Train, evaluate, save model
    pass

@dsl.component
def evaluate_model(model: dsl.Input[dsl.Model]) -> dict:
    """Evaluate and return metrics"""
    # Return {"accuracy": 0.92}
    pass

@dsl.pipeline(name="churn-prediction-pipeline")
def churn_pipeline(project: str):
    data_task = load_data(project=project)
    train_task = train_model(dataset=data_task.outputs['dataset'])
    eval_task = evaluate_model(model=train_task.outputs['model'])
    
    # Conditional: only deploy if accuracy > 0.90
    with dsl.Condition(eval_task.outputs['accuracy'] > 0.90):
        deploy_task = deploy_model(model=train_task.outputs['model'])

compiler.Compiler().compile(churn_pipeline, 'churn-pipeline.yaml')
```

### Running the Pipeline

```bash
gcloud ai pipelines runs create \
  --region=us-central1 \
  --pipeline-root=gs://my-bucket/pipeline-runs \
  --template-path=churn-pipeline.yaml
```

**Result:** Pipeline runs; each component runs in its own container; data flows between steps; automatically retries on failure.

### Cost Benefit

- **Reproducibility:** Same pipeline + same data = same model
- **Automation:** Run on schedule (daily, weekly) or on data arrival
- **Governance:** Audit trail: who triggered, when, which code version
- **Debugging:** Each step's logs are captured; easy to identify failures

## Model Monitoring and Retraining

### The Problem: Model Drift

Over time, the real world changes:
- **Data drift:** Distribution of input features changes (e.g., customer demographics shift)
- **Concept drift:** Relationship between features and target changes (e.g., churn drivers evolve)
- **Label drift:** Definition of target changes (e.g., churn metric redefined)

**Result:** Model accuracy degrades.

### Monitoring Strategy

```python
# Pseudocode: log predictions and actual outcomes
def make_prediction_with_logging(user_id, features):
    prediction = model.predict(features)
    log_to_bigquery({
        'user_id': user_id,
        'predicted_churn': prediction,
        'timestamp': datetime.now(),
        'features': features
    })
    return prediction

# Later, when ground truth arrives:
# UPDATE BigQuery table SET actual_churn = 1 WHERE user_id = 123
```

### Automated Retraining

Use Vertex AI Pipelines + Cloud Scheduler:

```bash
# Cloud Scheduler triggers pipeline weekly
gcloud scheduler jobs create pubsub weekly-retrain \
  --schedule="0 2 * * MON" \
  --location=us-central1 \
  --topic=ml-pipeline-trigger
```

**Pipeline logic:**
1. Load new data (last 7 days)
2. Compute accuracy on new data
3. If accuracy < threshold (e.g., 85%), automatically retrain
4. A/B test new model vs old
5. If new model wins, deploy

## A/B Testing and Canary Deployments

### A/B Testing

Serve two models to real users; measure which performs better.

```python
# Pseudocode
import random

def get_prediction(user_id, features):
    if random.random() < 0.5:
        model_version = 'production'
        prediction = model_v1.predict(features)
    else:
        model_version = 'candidate'
        prediction = model_v2.predict(features)
    
    log_prediction(user_id, model_version, prediction, actual_outcome_later)
    return prediction
```

**Analysis (after 1 week):**
- Model A: 500k predictions, 45% conversion
- Model B: 500k predictions, 47% conversion
- **Decision:** Model B is better; promote to production

**Trade-off:** Some users get sub-optimal model; acceptable if sample sizes are large and difference is meaningful.

### Canary Deployment

Gradually roll out new model:
- 5% of traffic → new model
- 95% of traffic → old model
- Monitor error rate; if error rate increases, roll back

```yaml
# Vertex AI Endpoint traffic split
apiVersion: aiplatform.cnrm.cloud.google.com/v1beta1
kind: google_vertex_ai_endpoint
metadata:
  name: churn-endpoint
spec:
  deployedModels:
    - model: gs://my-bucket/model-v1
      displayName: production
      traffic_percentage: 95
    - model: gs://my-bucket/model-v2
      displayName: candidate
      traffic_percentage: 5
```

## Model Governance and Versioning

### Model Registry

Store models with metadata:

```python
from google.cloud import aiplatform

model = aiplatform.Model.upload(
    display_name="churn-prediction-v2",
    artifact_uri="gs://my-bucket/model-v2",
    serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/tf2-cpu.2-11:latest",
    labels={
        "owner": "jane@company.com",
        "framework": "tensorflow",
        "training_accuracy": "0.92",
        "training_date": "2025-01-15"
    }
)
```

**Benefits:**
- Traceability: know who trained model, when, with which data
- Rollback: previous versions still available
- Governance: audit logs for compliance

### Model Cards

Document your model for transparency:

```markdown
# Churn Prediction Model Card

## Model Details
- **Framework:** TensorFlow
- **Training Date:** 2025-01-15
- **Training Data:** 1M customer records (Jan 2024–Dec 2024)

## Performance
- **Accuracy:** 92%
- **Precision:** 0.88
- **Recall:** 0.85

## Limitations
- Trained on UK customer data; may not generalise to EU
- Does not account for seasonal effects

## Ethical Considerations
- No protected attributes (race, gender, age) in features
- Fairness audited: no >5% accuracy difference across demographic groups
```

## Containerisation

### Docker for Training

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY train.py .

ENTRYPOINT ["python", "train.py"]
```

**Usage on Vertex AI:**

```bash
docker build -t gcr.io/my-project/churn-trainer .
docker push gcr.io/my-project/churn-trainer
gcloud ai custom-jobs create \
  --display-name="churn-training-run" \
  --worker-pool-spec="image-uri=gcr.io/my-project/churn-trainer,replica-count=1"
```

## Exam Focus

**PMLE will test:**
- [ ] CI/CD best practices for ML
- [ ] Designing Vertex AI Pipelines for automation
- [ ] Model drift detection and retraining strategies
- [ ] A/B testing and canary deployments
- [ ] Model versioning and governance
- [ ] Containerisation and orchestration
- [ ] Cost optimisation for CI/CD workflows

## Cross-References

- See `02-vertex-ai.md` for Vertex AI components
- See `03-tensorflow-keras.md` for training frameworks
- See `code-examples/deployment-scripts/` for real Docker/deployment code
