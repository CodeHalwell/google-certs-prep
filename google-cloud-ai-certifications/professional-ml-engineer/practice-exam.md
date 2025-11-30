# Practice Exam – Professional ML Engineer

_Last Updated: November 30, 2025_

## Instructions

- **Time limit:** 90 minutes (12 scenarios × 7.5 min each)
- **Format:** Scenario-based + multiple-choice; mimic real exam
- **Scoring:** Each question worth ~8–9 points; aim for 70% (50/70 points) to pass
- **Resources:** No external tools; use this guide + your knowledge
- **After exam:** Review model answers; identify weak domains

---

## Scenario 1: Bank Loan Approval System (15 min)

**Context:** Major UK bank (£500M annual loan portfolio) wants to build an ML system to approve/reject loan applications in real-time. Current process: manual review (2–3 days). Target: decision in <200ms.

**Current Data:**
- 2M historical loan records
- Features: age, income, employment_years, credit_score, loan_amount, loan_term
- Label: approved/rejected (80% approved, 20% rejected)
- Imbalance: Yes (minority class underrepresented)

**Questions:**

**Q1.1:** How would you frame this ML problem?
- A) Regression (predict approval probability 0–1)
- B) Binary classification (approve/reject)
- C) Clustering (segment customers)
- D) Ranking (sort applications)

**Recommended Answer:** B (primary); A also valid if probability needed. Classification fits binary decision.

---

**Q1.2:** Architecture: Choose the right serving approach.
- A) Vertex AI Endpoint (real-time, n1-standard-2, 2 replicas)
- B) Batch prediction (daily overnight scoring)
- C) BigQuery ML (queries on-demand)
- D) Cloud Run microservice (custom API)

**Recommended Answer:** A. <200ms latency requires real-time endpoint; batch violates SLA. A or D valid; A simpler.

---

**Q1.3:** Handle class imbalance (80% approved, 20% rejected). Best approach?
- A) Oversample minority class (SMOTE)
- B) Undersampling majority
- C) Weighted loss function (penalise misclassified rejected loans)
- D) Drop rejected records

**Recommended Answer:** C. Simplest in TensorFlow: `class_weight = {0: 1, 1: 4}` (weight rejected 4× more). A valid too.

---

**Q1.4:** Model selection: Best first model for loan approval?
- A) Logistic regression (interpretable, fast)
- B) Decision tree (explainable, non-linear)
- C) Neural network (high capacity)
- D) Random forest (ensemble)

**Recommended Answer:** A or B initially (baseline); A most interpretable (required for loans). Escalate to B/D if accuracy insufficient.

---

**Q1.5:** Production monitoring: What metric would alert you to model failure?
- A) Training accuracy (should stay high)
- B) Prediction latency (monitor SLA: <200ms)
- C) Approval rate (drift from historical 80%)
- D) All of above

**Recommended Answer:** D. A doesn't track production; B critical for SLA; C flags data drift (e.g., marketing shifted to lower-risk segment).

**Time:** 15 min | **Topics:** Problem framing, architecture, class imbalance, model selection, monitoring

---

## Scenario 2: E-commerce Recommendation Engine (15 min)

**Context:** Global e-commerce platform (£2B annual revenue) wants to personalise product recommendations. Current: non-personalised (all customers see trending products). Goal: increase click-through rate (CTR) from 2% to 3% (£20M revenue impact).

**Data Available:**
- 100M customer transactions (clicks, purchases)
- Features: customer_id, product_id, price, category, customer_age, purchase_history
- Labels: click (1) or no-click (0) from A/B test baseline

**Architecture Question:**

**Q2.1:** How many models needed? (Cold-start + production options)
- A) 1 model: single collaborative filtering model
- B) 2 models: cold-start (new customers) + warm (returning)
- C) 3+ models: content-based + collaborative + hybrid
- D) Real-time online ranking (no pre-trained model needed)

**Recommended Answer:** B or C. New customers have no history; need content-based (product similarity). B practical; C more accurate.

