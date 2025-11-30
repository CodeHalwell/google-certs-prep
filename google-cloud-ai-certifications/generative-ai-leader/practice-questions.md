# Practice Questions – Generative AI Leader

_Last Updated: November 30, 2025_

These scenario-based questions mirror exam style. Each question tests business acumen, technical understanding, and responsible AI awareness.

## Question 1: Customer Support Chatbot ROI

**Scenario:** Your company (500 employees, £50M revenue) spends 3% of revenue on customer support (£1.5M/year). Average support cost per ticket is £25; resolution time is 4 hours. You're considering deploying a Vertex AI chatbot to handle 70% of routine queries.

**Implementation costs:**
- Setup: £100k
- Annual operational cost: £50k (hosting, fine-tuning)
- Employee retraining: £20k

**Expected impact:**
- Reduce support headcount by 25% (save salary)
- Reduce average resolution time to 0.5 hours for chatbot-handled tickets
- Customer satisfaction same or slightly better

**Questions:**
1. Calculate annual cost savings (consider only salary savings and reduced tickets)
2. What's the payback period?
3. What risks would you raise to leadership?
4. How would you measure fairness in the chatbot?

**Model Answer:**
1. **Savings:**
   - Salary savings (25% × 20 support staff × £30k): ~£150k/year
   - Operational savings (fewer escalations, faster resolution): ~£50k/year
   - **Total: £200k/year**

2. **Payback:** (£100k setup + £20k training + £50k Year 1 opex) / £200k = 0.85 years (~10 months)

3. **Risks:**
   - Chatbot hallucinations causing customer frustration (mitigate: human review of common responses)
   - Discriminatory outcomes (e.g., chatbot less helpful to non-English speakers)
   - Job displacement and morale issues (mitigate: upskilling for team members)
   - Technical failures leading to customer outages (mitigate: graceful fallback to human agents)

4. **Fairness:**
   - Test chatbot on diverse queries (English, accents, dialects, accessibility needs)
   - Track resolution rate by demographic (if possible)
   - Monitor customer satisfaction scores by group
   - Set alert if any group has >5% lower satisfaction

---

## Question 2: Generative AI for Clinical Documentation

**Scenario:** A mid-sized NHS hospital trust wants to reduce clinician documentation burden using Vertex AI to auto-transcribe and summarise clinical notes. Current state: clinicians spend 2 hours/day on documentation; patient face-time only 4 hours/day.

**Constraints:**
- Patient data is PHI (Protected Health Information)
- Fairness audit required (no demographic disparities)
- Regulatory approval needed (NHS trust, GDPR compliance)

**Questions:**
1. What data governance measures must be in place?
2. What fairness metrics would you define?
3. How would you structure the responsible AI approval process?
4. What are the risks and mitigations?

**Model Answer:**
1. **Data Governance:**
   - Encryption in transit (TLS) and at rest (AES-256)
   - Access control: only authenticated clinicians can upload data
   - Audit logs: record all uploads, accesses, deletions
   - Data retention: delete transcripts after 30 days unless explicitly archived
   - De-identification: remove patient names, NHS numbers before any processing
   - Data Processing Agreement (DPA) with GCP (GDPR requirement)

2. **Fairness Metrics:**
   - Transcription accuracy by accent/language (English RA, Scottish, non-native speakers)
   - Summarisation quality by patient demographic (age, gender, ethnicity, disability)
   - Measure: Are recommendations equally clear for all groups?
   - Baseline: All groups within ±3% accuracy

3. **Approval Process:**
   - Step 1: Clinical Lead reviews prototype, provides feedback
   - Step 2: Information Governance (IG) review (data handling, legal)
   - Step 3: Ethics Committee review (fairness, consent, patient rights)
   - Step 4: Pilot on 50 patients with voluntary consent
   - Step 5: Evaluate fairness metrics; get approval from IG and Ethics
   - Step 6: Broader rollout with monitoring

4. **Risks & Mitigations:**
   - **Hallucination:** Summariser generates false clinical info → **Mitigation:** Clinician reviews all summaries; AI assists only
   - **Bias:** Worse transcription for certain accents → **Mitigation:** Test diverse accents; retrain if issues found
   - **Privacy:** PHI leaked or memorised → **Mitigation:** Use differential privacy, audit for data leakage
   - **Liability:** AI error contributes to adverse outcome → **Mitigation:** Clear documentation that AI assists; human decides

---

## Question 3: Personalised Email Marketing Campaign

**Scenario:** E-commerce company (£10M annual email revenue, 5M email subscribers) wants to deploy Vertex AI to personalise email campaigns. Goal: 20% increase in email revenue (from £10M to £12M).

**Data available:**
- Customer purchase history (anonymised)
- Browsing behaviour (anonymised)
- Email open/click history
- Demographics (age, location, purchase frequency)

**Questions:**
1. What are the legal/ethical considerations (GDPR, fairness)?
2. How would you structure the campaign to measure ROI?
3. What could go wrong, and how would you mitigate?

**Model Answer:**
1. **Legal/Ethical:**
   - **Consent:** Customers must have explicitly opted into personalised marketing (GDPR)
   - **Transparency:** Disclose that AI is personalising content
   - **Fairness:** Ensure model doesn't discriminate by demographic (e.g., show discounts unfairly to certain groups)
   - **Data rights:** Customers can request deletion; must be able to opt-out personalistion
   - **Auditable:** Log which personalisation rules applied to each customer

2. **ROI Structure (A/B Test):**
   - **Control (1M customers):** Traditional email template
   - **Test (4M customers):** Personalised email
   - **Metrics:**
     - Open rate (control vs test)
     - Click rate (control vs test)
     - Conversion rate (control vs test)
     - Revenue per email (control vs test)
   - **Duration:** 4 weeks minimum for statistical significance
   - **Success threshold:** >10% lift in revenue per email

