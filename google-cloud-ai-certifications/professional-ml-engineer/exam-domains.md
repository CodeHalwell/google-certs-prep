# Exam Domains Checklist – Professional ML Engineer

_Last Updated: November 30, 2025_

Use this as a progress tracker across 6 domains. Each domain appears on 15–30% of questions.

---

## Domain 1: Frame ML Problems (10–15%)
**Weight:** ~6–8 questions out of 50

### Key Concepts
- Identify when ML is the right solution vs traditional software
- Define success metrics (accuracy, precision, recall, AUC, RMSE)
- Recognise supervised vs unsupervised vs reinforcement learning
- Understand business objectives vs model objectives
- Trade-offs: interpretability vs accuracy, latency vs accuracy

### Study Checklist
- [ ] Supervised learning problems: regression (house price), classification (spam)
- [ ] Unsupervised: clustering (customer segmentation), dimensionality reduction
- [ ] Reinforcement learning: gaming, robotics (rarely in PMLE)
- [ ] Success metrics: When to use precision vs recall vs AUC vs RMSE
- [ ] Label definition: What is "fraud"? "Churned customer"? Ambiguity risks
- [ ] Ground truth challenges: Labeling errors, missing labels
- [ ] Business translation: "Improve conversion by 5%" → "Build recommendation model"

### Example Questions
**Q1:** Retail company wants to predict customer churn. Which is the right framing?
- A) Regression problem (predict churn probability 0–1)  ✅
- B) Classification problem (churn yes/no)  ✅
- C) Clustering problem (group customers)
- D) Time series forecasting

**Answer:** A or B (both valid; depends on downstream use - if probability needed, A; if binary decision, B).

**Q2:** How do you define "successful loan"?
- A) Customer doesn't default  ✅
- B) Customer never misses payment
- C) Loan term completes without default
- D) All of above (context dependent)

**Answer:** Depends on business goal. Default-free = A. Never-missed = B (stricter). All OK if specified upfront.

### Recommended Resources
- [Google Cloud Intro to ML](https://google-cloud.skills/intro-ml-en)
- `README.md` (problem framing section)
- `learning-paths/01-ml-on-gcp.md` (problem types overview)

---

## Domain 2: Architect ML Solutions (20–25%)
**Weight:** ~10–13 questions

### Key Concepts
- End-to-end ML system design
- Choose appropriate Google Cloud services (Vertex AI, BigQuery, Dataflow)
- Batch vs online serving trade-offs
- Feature engineering strategy
- Model deployment and monitoring

### Study Checklist
- [ ] When to use AutoML vs custom training
- [ ] Real-time serving: Vertex AI Endpoints, latency/cost trade-offs
- [ ] Batch prediction: Dataflow, BigQuery ML, preemptible VMs
- [ ] Feature Store architecture (offline + online)
- [ ] Data pipeline orchestration (Vertex AI Pipelines, Cloud Composer)
- [ ] Model versioning and registry
- [ ] A/B testing and canary deployment patterns
- [ ] Cost estimation per architecture choice

### Example Questions
**Q1:** Need to score 10M customers monthly for marketing campaign. Latency not critical (24-hour window). Best approach?
- A) Vertex AI Endpoint (online serving)
- B) Batch prediction with preemptible VMs
- C) BigQuery ML
- D) Dataflow custom model

**Answer:** B. Batch prediction 60% cheaper than online serving; preemptible VMs add 50% savings.

**Q2:** Clinical decision support system needs <200ms latency, HIPAA compliance. Architecture choice?
- A) Vertex AI Endpoint (GCP)
- B) Azure ML (NHS-approved)
- C) AWS SageMaker
- D) Local on-premise server

**Answer:** B. Azure has NHS-approved compliance; GCP possible but requires extra work. Depends on existing cloud.

### Recommended Resources
- `architecture-patterns.md` (5 key patterns)
- `learning-paths/04-mlops-deployment.md` (deployment patterns)
- `hands-on-labs/vertex-ai-labs.md` (Lab 2: custom training; Lab 3: pipelines)

---

## Domain 3: Design Data Preparation & Processing (20–25%)
**Weight:** ~10–13 questions

### Key Concepts
- Data ingestion (Cloud Storage, BigQuery, Pub/Sub)
- Data validation and quality checks
- Feature engineering (creating/transforming columns)
- Data pipeline orchestration
- Handling missing values, outliers, imbalanced data

### Study Checklist
- [ ] Data quality checks: schema validation, schema drift, data freshness
- [ ] Missing value strategies: imputation (mean, median, forward-fill), deletion
- [ ] Outlier handling: Z-score, IQR, domain knowledge
- [ ] Feature scaling: normalization, standardization
- [ ] Categorical features: one-hot encoding, embedding
- [ ] Feature interactions: crossing, polynomials
- [ ] Class imbalance: SMOTE, weighted loss, stratified sampling
- [ ] Pipeline automation: Dataflow, Vertex AI Pipelines, Cloud Composer