---

**Q2.2:** Which architecture minimises latency for personalised homepage (show top 10 products in <200ms)?
- A) Real-time model serving (Vertex AI Endpoint)
- B) Pre-compute daily recommendations (batch, store in Firestore)
- C) Call BigQuery for ranking (too slow)
- D) Local cached model (expensive storage)

**Recommended Answer:** B (most practical). Pre-compute top-10 per customer nightly; lookup Firestore (<50ms). A valid if budget allows.

---

**Q2.3:** How to safely deploy new recommendation model without risking revenue?
- A) A/B test: 50% old model, 50% new
- B) Canary: 95% old, 5% new; gradual rollout
- C) Shadow mode: serve new predictions offline, measure only
- D) B or C (risk-averse strategy)

**Recommended Answer:** D. B (5%) lowest risk for £20M impact; C (shadow) even safer but delayed decision. Deploy B, monitor CTR/revenue closely.

---

**Q2.4:** Monitor for model failure (data drift). What would you track?
- A) Click-through rate (CTR should stay 3%)
- B) Product diversity (are recommendations repetitive?)
- C) Input feature distribution (e.g., customer age shifted)
- D) All of above

**Recommended Answer:** D. A directly measures business metric (CTR); B checks recommendation quality; C detects input drift (trigger retrain).

**Time:** 15 min | **Topics:** Recommendation systems, cold-start, architecture choices, A/B testing, monitoring

---

## Scenario 3: Healthcare Diagnosis System (15 min)

**Context:** NHS hospital wants to build ML system to assist radiologists in detecting lung cancer from CT scans. Goal: reduce diagnosis time by 20%, maintain 99%+ accuracy (patient safety critical).

**Compliance:** GDPR, NHS Data Security & Protection Toolkit, NHS HIPAA-equivalent

**Dataset:**
- 10k CT scan images (positive: cancer, negative: no cancer)
- Class distribution: 5% cancer, 95% no cancer (highly imbalanced)
- Requirement: Explainability (radiologist must understand why model flagged image)

**Q3.1:** Which model type best balances accuracy + explainability?
- A) Deep CNN (best accuracy, low explainability)
- B) Logistic regression on hand-crafted features (explainable, lower accuracy)
- C) Ensemble CNN + attention maps (hybrid)
- D) Decision tree on image features (explainable, poor accuracy)

**Recommended Answer:** C. CNN for accuracy; attention maps show which regions triggered cancer flag (explainability). A too black-box for medical.

---

**Q3.2:** Handle extreme class imbalance (5% cancer, 95% no cancer)?
- A) Oversample positive class (SMOTE on images)
- B) Weighted loss: penalise false negatives (misdiagnosed cancer) heavily
- C) Focal loss (designed for imbalance)
- D) All reasonable (B or C preferred)

**Recommended Answer:** D. B simplest; C (focal loss) state-of-art for imbalance. Skip A (SMOTE harder for images).

---

**Q3.3:** Validation strategy for medical ML (patient safety)?
- A) 80/20 train/test split
- B) k-fold cross-validation
- C) Stratified k-fold (ensure both classes in each fold)
- D) Leave-one-out cross-validation (expensive but thorough)

**Recommended Answer:** C. Stratified preserves 5%/95% ratio in each fold. Important for imbalanced data.

---

**Q3.4:** Deployment: Real-time vs batch for radiologist workflow?
- A) Real-time (radiologist uploads scan → instant prediction)
- B) Batch nightly (predict all pending scans)
- C) Hybrid (real-time with human-in-loop approval)
- D) Offline training (no deployment; used for research)

**Recommended Answer:** C (ideal for medical). Real-time model prediction, but radiologist reviews + approves before action. Avoids autonomous medical decisions (regulatory risk).

---

**Q3.5:** Regulatory compliance: What governance needed?
- A) Regular audit trail (predict → reason → radiologist decision)
- B) Right-to-explanation (GDPR): patient can ask "why flagged"
- C) Fairness monitoring (model accuracy by age, gender, ethnicity)
- D) All of above + NHS approval

