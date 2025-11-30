# Learning Path 06 – Responsible ML

_Last Updated: November 30, 2025_

**Difficulty:** Advanced  
**Estimated time:** 8–12 hours

Responsible AI ensures models are fair, transparent, accountable, and aligned with ethical principles. This path covers bias detection, fairness metrics, and governance.

## Bias and Fairness

### What Is Bias?

**Bias:** Systematic error or unfairness in predictions across demographic groups.

**Common sources:**
1. **Historical bias:** Training data reflects past discrimination (e.g., hiring data biased against women)
2. **Representation bias:** Training data underrepresents certain groups (e.g., few non-binary examples)
3. **Measurement bias:** How labels are defined is biased (e.g., "creditworthiness" historically defined to exclude certain groups)
4. **Aggregation bias:** One-size-fits-all model performs poorly on minority groups

### Example: Loan Default Prediction

**Biased model:** Predicts lower default risk for applicants from wealthy neighbourhoods (which historically had better credit access).

**Result:** Denies loans to creditworthy applicants from disadvantaged areas, perpetuating inequality.

**Fix:** Train on features that reflect creditworthiness (income, employment, credit history) not neighbourhood.

## Fairness Metrics

### Demographic Parity

**Definition:** Equal prediction rates across groups.

$$P(\hat{Y} = 1 | A = \text{group0}) = P(\hat{Y} = 1 | A = \text{group1})$$

**Example:** Loan approval rate is 60% for both men and women.

**Challenge:** May require rejecting qualified applicants to balance rates.

### Equalized Odds

**Definition:** Equal true positive and false positive rates across groups.

$$P(\hat{Y} = 1 | Y = 1, A = \text{group0}) = P(\hat{Y} = 1 | Y = 1, A = \text{group1})$$

**Interpretation:** If a qualified applicant applies, they have equal chance of approval regardless of group.

### Calibration

**Definition:** Predicted probabilities match actual outcomes within each group.

**Example:** Model predicts 70% loan approval for Group A and 70% for Group B; actual approval rates are ~70% in both groups.

### Detecting Fairness Issues

```python
from fairness_indicators.python import fairness_indicators
from tensorflow_model_analysis import model_eval_lib

# Compute fairness metrics
metrics_dict = fairness_indicators.compute_fairness_metrics(
    eval_result=eval_result,
    protected_columns=['gender', 'age_group'],
    thresholds=[0.5]
)

# Display results
for metric, values in metrics_dict.items():
    print(f"{metric}:")
    for group, value in values.items():
        print(f"  {group}: {value:.4f}")
```

## Transparency and Explainability

### Feature Attribution (SHAP)

**Goal:** Understand which features contributed most to a prediction.

```python
import shap

# Create explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Plot: which features push predictions up/down?
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

**Output:** "This loan default prediction (0.75 probability) is driven by low income (−0.2 contribution) and high debt (0.15 contribution)."

### LIME (Local Interpretable Model-Agnostic Explanations)

Explain individual predictions by approximating model with simple rules.

```python
import lime.tabular

explainer = lime.tabular.LimeTabularExplainer(
    X_train,
    feature_names=X_train.columns,
    class_names=['No Default', 'Default'],
    mode='classification'
)

# Explain a single prediction
exp = explainer.explain_instance(X_test.iloc[0], model.predict_proba)
exp.show_in_notebook()
```

**Output:** "This prediction is based on: debt-to-income > 0.5 (default likelihood +0.3), employment > 5 years (default likelihood −0.2)."

### Model Cards

Document your model transparently:

```markdown
# Loan Default Prediction Model Card

## Overview
- **Purpose:** Predict loan default risk
- **Framework:** Random Forest
- **Training Date:** 2025-01-15
- **Data:** 500k loans (2020–2024)

## Performance
- **Accuracy:** 87%
- **Recall (correctly identifying defaults):** 72%
- **Precision:** 88%

## Fairness Analysis
- **Gender:** ±2% accuracy difference (acceptable)
- **Age:** ±1% accuracy difference (acceptable)
- **Geography:** ±3% accuracy difference (borderline; recommend monitoring)

## Limitations
- No historical data for recent immigrants; model may underperform
- Does not consider alternative credit scores (e.g., rent payment history)
- Trained on 2020–2024; may not reflect economic shifts post-2024

## Ethical Considerations
- No protected attributes directly in model
- Fairness audited quarterly
- Model decisions are explainable (SHAP values logged)