### Example Questions
**Q1:** Dataset has 5% missing values in "income" column. Approach?
- A) Delete all rows with missing income
- B) Fill with mean income (for numerical)
- C) Fill with median income
- D) Drop column entirely

**Answer:** B or C (both valid). Mean if normal distribution; median if skewed. Depends on data.

**Q2:** Customer churn dataset: 2% positive (churn), 98% negative (no churn). How to handle imbalance?
- A) Use weighted loss function (weight positive class higher)
- B) Oversample minority class (SMOTE)
- C) Undersampling majority class
- D) All of above (context dependent)

**Answer:** A (simplest); B or C if A doesn't work. Avoid deleting data.

### Recommended Resources
- `learning-paths/03-tensorflow-keras.md` (data preprocessing section)
- `learning-paths/05-model-optimization.md` (feature selection)
- `learning-paths/02-vertex-ai.md` (Vertex AI Training data prep)

---

## Domain 4: Develop ML Models (25–30%)
**Weight:** ~12–15 questions

### Key Concepts
- Model training techniques (supervised, unsupervised)
- Hyperparameter tuning (grid search, random search, Bayesian)
- Model selection and evaluation
- Regularization (dropout, L1/L2, early stopping)
- Transfer learning and fine-tuning
- Distributed training

### Study Checklist
- [ ] Supervised learning algorithms: linear regression, logistic regression, tree models, neural networks
- [ ] Unsupervised: K-means, PCA, autoencoders
- [ ] Hyperparameter tuning: grid vs random vs Bayesian (Vertex AI Vizier)
- [ ] Cross-validation strategies: k-fold, stratified
- [ ] Regularization: L1/L2, dropout, early stopping, batch norm
- [ ] Transfer learning: pre-trained models, fine-tuning
- [ ] Distributed training: MirroredStrategy, TPU, data parallelism
- [ ] Model ensembles: voting, averaging, stacking

### Example Questions
**Q1:** TensorFlow model overfitting (training loss 0.1, validation loss 0.5). Solutions?
- A) Add dropout layers
- B) L2 regularization
- C) Early stopping (stop when validation loss increases)
- D) All of above

**Answer:** D. All are valid. Try all three; stop when validation loss plateaus.

**Q2:** Which hyperparameter tuning fastest for 50 hyperparameters?
- A) Grid search (all combinations)
- B) Random search (random sample)
- C) Bayesian (intelligent sampling, Vizier)
- D) Manual

**Answer:** C. Bayesian most efficient (50 params = 10^50 grid combinations; Bayesian explores smart subspace).

### Recommended Resources
- `learning-paths/02-vertex-ai.md` (AutoML training)
- `learning-paths/03-tensorflow-keras.md` (custom models, distributed training)
- `learning-paths/05-model-optimization.md` (hyperparameter tuning, regularization)

---

## Domain 5: Automate & Orchestrate ML Pipelines (15–20%)
**Weight:** ~8–10 questions

### Key Concepts
- Pipeline definition (DAGs, components)
- Orchestration tools (Vertex AI Pipelines, Cloud Composer)
- Continuous training (retraining on new data)
- Model monitoring and drift detection
- Experiment tracking and versioning

### Study Checklist
- [ ] Kubeflow Pipelines (DSL, components, DAG definition)
- [ ] Vertex AI Pipelines (managed orchestration)
- [ ] Cloud Composer (Apache Airflow on GCP)
- [ ] Pipeline scheduling: Cloud Scheduler, cron jobs
- [ ] Model versioning: registry, rollback, promotion
- [ ] Experiment tracking: metrics logging, hyperparameter comparison
- [ ] Automated retraining: triggers (schedule, drift, new data)
- [ ] Pipeline failure handling: retries, notifications

### Example Questions
**Q1:** Model performance degrades after deployment. Need automated retraining weekly. Approach?
- A) Manual trigger
- B) Cloud Scheduler + Vertex AI Pipeline
- C) Apache Airflow + manual approval
- D) Data Fusion + scheduled jobs

**Answer:** B. Simplest: Cloud Scheduler triggers pipeline on schedule; Vertex AI orchestrates training + evaluation + conditional deploy.

**Q2:** How to structure Vertex AI Pipeline for conditional deployment (train → evaluate → deploy only if AUC > 0.85)?
- A) Single linear pipeline
- B) Branching pipeline with conditional exit
- C) Two separate pipelines (one trains, one deploys manually)
- D) Dashboard-driven (person checks metrics, manually triggers deploy)

**Answer:** B. Use dsl.Condition to branch: if AUC > 0.85, deploy; else, skip.