**Recommended Answer:** D. A (audit trail) tracks decisions. B (GDPR) required. C (fairness) prevents discrimination. NHS approval gate deployment.

**Time:** 15 min | **Topics:** Medical ML, explainability, class imbalance, validation, governance, compliance

---

## Scenario 4: Demand Forecasting (Multi-Cloud) (12 min)

**Context:** Global retail chain operates in 50 countries. Inventory planning uses naive forecasts (last year + 10%). Goal: reduce inventory costs by 15% (£50M savings) via ML demand forecasting.

**Constraints:**
- Data spread across AWS (US), GCP (EU), Azure (APAC)
- Model trained on GCP (best ML tools)
- Serve predictions on local clouds (latency + compliance)

**Q4.1:** Multi-cloud strategy: How to centralise training, decentralise serving?
- A) Train on GCP only; export model to AWS/Azure
- B) Train model registry (Weights & Biases / Databricks) accessible to all clouds
- C) Replicate dataset to all clouds; train separately
- D) Use only GCP (no multi-cloud)

**Recommended Answer:** B. Centralised model registry (W&B/Databricks); each cloud pulls model + deploys locally. Avoids duplication.

---

**Q4.2:** Data privacy: US sales data in AWS, EU in GCP. Mixing for training?
- A) Yes; centralise all data to GCP (best ML tools)
- B) No; GDPR forbids EU data to US (AWS)
- C) Train separate models per region (EU model, US model)
- D) Use federated learning (train on local data without centralising)

**Recommended Answer:** D (ideal) or C. B partially correct (GDPR restricts EU→US; AWS EU region OK). D avoids data transfer entirely.

---

**Q4.3:** Cost optimisation: 1M store-level daily forecasts, latency <5 min OK. Best approach?
- A) Real-time endpoint on each cloud (expensive, 3× £40/month)
- B) Batch daily prediction (£5–10 total, but delayed)
- C) Hybrid: batch for 95% standard products, real-time for fast-movers
- D) On-device models (edge)

**Recommended Answer:** C (practical). Batch = £6/month; real-time for urgent = £15/month. Total ~£21/month vs £120 (all real-time). 82% savings.

**Time:** 12 min | **Topics:** Multi-cloud architecture, GDPR privacy, cost optimisation, forecasting

---

## Scenario 5: Model Monitoring & Incident Response (10 min)

**Context:** Production fraud detection model (real-time endpoint, 100 QPS). Monitors 1M transactions/day.

**Alert:** Today, fraud detection rate dropped 40% (yesterday: 0.8% flagged, today: 0.48%). Revenue loss: £2M/day.

**Q5.1:** Diagnose: What likely happened?
- A) Model bug or code deployment error
- B) Data drift (fraud patterns changed)
- C) Concept drift (new fraud type not seen in training)
- D) Any of above (need investigation)

**Recommended Answer:** D. Quick checks: (1) Code changed? (2) Input features different? (3) Fraud type changed (criminals adapted)?

---

**Q5.2:** Immediate action plan (next 30 min)?
- A) Rollback to previous model (v1)
- B) Investigate logs + feature importance
- C) Retrain on latest data
- D) A then B (safe first, investigate later)

**Recommended Answer:** A. Fraud costs money → rollback ASAP (5 min). Then investigate (B) in parallel.

---

**Q5.3:** Root cause analysis (post-incident). Where would you look?
- A) Model performance metrics (accuracy, precision, recall)
- B) Feature distributions (feature drift)
- C) Label quality (were recent labels correct?)
- D) All of above

**Recommended Answer:** D. Check (A) baseline model still works? (B) did feature sources change? (C) did fraud labeling process change?

**Time:** 10 min | **Topics:** Monitoring, incident response, drift detection, debugging

---

## Scenario 6: Feature Engineering & Model Selection (12 min)