3. **Risks & Mitigations:**
   - **Hallucination/Poor Recommendations:** AI suggests irrelevant products → **Mitigation:** Manually curate top 10 product categories shown; AI personalises within guardrails
   - **Discrimination:** AI shows lower prices to certain demographics → **Mitigation:** Fairness audit; ensure pricing consistent within demographic groups
   - **Opt-Out Failure:** Customers request personalisation stop but don't hear from AI → **Mitigation:** Immediate application of opt-out; weekly compliance audit
   - **Unintended Outcomes:** Email frequency perceived as spam → **Mitigation:** Respect existing frequency caps; allow customer controls

---

## Question 4: Responsible AI for Loan Approval

**Scenario:** Fintech company uses Vertex AI to approve personal loans (£100–£10k) for UK customers. Current approval rate: 60% (approved/total applicants). Goal: Speed up decisions while maintaining fairness.

**Data:**
- Income, employment, credit score, debt-to-income ratio
- Also available (but concerning): postcode, age, gender, marital status

**Questions:**
1. Which features should be included in the model and why?
2. What fairness issues would you anticipate?
3. How would you structure the approval process (AI role)?
4. What's your approach to responsible AI governance?

**Model Answer:**
1. **Feature Selection:**
   - **Include:** Income, employment stability, credit score, debt-to-income (directly predictive of default)
   - **Exclude:** Postcode (proxy for race/socioeconomic status), age (protected), gender (protected), marital status (protected)
   - **Rationale:** Use only features that directly indicate credit risk; remove proxies for protected attributes

2. **Fairness Issues:**
   - **Systemic bias:** Historical lending practices denied credit to certain groups; model trained on biased data will perpetuate bias
   - **Feature proxy:** Postcode correlates with race/wealth; excluding it helps but not fully
   - **Disparate impact:** Even without protected attributes, model may approve at different rates by demographic
   - **Mitigation:** Test model accuracy by demographic; audit decisions; retrain quarterly

3. **Approval Process:**
   - **AI role:** Score application; recommend "Approve," "Manual Review," or "Decline"
   - **Human oversight:** Humans review all "Manual Review" cases; any "Decline" can be appealed
   - **Transparency:** Customer receives explanation (which features drove decision)
   - **Appeal:** 10% of applicants appeal decisions; manual review by independent assessor

4. **Responsible AI Governance:**
   - **Fairness baseline:** Model approval rates within ±5% across all demographic groups
   - **Monthly audits:** Check for drift; if fairness metrics exceed threshold, pause and investigate
   - **Model versioning:** Track all model versions; quick rollback if issues found
   - **Audit logs:** Log every decision, score, and reason; 7-year retention for compliance
   - **Incident response:** If unfair pattern detected, halt AI decisions; switch to manual review; investigate root cause

---

## Question 5: Multi-Cloud GenAI Strategy

**Scenario:** Enterprise is deciding between Google Cloud, Azure, and AWS for generative AI workloads. Key requirements:
- Train custom models on proprietary data
- Deploy chatbots for internal knowledge management
- Ensure compliance with GDPR and healthcare standards

**Questions:**
1. Compare Google Cloud, Azure, and AWS for this use case
2. Which would you recommend and why?
3. What are the trade-offs?

**Model Answer:**
1. **Comparison:**

| Factor | Google Cloud | Azure | AWS |
|--------|---|---|---|
| **Foundation Models** | Gemini, PaLM (native) | GPT-4 via partnership (more expensive) | Bedrock (limited selection) |
| **Custom Training** | Vertex AI (excellent) | Azure ML (good) | SageMaker (good) |
| **Chatbot/RAG** | Vertex AI Search (best-in-class) | QnA Maker (older, less capable) | Bedrock + custom (good but more code) |
| **GDPR Compliance** | Excellent (data stays in region) | Excellent | Good |
| **Healthcare** | HIPAA-compliant services | NHS-approved (UK region) | HIPAA-compliant |
| **Cost** | Mid-range | Higher (OpenAI partnership tax) | Lowest (but fewer managed services) |
| **Developer Experience** | Best (Vertex AI Studio, minimal code) | Good (Azure OpenAI, some friction) | Requires more coding (Bedrock APIs) |

2. **Recommendation:**
   - **If UK/NHS:** Azure (NHS-approved region) OR Google (GDPR+ healthcare compliance)
   - **If speed-to-market critical:** Google (Vertex AI Studio, minimal code)
   - **If cost-sensitive:** AWS (cheapest compute, but more dev overhead)
   - **If enterprise locked-in:** Depends on existing cloud vendor

   **For this scenario (GDPR + healthcare + custom models):** **Google Cloud** (Vertex AI is best-of-breed for managed ML + healthcare)

3. **Trade-offs:**
   - Google: Fastest to deploy, best managed services, but potentially higher licensing costs for enterprise
   - Azure: Strong NHS integration, but less intuitive for AI/ML (more Azure ML overhead)
   - AWS: Most cost-efficient, but requires more custom coding

---

## Exam Tips

1. **Read closely:** Scenario-based questions have hidden details (e.g., "GDPR applies" vs "NHS")
2. **Show your reasoning:** Partial credit for methodology, even if numbers are slightly off
3. **Consider responsible AI:** Almost every question includes bias, fairness, or governance angle
4. **Use frameworks:** ROI template, fairness checklist, governance steps make answers clearer
5. **Think like a leader:** Focus on business value, risks, stakeholder management (not just technical details)