### Recommended Resources
- `hands-on-labs/vertex-ai-labs.md` (Lab 3: Pipelines)
- `learning-paths/04-mlops-deployment.md` (MLOps patterns, pipeline orchestration)
- [Vertex AI Pipelines Documentation](https://cloud.google.com/vertex-ai/docs/pipelines)

---

## Domain 6: Monitor, Optimise & Maintain ML Solutions (10–15%)
**Weight:** ~5–8 questions

### Key Concepts
- Model monitoring (predictions, latency, data drift)
- Performance metrics tracking
- Model retraining triggers
- Cost optimisation
- Incident response and debugging

### Study Checklist
- [ ] Model monitoring: online metrics (latency, error rate), batch metrics (accuracy)
- [ ] Data drift detection: statistical tests, alert thresholds
- [ ] Prediction drift: model output distribution shift
- [ ] Feature monitoring: schema changes, data quality issues
- [ ] Cost tracking: per-model cost attribution, optimisation
- [ ] Debugging: feature importance analysis, error analysis
- [ ] Incident response: rollback procedures, root cause analysis
- [ ] SLA management: availability, latency SLAs

### Example Questions
**Q1:** Fraud detection model accuracy drops 5% week-over-week. Diagnose:
- A) Data drift (input distribution changed)
- B) Label drift (fraud definition changed)
- C) Concept drift (fraud patterns evolved)
- D) Any of above (need investigation)

**Answer:** D. Common causes: fraudsters adapt (concept), new products (data), or labeling error (label). Investigate each.

**Q2:** Endpoint costs £50/month but used only 20% of the time. Optimisation?
- A) Increase min-replica-count to 10
- B) Reduce min-replica-count to 1, enable autoscaling
- C) Switch to batch prediction (if latency OK)
- D) B or C (depends on latency requirements)

**Answer:** D. If latency <1 hour acceptable, use batch (70% cheaper). If real-time required, B (autoscaling reduces cost by 60%).

### Recommended Resources
- `learning-paths/04-mlops-deployment.md` (monitoring, incident response)
- `learning-paths/06-responsible-ml.md` (model governance, incident response)
- `hands-on-labs/vertex-ai-labs.md` (Lab 4: monitoring & drift)

---

## Exam Preparation by Domain

| Domain | Weight | Priority | Hours | Resources |
|--------|--------|----------|-------|-----------|
| Problem Framing | 10–15% | High | 4–5 | README, learning-path-01 |
| Architecture | 20–25% | Critical | 8–10 | architecture-patterns, hands-on-labs (2–3) |
| Data Prep | 20–25% | Critical | 8–10 | learning-path-03, practice-flows |
| Model Dev | 25–30% | Critical | 10–12 | learning-path-03/05, hands-on-labs (1–2) |
| Orchestration | 15–20% | High | 6–8 | hands-on-labs-03, architecture-patterns |
| Monitor/Maintain | 10–15% | Medium | 4–6 | learning-path-04, hands-on-labs (4–5) |

**Total:** 40–60 hours study + 10–15 hours hands-on labs

---

## Exam Strategy by Domain

### Domain 1 (Problem Framing): 1–2 questions expected
- Skim in 2–3 minutes
- Look for buzzwords: "real-time", "batch", "unsupervised"
- Usually straightforward if business problem clearly stated

### Domain 2 (Architecture): 10–13 questions expected
- **Most important domain** (worth 5+ hours study)
- Focus on trade-offs: latency vs cost, AutoML vs custom
- Memorise 5 patterns from `architecture-patterns.md`

### Domain 3 (Data Prep): 10–13 questions expected
- Feature engineering + data quality common
- Know handling of missing values, imbalance, scaling
- 2–3 scenario questions on dirty data

### Domain 4 (Model Dev): 12–15 questions expected
- **Largest domain** (worth 6+ hours study)
- Focus on hyperparameter tuning, regularisation, distributed training
- Expect 2–3 TensorFlow/Keras code-based questions

### Domain 5 (Orchestration): 8–10 questions expected
- Pipelines, scheduling, versioning key
- 1–2 questions on conditional logic, retraining triggers

### Domain 6 (Monitor/Maintain): 5–8 questions expected
- Least tested; focus on drift detection, cost optimisation
- 1–2 questions on incident response

---

## Weakest Areas Check

Take this self-assessment:
- Problem Framing: Can I define success metrics for any scenario? (Y/N)
- Architecture: Can I sketch real-time vs batch trade-offs? (Y/N)
- Data Prep: Do I know handling for missing values, imbalance, scaling? (Y/N)
- Model Dev: Can I explain hyperparameter tuning (grid/random/Bayesian)? (Y/N)
- Orchestration: Do I understand Vertex AI Pipelines DAG structure? (Y/N)
- Monitor/Maintain: Can I diagnose data vs concept vs label drift? (Y/N)

**If any = N, spend 2–3 extra hours on that domain before exam.**

---

**Next:** Take `practice-exam.md` (6–8 scenario-based questions) to assess readiness.