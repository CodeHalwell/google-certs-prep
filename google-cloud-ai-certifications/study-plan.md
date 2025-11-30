# 6‑Month Integrated Study Plan

_Last Updated: November 30, 2025_

This plan assumes you are working full‑time and can dedicate **8–12 hours per week**. It is designed so that each certification builds on the previous one:

- Month 1–2: **Associate Cloud Engineer (ACE)** – core GCP platform skills
- Month 3: **Generative AI Leader** – business and strategy layer
- Month 4–6: **Professional Machine Learning Engineer (PMLE)** – deep technical and MLOps

Use the checkboxes to track progress and adapt based on your schedule.

---

## Month 1–2 – Associate Cloud Engineer

**Primary goals:**

- Understand how GCP projects, billing, IAM, and core services fit together.
- Become comfortable deploying, configuring, and operating workloads using the console and `gcloud`.
- Build a mental model that will support GenAI and ML work later.

### Weeks 1–2 – Core Services (Compute & Storage)

- [ ] Read: `associate-cloud-engineer/core-services/compute-engine.md`
- [ ] Read: `associate-cloud-engineer/core-services/kubernetes-engine.md`
- [ ] Read: `associate-cloud-engineer/core-services/app-engine.md`
- [ ] Read: `associate-cloud-engineer/core-services/cloud-run.md`
- [ ] Lab: Deploy a simple web app to Compute Engine, App Engine, or Cloud Run.
- [ ] Storage: `associate-cloud-engineer/storage-databases/cloud-storage.md` and set up at least one bucket with lifecycle rules.

**Outcome:** You can explain when to use Compute Engine vs GKE vs App Engine vs Cloud Run, and you can deploy a basic service to at least one of them.

### Weeks 3–4 – Networking & Security

- [ ] Networking: `associate-cloud-engineer/networking/vpc-fundamentals.md`, `load-balancing.md`, `cloud-dns.md`.
- [ ] Security: `associate-cloud-engineer/iam-security/identity-access-management.md`, `service-accounts.md`, `security-best-practices.md`.
- [ ] Lab: Build a small VPC with subnets, firewall rules, and an HTTP(S) load balancer.
- [ ] Configure DNS for a test domain or subdomain pointing at your load balancer (where feasible).

**Outcome:** You can design a simple, secure VPC-based architecture and reason about IAM roles vs service accounts.

### Weeks 5–6 – Storage, Databases, and Operations

- [ ] Databases: `associate-cloud-engineer/storage-databases/cloud-sql.md`, `firestore.md`, `bigtable.md` (skim Bigtable if short on time).
- [ ] Operations: `associate-cloud-engineer/monitoring-operations/cloud-monitoring.md`, `cloud-logging.md`, `error-reporting.md`.
- [ ] Lab: Deploy an app backed by Cloud SQL or Firestore and monitor it.
- [ ] Configure basic billing alerts in the GCP console.

**Outcome:** You know how to pick the right storage/database option and how to monitor and troubleshoot a small GCP deployment.

### Weeks 7–8 – Labs, Revision & Exam Readiness

- [ ] Work through the ACE-focused labs listed in `associate-cloud-engineer/hands-on-labs/README.md`.
- [ ] Review `shared-resources/gcp-fundamentals.md` and `gcloud-cli-reference.md`.
- [ ] Attempt `associate-cloud-engineer/practice-exam.md` under timed conditions.
- [ ] Book the ACE exam (see `shared-resources/exam-booking-guide.md`).

**Target:** Sit the **Associate Cloud Engineer** exam at the end of Month 2.

---

## Month 3 – Generative AI Leader

**Primary goals:**

- Be able to articulate GenAI concepts, risks, and opportunities to business stakeholders.
- Understand where Vertex AI and Gemini fit into broader digital transformation.
- Craft credible, ROI-aware GenAI proposals, with a focus on healthcare and consultancy work.

### Weeks 9–10 – GenAI Fundamentals & Business Use Cases

- [ ] Read: `generative-ai-leader/genai-fundamentals.md` and `study-materials.md`.
- [ ] Skills Boost: Complete the Generative AI learning path (or equivalent role-based path).
- [ ] Draft 2–3 GenAI use cases for your consultancy (client-facing and internal productivity).
- [ ] Tailor at least one use case to healthcare (see `generative-ai-leader/business-use-cases.md`).

### Week 11 – Vertex AI & Responsible AI

- [ ] Read: `generative-ai-leader/vertex-ai-overview.md`.
- [ ] Read: `generative-ai-leader/responsible-ai.md` and cross-check with official Google AI Principles.
- [ ] Design a GenAI solution outline including: objectives, success metrics, data sources, and risk controls.

### Week 12 – Practice & Exam Readiness

- [ ] Work through `generative-ai-leader/practice-questions.md`.
- [ ] Prepare a short slide deck or written brief pitching a GenAI initiative.
- [ ] Book and sit the **Generative AI Leader** exam.

---

## Month 4–6 – Professional Machine Learning Engineer

**Primary goals:**

- Design and implement production-grade ML systems on GCP.
- Use Vertex AI, TensorFlow, and MLOps best practices confidently.
- Cover all PMLE domains with both theory and hands-on practice.

### Weeks 13–14 – ML Foundations & ML on GCP

- [ ] Review ML theory (supervised/unsupervised, evaluation metrics, overfitting, etc.).
- [ ] Read: `professional-ml-engineer/learning-paths/01-ml-on-gcp.md`.
- [ ] Labs: Start with "Perform Foundational Data, ML, and AI Tasks in Google Cloud" and related Skills Boost content.
- [ ] Implement a simple model locally (e.g. `tensorflow-examples/01-keras-baseline.py`).

### Weeks 15–16 – Vertex AI & TensorFlow/Keras

- [ ] Read: `professional-ml-engineer/learning-paths/02-vertex-ai.md` and `03-tensorflow-keras.md`.
- [ ] Notebook: run `professional-ml-engineer/pmle-end-to-end.ipynb` for an AutoML tabular E2E flow.
- [ ] Code: adapt `vertex-ai-sdk/02-dataset-creation.py` and `03-automl-training.py` to your own dataset.

### Weeks 17–18 – MLOps, Deployment & Serving Patterns

- [ ] Read: `professional-ml-engineer/learning-paths/04-mlops-deployment.md`.
- [ ] Build a CI/CD flow using Cloud Build and Cloud Run or GKE for an ML-backed service.
- [ ] Deploy the FastAPI → Vertex AI gateway in `deployment-scripts/fastapi-vertex-endpoint/`.

### Weeks 19–20 – Optimisation & Responsible ML

- [ ] Read: `professional-ml-engineer/learning-paths/05-model-optimization.md` and `06-responsible-ml.md`.
- [ ] Run at least one hyperparameter tuning experiment (Vertex AI Vizier) and monitor metrics.
- [ ] Evaluate a model’s fairness, explainability, and drift using Vertex AI tools where possible.

### Weeks 21–22 – Advanced Labs & Case Studies

- [ ] Complete labs listed in `professional-ml-engineer/hands-on-labs/` (Vertex AI, MLOps, production systems).
- [ ] Document lessons learned in your own words, especially where they map to exam domains.

### Weeks 23–24 – Practice Exams & Final Review

- [ ] Work through `professional-ml-engineer/practice-exam.md`.
- [ ] Use `exam-domains.md` as a checklist to find and shore up weak areas.
- [ ] Book and sit the **Professional ML Engineer** exam.

---

For more detail, use the learning paths, topic files, and lab guides under each certification folder, as well as `premium-resources.md` for premium-only content.