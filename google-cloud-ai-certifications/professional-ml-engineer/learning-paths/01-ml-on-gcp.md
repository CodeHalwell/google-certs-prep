# Learning Path 01 – ML on Google Cloud

_Last Updated: November 30, 2025_

**Difficulty:** Intermediate–Advanced  
**Estimated time:** 8–12 hours

## Goals

- [ ] Understand the Google Cloud ML ecosystem and when to use each service
- [ ] Learn when to use BigQuery ML, Vertex AI, and pre-trained APIs
- [ ] Build a cost-aware mental model of ML solutions on GCP

## Key Topics

### Google Cloud ML Ecosystem Overview

**The challenge:** ML projects involve data ingestion, preprocessing, training, evaluation, and deployment. Google Cloud offers a toolkit of services; the art is picking the right combination for your use case.

**Services overview:**

- **BigQuery ML (BQML):** SQL-based ML; train models using SQL queries
- **Vertex AI AutoML:** Point-and-click model training (minimal code)
- **Vertex AI custom training:** Bring your own code (TensorFlow, PyTorch, scikit-learn); run on managed infrastructure
- **Pre-trained APIs:** Vision AI, Natural Language AI, Document AI; no training needed
- **Dataflow:** ETL and data preprocessing at scale

### When to Use BigQuery ML

**Best for:**
- Tabular/structured data already in BigQuery
- Quick prototypes and proof-of-concepts
- Your team knows SQL better than Python

**Strengths:**
- No data movement: train and predict directly in BigQuery
- Fast: SQL-based syntax, low latency
- Cost-effective: pay only for queries (no separate ML infrastructure)

**Limitations:**
- Limited model types (linear/logistic regression, time-series forecasting, clustering, XGBoost, TensorFlow DNN)
- No transfer learning or complex architectures
- Not suitable for unstructured data (images, text)

**Example:** Credit scoring model: SELECT features FROM transactions_table; CREATE OR REPLACE MODEL credit_score_model AS SELECT ... (BigQuery ML automatically handles train/test split, scaling, etc.)

### When to Use Vertex AI AutoML

**Best for:**
- Structured data or images/text that you want to train quickly
- Teams without ML expertise
- Time-to-value is critical

**Strengths:**
- No code: use console or simple APIs
- Google handles hyperparameter tuning, feature engineering, ensemble building
- Scales: can train on large datasets

**Limitations:**
- Less control over the model architecture
- Hidden complexity: you don't see exactly what the model is doing
- Cost: AutoML jobs can be expensive (charged for training time + compute)

**Example:** Image classification for healthcare: Upload labeled images to Vertex AI AutoML; Google trains a model automatically; deploy to an endpoint.

### When to Use Vertex AI Custom Training

**Best for:**
- Your own TensorFlow, PyTorch, or scikit-learn code
- Complex architectures (RNNs, Transformers, multi-modal models)
- Fine-tuning pre-trained models

**Strengths:**
- Full control: use any framework, architecture, loss function
- Scalability: distributed training on multiple GPUs/TPUs
- Reproducibility: your code, your versioning

**Workflow:**
1. Write training code (train.py) and save to Cloud Storage
2. Create a Docker image with your code and dependencies
3. Submit to Vertex AI Training with machine type (CPU, GPU, TPU) and scaling options
4. Vertex AI provisions infrastructure, runs training, saves model

**Cost:** You pay only for compute used (per GPU/TPU hour)

**Example:** Fine-tuning a BERT model for clinical text classification: package your training code, push Docker image to Artifact Registry, submit to Vertex AI Training.

### Pre-Trained APIs

**What they are:** Google-hosted models ready to use; no training needed. You just call an API.

**Examples:**
- **Vision AI:** Image classification, object detection, optical character recognition (OCR)
- **Natural Language AI:** Sentiment analysis, entity recognition, document classification
- **Document AI:** Extract structured data from scanned documents
- **Translation API:** Translate between 100+ languages

**Cost model:** Pay per request (usually pennies to fractions of a pound)

**Best for:**
- Quick wins (no training time)
- Off-the-shelf tasks where you don't need customisation
- Prototypes and MVPs

**Limitation:** Limited to what Google offers; can't fine-tune most APIs

**Example:** Sentiment analysis of customer feedback: call Natural Language AI API; returns sentiment scores (no model training needed).

### Data Preparation and Preprocessing

**Reality:** 80% of ML work is data preparation, not training.

**On GCP:**
- **Dataflow:** Apache Beam jobs for large-scale ETL (extract, transform, load)
- **BigQuery:** SQL transformations, feature engineering
- **Vertex AI Workbench:** Pandas, PySpark for interactive preprocessing

**Common tasks:**
- Handling missing values
- Scaling/normalisation (mean 0, std 1)
- Encoding categorical variables
- Feature engineering (derive new features from raw data)
- Train/test splitting
- Addressing class imbalance

**Cost tip:** Use Dataflow for large pipelines; use BigQuery SQL for quick transformations; use Workbench notebooks for exploration (then move to Dataflow for production).

## Cost Considerations

### Rough Cost Comparison (GBP)

**Scenario:** Training a tabular model on 1 million rows, 100 features

| Approach | Setup | Training | Prediction (per 1000 rows) | Notes |
|----------|-------|----------|---------------------------|-------|
| BigQuery ML | £0 | £5–20 (query cost) | £0.50 | Cheapest; SQL-only |
| Vertex AutoML | £0 | £100–500 | £1–5 | Managed; higher cost |
| Custom (1 GPU, 1h) | £50–200 (infrastructure setup) | £50–100 | £1–3 | Full control; pay for compute |
| Pre-trained API | £0 | N/A (no training) | £10–100/month | No training; pay per call |

**Rule of thumb:** Start with BigQuery ML for quick wins; move to Vertex AutoML if you need non-SQL models; use custom training for advanced requirements.

## Exam Focus

**PMLE exam will test:**
- [ ] When to use which service (decision trees, trade-offs)
- [ ] Cost optimisation (choosing cheaper options where feasible)
- [ ] Data preparation best practices
- [ ] Understanding of ML lifecycle (data → train → evaluate → deploy)

## Cross-References

- See `learning-paths/02-vertex-ai.md` for hands-on Vertex AI usage
- See `code-examples/` for concrete examples of custom training and deployment
- See `../shared-resources/cost-optimization.md` for detailed GBP budgeting
