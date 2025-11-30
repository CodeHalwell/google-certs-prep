# Learning Path 02 – Vertex AI

_Last Updated: November 30, 2025_

**Difficulty:** Advanced  
**Estimated time:** 10–14 hours

This path covers the core Vertex AI components you'll need for PMLE and production ML.

## Vertex AI Components to Master

### Vertex AI Workbench

**What it is:** Managed Jupyter notebooks (interactive Python/R environment)

**Use cases:**
- Data exploration and visualisation
- Model prototyping
- Running training code interactively

**Managed vs User-Managed:**
- **Managed notebooks:** Google handles infrastructure; you write code
- **User-managed:** Full control over the instance (requires more ops knowledge)

**Best practice:** Start with managed notebooks for prototyping; switch to custom training jobs for production workloads.

**Cost:** Charged by compute instance size (CPU/GPU hours); pause when not in use to avoid surprise bills.

### Vertex AI Training

**What it is:** Managed service for training ML models at scale.

**Workflow:**
1. Package your training code (train.py) into a Docker image
2. Push image to Artifact Registry (Google's container registry)
3. Submit a training job specifying:
   - Image URI
   - Machine type (n1-standard-4, V100 GPU, TPU, etc.)
   - Replica count (for distributed training)
   - Hyperparameters (learning rate, batch size, etc.)
4. Vertex AI provisions instances, runs training, saves model to Cloud Storage

**Job types:**
- **Built-in algorithms:** Pre-built, optimised training (common in AutoML)
- **Custom jobs:** Bring your own Docker image with any framework

**Example:** Submit a TensorFlow training job that runs for 1 hour on 1 GPU, then saves the trained model to GCS.

**Cost:** Charged per machine-hour (e.g., 1 GPU-hour ≈ £0.35–0.60 GBP)

### Vertex AI Model Registry

**What it is:** Versioned storage for trained models with metadata.

**Why it matters:**
- Reproducibility: know exactly which code, data, and hyperparameters produced each model
- Governance: track who deployed which model and when
- Rollback: quickly revert to a previous model version if the new one fails

**Workflow:**
1. After training, upload model to registry with a name and version
2. Add metadata (accuracy, training date, owner, framework)
3. Use registry to deploy or share models

**Best practice:** Always version your models; never overwrite a production model without testing.

### Vertex AI Endpoints (Online Prediction)

**What it is:** Managed REST API for real-time model predictions.

**Workflow:**
1. Create an endpoint (allocates infrastructure)
2. Deploy a model to the endpoint (runs prediction server)
3. Send requests to the endpoint; get predictions back
4. Monitor latency, throughput, and errors

**Scaling:** Automatically scales based on traffic (up to a max you define). Can also do manual scaling.

**Cost:** Charged by compute instance type and time deployed (e.g., online endpoint running 1 month on 1 CPU ≈ £100–200 GBP). Prediction requests typically included; some compute instances charge per request.

**Example:** Deploy a trained model to an endpoint; receive 1,000 predictions/second during peak hours.

### Vertex AI Pipelines

**What it is:** Orchestration tool for automating ML workflows using Kubeflow Pipelines.

**Components of a pipeline:**
- **Data ingestion:** Fetch data from BigQuery, Cloud Storage, APIs
- **Preprocessing:** Clean, transform, feature engineer
- **Training:** Submit training job
- **Evaluation:** Assess model quality
- **Conditional logic:** Deploy if accuracy > threshold
- **Deployment:** Push model to endpoint

**Why it matters:**
- **Reproducibility:** run the same workflow repeatedly; get same results
- **Automation:** trigger on schedule or on data changes
- **Monitoring:** track which data/code/models were used
- **Governance:** audit trail for compliance

**Example pipeline:**
1. Read monthly transactions from BigQuery
2. Preprocess (scale, encode)
3. Train model
4. Evaluate on holdout set
5. If accuracy > 90%, deploy to production; else alert data scientist

**Cost:** Charged for underlying compute (training, evaluation, etc.); pipeline orchestration itself is free.

### Vertex AI Feature Store (Conceptual Overview)

**What it is:** Centralised repository for ML features (input variables).

**Problem it solves:** Data scientists often recompute the same features (e.g., "customer lifetime value") repeatedly, leading to inconsistency and waste.

**Solution:** Define features once in Feature Store; reuse across models, training, and prediction.

**Example:** In the Feature Store, define "customer_lifetime_value" as a feature; Vertex AI computes it during training and automatically fetches it during serving (ensuring consistency).

**For PMLE:** You should understand the concept and use cases; detailed configuration is less critical for the exam.

### Vertex AI Experiments and Metadata

**What it is:** Automated tracking of ML experiments (hyperparameters, metrics, code versions).

**Use case:** You run multiple training jobs with different hyperparameters; Vertex AI logs each run, metrics, and outputs; you can compare and find the best config.

**Best practice:** Always log experiments; helps with reproducibility and governance.

## Putting It All Together: E2E Vertex AI Workflow

1. **Explore (Workbench):** Load data, visualise, prototype model
2. **Train (Training):** Package code, submit scalable training job
3. **Register (Model Registry):** Save trained model with metadata
4. **Evaluate (Pipelines):** Automated evaluation and conditional logic
5. **Deploy (Endpoints):** Serve model for real-time or batch predictions
6. **Monitor (Monitoring):** Track accuracy and performance; alert on issues

## Exam Focus

**PMLE will test:**
- [ ] When to use Workbench vs custom training vs AutoML
- [ ] How to structure training code for Vertex AI
- [ ] Trade-offs between online endpoints and batch prediction
- [ ] Scaling and performance considerations
- [ ] Cost optimisation (choosing cheaper instance types, auto-scaling)
- [ ] Model versioning and governance

## Cross-References

- See `03-tensorflow-keras.md` for writing training code
- See `04-mlops-deployment.md` for pipelines and CI/CD
- See `code-examples/vertex-ai-sdk/` for hands-on code