## Recommendation
Safe for production with quarterly fairness audits.
```

## Privacy-Preserving ML

### Differential Privacy

Add noise to data or model to prevent membership inference attacks.

```python
import tensorflow as tf
from tensorflow_privacy import keras

# Train with differential privacy
optimizer = keras.DPKerasSGDOptimizer(
    l2_norm_clip=1.0,  # Clip gradients
    noise_multiplier=1.1,  # Add noise
    num_microbatches=256
)

model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy')
model.fit(X_train, y_train, epochs=5)
```

**Trade-off:** Model accuracy decreases slightly (usually <2%); privacy guarantee: attacker cannot reliably determine if specific record was in training data.

### Federated Learning

Train model across multiple devices without centralising data.

```python
# Pseudocode: train on-device, aggregate on server
def federated_train(device_id):
    # Each device loads local data
    local_data = load_device_data(device_id)
    
    # Download current model from server
    model = download_model_from_server()
    
    # Train locally
    model.fit(local_data, epochs=1)
    
    # Upload weight updates (not data)
    upload_weight_updates_to_server(model.get_weights())

# Server aggregates updates
aggregated_weights = average_weight_updates(all_device_updates)
broadcast_to_all_devices(aggregated_weights)
```

**Use case:** Mobile keyboard prediction; no keystroke data leaves device.

### Data Minimisation

Only collect and use necessary data.

**Example:** Instead of logging full customer behaviour, log only aggregate metrics (e.g., "user clicked ad" not "user browsed for 5 min at 14:32").

## Regulatory Compliance

### GDPR (General Data Protection Regulation)

**Key requirements:**
- **Right to explanation:** Users can request why model made a decision
- **Right to erasure:** Users can demand their data be deleted
- **Consent:** Users must consent to data collection

**Implication for ML:**
- Model decisions must be explainable (use SHAP, LIME)
- Store audit logs (who accessed model, when)
- Implement data deletion pipelines

### NHS & Healthcare

**Additional requirements:**
- Models using NHS data must meet strict security/privacy standards
- Fairness audits mandatory (equity of access across demographics)
- Explainability required for clinical decisions

**Example:** Sepsis prediction model must:
- Log which features triggered "high sepsis risk" alert
- Allow clinicians to understand reasoning
- Be regularly audited for fairness across patient demographics

## Model Governance

### Model Validation Checklist

Before deploying any model:

- [ ] Accuracy meets threshold (e.g., > 85%)
- [ ] Fairness audited (all groups within ±3% accuracy)
- [ ] Privacy reviewed (no sensitive data leakage)
- [ ] Explainability tested (can generate SHAP values)
- [ ] Monitored for drift (data/concept drift detection in place)
- [ ] Model card written and reviewed
- [ ] Regulatory compliance verified (GDPR, healthcare, etc.)

### Version Control

```yaml
# Model metadata in model-config.yaml
model_id: churn-prediction-v2
training_date: 2025-01-15
data_version: dataset-2024-12
framework: tensorflow-2.11
code_commit: abc123def456

fairness_metrics:
  gender: accuracy_diff: 0.01
  age_group: accuracy_diff: 0.02

performance_metrics:
  accuracy: 0.92
  auc: 0.88
  recall: 0.85

owner: jane@company.com
approved_by: ml-governance-board
```

### Incident Response

Document what to do if model misbehaves:

```markdown
## Incident Response Plan

### Alert Triggers
- Model accuracy drops >5% in 24h
- Fairness drift: any group accuracy drops >3%
- Prediction volume anomaly: >2σ deviation from baseline

### Response Steps
1. Pause model deployment (revert to previous version)
2. Investigate: check data drift, concept drift, code changes
3. Retrain model on fresh data
4. Validate fairness and performance
5. Re-deploy after approval

### Escalation
- Prediction accuracy: escalate to ML team lead
- Fairness issue: escalate to ethics officer
- Data breach: escalate to security team
```

## Exam Focus

**PMLE will test:**
- [ ] Identifying and mitigating bias in ML models
- [ ] Fairness metrics (demographic parity, equalized odds, calibration)
- [ ] Explainability techniques (SHAP, LIME, feature importance)
- [ ] Privacy considerations (differential privacy, federated learning)
- [ ] Regulatory compliance (GDPR, healthcare)
- [ ] Model governance and validation
- [ ] Monitoring and incident response

## Cross-References

- See `02-vertex-ai.md` for Vertex AI Explainable AI tools
- See `04-mlops-deployment.md` for model governance and versioning
- See `code-examples/` for fairness testing code patterns
