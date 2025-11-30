# Responsible AI

_Last Updated: November 30, 2025_

Responsible AI ensures generative AI systems are fair, transparent, safe, and aligned with ethical principles and regulations. This is critical for business trust and compliance.

## Google AI Principles

Google's approach to responsible AI, used across Vertex AI:

1. **Beneficial:** AI should advance human flourishing
2. **Accountable:** Clear ownership and governance
3. **Fair:** Avoid bias and promote equity
4. **Transparent:** Explain how systems work
5. **Technically Sound:** Rigorous testing and monitoring
6. **Responsible:** Assess and manage risks

## Common GenAI Risks

### Bias and Fairness

**Risk:** Model discriminates against protected groups (gender, race, age, etc.)

**Examples:**
- Resume screening tool rejects female candidates (trained on male-dominated historical data)
- Loan approval system denies credit to certain ethnicities
- Medical diagnosis tool performs worse on non-white patients

**Mitigation:**
- [ ] Audit training data for representation (are all demographics equally present?)
- [ ] Test model on held-out demographic groups (verify similar accuracy)
- [ ] Use fairness metrics (demographic parity, equalized odds)
- [ ] Include diverse stakeholders in review (business, ethics, affected communities)
- [ ] Implement monitoring (alert if fairness metrics drift)

### Hallucinations (Generating False Information)

**Risk:** Model generates confident-sounding but factually incorrect content.

**Examples:**
- Medical chatbot: "Vitamin C cures cancer" (false, harmful)
- Financial advisor: "Apple stock is trading at £2,000/share" (completely fabricated)
- Legal assistant: "UK contract law requires XYZ" (misquotes actual law)

**Mitigation:**
- [ ] Use retrieval-augmented generation (RAG): ground responses in verified data
- [ ] Require human review for high-stakes decisions (medical, financial, legal)
- [ ] Add uncertainty quantification ("I'm 70% confident" vs "definitely")
- [ ] Implement fact-checking workflows
- [ ] Monitor for known false patterns and filter

### Toxicity and Safety

**Risk:** Model generates harmful, offensive, or abusive content.

**Mitigation:**
- [ ] Use content filtering (block known toxic phrases/topics)
- [ ] Test adversarially (try to "jailbreak" the model)
- [ ] Implement safety classifiers (rate toxicity of outputs)
- [ ] Have human reviewers flag concerning outputs for retraining
- [ ] Clear policies on prohibited use cases

### Privacy Violations

**Risk:** Model leaks or memorises private training data.

**Examples:**
- Model trained on patient records; someone prompts: "Name a patient with diabetes" → AI outputs real patient name
- Model trained on financial documents; prompts reveal credit card numbers

**Mitigation:**
- [ ] Use differential privacy (add noise to prevent memorisation)
- [ ] Implement data minimisation (collect/store only necessary data)
- [ ] Audit for data leakage (test if model reproduces training data)
- [ ] Implement access controls (who can query the model?)
- [ ] Audit logs (track what queries were made, when)

### Misuse and Deepfakes

**Risk:** Bad actors use AI to impersonate, defraud, or spread disinformation.

**Examples:**
- Deepfake video of CEO announcing bankruptcy (stock manipulation)
- Phishing email from "CEO" (generated with voice cloning)
- Disinformation campaign (automated fake news generation)

**Mitigation:**
- [ ] Rate-limit access (prevent abuse at scale)
- [ ] Implement authentication (verify user identity)
- [ ] Content origin labelling (mark AI-generated content)
- [ ] Watermarking (add imperceptible marks to detect generated content)
- [ ] Terms of service enforcement (prohibit misuse; suspend bad actors)

## Regulatory Compliance

### GDPR (General Data Protection Regulation)

**Applies to:** Any organisation processing personal data of EU residents.

**Key requirements for AI:**
- **Right to Explanation:** Users can request why a decision was made
- **Right to Erasure:** Users can demand their data be deleted (and model retraining)
- **Data Protection Impact Assessment:** Document risks before deploying
- **Consent:** Users must opt-in to data collection

**Implications:**
- Model must be explainable (use SHAP, LIME to show which inputs drove decision)
- Audit logs required (who accessed model, when, what decision)
- Data deletion pipelines needed (delete user data; potentially retrain model)

### UK Data Protection Act 2018

**Similar to GDPR; applies to UK organisations.**

**Key requirements:**
- Fair processing (users know how data is used)
- Purpose limitation (only use data for stated purposes)
- Data minimisation (collect only necessary data)
- Security (encrypt data, access controls)

### HIPAA (USA Healthcare)

**Applies to:** Healthcare providers, insurers, clearinghouses handling protected health information (PHI).