**Context:** Customer churn prediction (telecom company). Current model: logistic regression on 10 raw features. Accuracy: 82%.

**Problem:** Model doesn't capture customer lifecycle patterns (e.g., "long-time customer with spike in support tickets" = churn risk).

**Q6.1:** Feature engineering: What new features might help?
- A) Temporal: days_since_signup, support_tickets_last_30d, call_volume_trend
- B) Interaction: high_support_tickets AND low_revenue = churn risk
- C) Aggregations: avg_monthly_bill_last_3m, std_deviation (volatility)
- D) All of above (multi-faceted)

**Recommended Answer:** D. Temporal captures lifecycle; interactions model relationships; aggregations detect patterns.

---

**Q6.2:** Model upgrade: Logistic regression → Random Forest? Trade-offs?
- A) Pros: non-linear, feature interactions captured; Cons: slower, less interpretable
- B) Pros: higher accuracy; Cons: higher cost (training time)
- C) Pros: automatic feature selection; Cons: overfitting risk
- D) All of above

**Recommended Answer:** D (all true). Random Forest captures interactions but slower. Test on hold-out set first.

---

**Q6.3:** Validate new features (prevent overfitting)?
- A) Cross-validation (k-fold on full dataset)
- B) Hold-out test set (80/20 split, never touch test until final eval)
- C) A + B (k-fold on training set, then test on hold-out)
- D) None (manual inspection of feature importance)

**Recommended Answer:** C. k-fold on 80% (training); then evaluate on held-out 20%. Prevents data leakage.

**Time:** 12 min | **Topics:** Feature engineering, model selection, validation

---

## Summary & Scoring

| Scenario | Topics | Points |
|----------|--------|--------|
| 1. Loan Approval | Problem framing, architecture, imbalance, model selection, monitoring | 15 |
| 2. Recommendation | Recommendation systems, cold-start, A/B testing, monitoring | 15 |
| 3. Healthcare | Medical ML, explainability, imbalance, validation, governance | 15 |
| 4. Demand Forecast | Multi-cloud, privacy, cost optimisation | 12 |
| 5. Incident Response | Monitoring, debugging, rollback | 10 |
| 6. Feature Engineering | Feature engineering, model selection, validation | 12 |
| **Total** | | **79 points** |

**Passing:** 55+ (70%) → confident for real exam  
**Review needed:** <55 → revisit weak domains before exam

---

## Answer Review Checklist

After completing:
- [ ] Scenario 1: Can you explain architecture trade-offs (real-time vs batch)?
- [ ] Scenario 2: Do you understand A/B testing for recommendations?
- [ ] Scenario 3: Can you explain explainability requirements for medical ML?
- [ ] Scenario 4: Do you grasp multi-cloud + privacy trade-offs?
- [ ] Scenario 5: Could you create an incident response runbook?
- [ ] Scenario 6: Can you articulate feature engineering impact on model?

---

## Weak Areas Guide

**If struggling with:**
- Problem framing → Revisit `exam-domains.md` (Domain 1)
- Architecture choices → Study `architecture-patterns.md` (5 key patterns)
- Data handling → Review `learning-paths/03-tensorflow-keras.md` (preprocessing, validation)
- Model techniques → Deep dive `learning-paths/05-model-optimization.md` (hyperparameter tuning, regularisation)
- Orchestration → Complete `hands-on-labs/vertex-ai-labs.md` (Lab 3: pipelines)
- Monitoring → Read `learning-paths/04-mlops-deployment.md` (monitoring + drift)

---

**Final Advice:** These 6 scenarios test integrated knowledge (not isolated facts). Success requires understanding **why** each choice matters, not memorising answers. Focus on reasoning; the exam will have novel scenarios.

**Feeling ready?** Schedule your exam via [Google Cloud Certification](https://cloud.google.com/certification/cloud-certified-professional-machine-learning-engineer). Good luck!

---

**Last Updated:** November 30, 2025