**Key requirements for AI:**
- Business Associate Agreement (require vendors to pledge compliance)
- Audit logs of PHI access
- Encryption of PHI in transit and at rest
- De-identification (remove patient identifiers before processing)

### NHS (UK Healthcare)

**Applies to:** Healthcare systems using NHS patient data.

**Key requirements:**
- Data Security and Protection Toolkit (annual compliance audit)
- Information Governance Review (IG Review)
- Incident reporting (data breaches to ICO within 30 days)
- Patient consent (explain data use clearly; opt-out available where possible)

**For AI specifically:**
- Fairness audit: model accuracy consistent across demographics
- Explainability: clinicians understand AI recommendations
- Safety validation: AI tested for harmful recommendations
- Human oversight: AI assists; clinicians decide

## Building Responsible AI Systems

### Step 1: Problem Definition & Stakeholder Engagement

- [ ] Define problem clearly (e.g., "reduce support costs 30%" not "build a chatbot")
- [ ] Identify stakeholders (business, tech, legal, ethics, affected communities)
- [ ] Document use cases and non-use cases (where AI should NOT be used)
- [ ] Discuss potential harms (who could be negatively impacted?)

**Example:** Before building a hiring AI:
- **Use:** Initial resume screening (suggest candidates to humans)
- **Non-use:** Final hiring decision (humans decide)
- **Harms:** Could discriminate against women, minorities, disabled people
- **Stakeholders:** HR team, legal, affected applicants, ethics board

### Step 2: Data Audit

- [ ] Is data representative of populations it will serve?
- [ ] Are there demographic imbalances (e.g., 90% of training data male)?
- [ ] Are labels consistent and unbiased (e.g., past hiring decisions already discriminatory)?
- [ ] Is sensitive data present that shouldn't influence model (zip code = proxy for race)?

**Action:** Remove or rebalance imbalanced data; remove inappropriate features.

### Step 3: Model Development with Testing

- [ ] Train baseline model
- [ ] Test on held-out demographic groups (verify similar accuracy across groups)
- [ ] Test for hallucinations (prompt model to generate false claims; count how often)
- [ ] Adversarial testing (try to "break" model; elicit toxic/harmful responses)
- [ ] Privacy testing (can model memorise and reproduce training data?)

**Metrics:**
- Accuracy gap between groups (should be <3%)
- Hallucination rate (% of outputs with factual errors)
- Toxicity detection score (% of outputs flagged as harmful)

### Step 4: Human Review & Documentation

- [ ] Have diverse reviewers (different backgrounds, expertise) evaluate model
- [ ] Document model card: performance, limitations, fairness metrics, ethical considerations
- [ ] Get sign-off from legal, ethics, security teams
- [ ] Plan for monitoring and incident response

**Model Card Example:**

```markdown
# Hiring Recommendation Model Card

## Overview
- Purpose: Suggest candidates for initial screening
- Framework: Random Forest
- Training Date: Jan 2025
- Training Data: 100k historical hires (2018–2024)

## Performance
- Accuracy: 78%
- Precision: 82%
- Recall: 72%

## Fairness
- Gender: Accuracy gap 1.2% (acceptable)
- Age: Accuracy gap 3.1% (monitor)
- Ethnicity: Cannot assess (data not available; recommend collecting)

## Limitations
- No data for non-traditional career paths (may undervalue)
- Trained on historical hires (may perpetuate past biases)
- No real-time labour market data (may miss emerging skills)

## Ethical Considerations
- No protected attributes (gender, race, age) directly in model
- Fairness audited quarterly
- Humans make final hiring decisions (model assists only)
- Audit log of all recommendations

## Recommendation
Safe for production as **screening assist tool** with:
- Quarterly fairness audits
- HR team awareness of limitations
- Diverse hiring panel reviews (model suggestions not treated as gospel)
```

### Step 5: Deployment & Monitoring

- [ ] Implement explainability (log feature importance for each prediction)
- [ ] Set up monitoring (track accuracy, fairness metrics, hallucination rate)
- [ ] Define incident response (if accuracy drops >5%, pause and investigate)
- [ ] Plan for updates (retrain model quarterly with new data)
- [ ] Communicate to users (explain how model works, its limitations)

## Exam Focus

**GenAI Leader will test:**
- [ ] Google AI Principles and how to apply them
- [ ] Common GenAI risks and mitigation strategies
- [ ] GDPR, NHS, healthcare compliance requirements
- [ ] Building responsible AI systems (steps and checkpoints)
- [ ] Fairness metrics and bias detection
- [ ] Explainability and transparency
- [ ] Incident response and governance

## Cross-References

- See `business-use-cases.md` for real-world responsible AI implementation
- See `genai-fundamentals.md` for model capabilities and limitations
- See `vertex-ai-overview.md` for Vertex AI responsible AI tools
