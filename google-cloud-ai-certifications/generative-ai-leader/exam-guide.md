# Google Cloud Generative AI Leader Exam Guide

_Last Updated: November 30, 2025_

## Exam Overview

**Official Name:** Google Cloud Generative AI Leader

**Format:** 90 minutes, multiple choice and multiple-select (50–60 questions)

**Cost:** £74 GBP (approximately £99 USD equivalent)

**Passing Score:** ~70% (exact threshold not published; typically 35/50 questions)

**Delivery:** Online proctored via Kryterion; available globally; book via Google Cloud Skills Boost or Webassessor

**Prerequisites:** None (recommended: familiarity with cloud concepts and GenAI basics)

## Exam Domains and Weights

| Domain | Weight | Key Topics |
|--------|--------|-----------|
| **Generative AI Fundamentals** | 20–25% | LLM concepts, tokens, prompting, RAG, embeddings, fine-tuning, hallucinations |
| **Vertex AI & Google Cloud Services** | 25–30% | Vertex AI Studio, Model Garden, Search & Conversation, Endpoints, Workbench, Pipelines |
| **Business Value & Use Cases** | 20–25% | ROI calculation, risk assessment, industry applications, change management |
| **Responsible AI & Governance** | 15–20% | Bias, fairness, privacy, regulatory compliance (GDPR, NHS, HIPAA), ethical principles |
| **Practical Implementation** | 10–15% | Architecture decisions, cost optimisation, scaling patterns, multi-cloud strategy |

## Skills Assessed

**Knowledge:**
- Define LLM concepts (tokens, context window, attention, hallucinations)
- Describe Vertex AI services and use cases
- Calculate ROI for GenAI projects
- Identify bias and fairness issues
- Explain responsible AI principles

**Application:**
- Recommend appropriate service for scenarios (Studio vs Search vs AutoML)
- Structure responsible AI governance processes
- Design cost-effective architectures
- Identify regulatory compliance requirements

**Analysis:**
- Compare cloud providers for GenAI workloads
- Assess trade-offs (cost vs quality, speed vs latency)
- Evaluate responsible AI risks and mitigations
- Map business requirements to technical solutions

## Study Path (4–6 weeks)

### Week 1: Fundamentals
- **Read:** `genai-fundamentals.md` (LLMs, tokens, prompting, embeddings, RAG, fine-tuning, safety)
- **Resource:** Google Cloud Generative AI learning path (free)
- **Practice:** Define key concepts; summarise each section in 1 sentence

### Week 2: Vertex AI & Services
- **Read:** `vertex-ai-overview.md` (all Vertex AI services, use cases, cost)
- **Hands-on:** Explore Vertex AI Studio via Google Cloud Skills Boost
- **Practice:** Create a comparison table: service vs use case vs cost

### Week 3: Business & ROI
- **Read:** `business-use-cases.md` (chatbots, email marketing, healthcare, finance)
- **Practice:** Calculate ROI for each use case (template provided)
- **Identify:** For each scenario, what could go wrong? How mitigate?

### Week 4: Responsible AI & Compliance
- **Read:** `responsible-ai.md` (Google AI Principles, bias, fairness, privacy, compliance)
- **Read:** UK-specific guides (GDPR, NHS Data Security and Protection Toolkit, healthcare regulations)
- **Practice:** Design a governance process for a healthcare AI scenario

### Week 5: Practical Scenarios
- **Read:** `practice-questions.md` (5 detailed scenario-based questions with model answers)
- **Practice:** Attempt questions; compare your reasoning to model answers
- **Identify:** Weak areas; re-read relevant sections

### Week 6: Final Review
- **Quiz:** Full practice exam simulation (90 min, ~50 questions)
- **Review:** Any topics scoring <70%
- **Ready?** Schedule exam when confident

## Key Topics Deep Dive

### Generative AI Fundamentals

**Tokens & Context:**
- 1 token ≈ 4 characters; "hello world" = ~2 tokens
- Context window: max tokens model can process
  - Gemini 1.5: 1M tokens (process entire book)
  - GPT-4: 128k tokens
  - Larger context = can handle more documents/history

**Prompting Techniques:**
- **Zero-shot:** Prompt with no examples ("Summarise: [text]")
- **Few-shot:** Prompt with examples ("Example 1: [input] → [output]. Example 2: ..., Now summarise: [text]")
- **Chain-of-thought:** Ask model to explain reasoning ("Step 1: Identify customer segment. Step 2: ...")

**Embeddings:**
- Convert text to vector (list of numbers)
- Similar text = similar vectors
- Use case: Semantic search, clustering, recommendation

**RAG (Retrieval-Augmented Generation):**
- Problem: LLM hallucinates without grounding
- Solution: Retrieve relevant documents first; ask LLM to answer based on documents
- Result: Lower hallucination rate; answers traceable to source

**Fine-Tuning:**
- Adapt pre-trained model to specific domain
- Train on small dataset (100–1000 examples) of your data
- Result: Better quality for niche use case; but slower inference
- Trade-off: Fine-tuning vs in-context learning (few-shot examples)

**Safety & Guardrails:**
- Content filtering: Block toxic topics
- Safety classifiers: Rate toxicity of output
- Mitigation: Safety instructions in prompt ("You are a helpful assistant that refuses harmful requests")

### Vertex AI Services

**Vertex AI Studio (No-Code GenAI)**
- **Use:** Prompt engineering, model exploration, basic tuning
- **Best for:** Business users, quick prototyping
- **Cost:** Free (limited) → £0.001–0.01 per prompt

**Model Garden**
- **Use:** Access 100+ pre-trained models (Google, open-source, partner)
- **Best for:** Finding right model for task; quick evaluation
- **Cost:** Free access; pay only for compute if you deploy

**Vertex AI Search & Conversation (RAG)**
- **Use:** Q&A over documents (PDFs, web pages, databases)
- **Best for:** Customer support, internal knowledge
- **Cost:** ~£0.05–0.10 per query

**Vertex AI Endpoints (Online Serving)**
- **Use:** Real-time REST API for predictions
- **Best for:** Live chatbots, APIs, mobile apps
- **Cost:** ~£0.05–0.60/hour depending on machine type

**Vertex AI Pipelines (Orchestration)**
- **Use:** Automate ML workflows (data → train → evaluate → deploy)
- **Best for:** Production ML; automated retraining
- **Cost:** Free; pay for underlying compute

### Business Value & ROI

**ROI Formula:**
```
ROI = (Benefits − Costs) / Costs × 100%
Payback Period = Total Investment / Annual Benefits
```

**Examples:**

**1. Support Chatbot:**
- Current: £1.5M/year support costs
- Implementation: £150k (setup + Year 1)
- Benefit: 30% headcount reduction = £450k/year
- ROI: (£450k − £150k) / £150k = 200%
- Payback: £150k / £450k = 4 months

**2. Personalized Email:**
- Current: £10M email revenue; 2% conversion
- Implementation: £100k
- Benefit: Lift conversion to 2.5% = +£500k revenue/year
- ROI: (£500k − £100k) / £100k = 400%
- Payback: 2.4 months

### Responsible AI & Compliance

**Bias & Fairness:**
- **Bias:** Systematic error across demographics (e.g., model approves loans differently for men vs women)
- **Fairness metrics:**
  - Demographic parity: Equal approval rate across groups
  - Equalized odds: Equal true positive rate across groups
  - Calibration: Predicted probabilities match reality

**Privacy:**
- **Differential privacy:** Add noise to prevent memorisation
- **Federated learning:** Train on devices; no data centralisation
- **Data minimisation:** Collect only necessary data

**Compliance:**
- **GDPR (EU):** Right to explanation, erasure, consent
- **NHS (UK):** Fairness audits, explainability, human oversight
- **HIPAA (US):** Encryption, audit logs, Business Associate Agreement

### Practical Implementation

**Trade-offs:**

| Scenario | Recommendation | Why |
|----------|---|---|
| **Batch vs Online** | Batch for monthly payroll, online for real-time fraud | Batch cheaper; online faster |
| **Larger vs Smaller Model** | Smaller + RAG usually wins | Smaller cheaper; RAG improves quality |
| **Fine-tune vs Few-shot** | Few-shot for quick POC; fine-tune for production | Few-shot fast; fine-tune higher quality |
| **Google vs Azure vs AWS** | Google for speed, Azure for NHS, AWS for cost | Different strengths per cloud |

**Cost Optimisation:**
- Use batch prediction for non-urgent work
- Start with pre-trained model; fine-tune only if needed
- Monitor spending; alert if unexpected spike
- Schedule training off-peak (weekends) if possible

## Exam Question Patterns

### Pattern 1: "Choose the Right Service"
**Example:** "Healthcare provider wants to reduce clinician documentation time. Which service?"

**Answer Strategy:**
- Identify need: Transcribe + summarise clinical notes
- Match service: Vertex AI + custom training (healthcare compliance required)
- Why: Pre-built services don't meet healthcare compliance; need custom model

### Pattern 2: "Calculate ROI"
**Example:** "Setup £50k, annual cost £10k, saves £40k/year. Payback?"

**Answer Strategy:**
- Payback = (£50k + £10k) / £40k = 1.5 years

### Pattern 3: "Identify Bias Risk"
**Example:** "Loan approval model. What fairness issue?"

**Answer Strategy:**
- Training data: Historical lending decisions (biased)
- Result: Model perpetuates historical bias
- Mitigation: Test accuracy by demographic; retrain on balanced data; exclude proxy features

### Pattern 4: "Compare Cloud Providers"
**Example:** "Enterprise needs GenAI for healthcare + speed-to-market. Which?"

**Answer Strategy:**
- Google: Vertex AI best-in-class, healthcare compliance possible
- Azure: NHS-approved region (if UK)
- AWS: Cheapest, but slower time-to-market
- **For this scenario:** Google (speed + healthcare support)

## Common Misconceptions to Avoid

- ❌ **"Bigger models are always better"** → ✅ Smaller + RAG often better value
- ❌ **"GenAI = Science fiction"** → ✅ Production-ready now; used by leading companies
- ❌ **"AI replaces humans"** → ✅ Augment humans; they stay in control
- ❌ **"Fairness = remove protected attributes"** → ✅ Must test outcome fairness; need demographic data to audit
- ❌ **"GCP is only for Google users"** → ✅ Competitive advantage for any company (like AWS/Azure)

## Exam Day Tips

1. **Read each question carefully:** Hidden requirements (e.g., "GDPR compliance", "NHS") change answer
2. **Eliminate obviously wrong answers first** (narrows to 2–3 choices)
3. **If unsure, lean toward responsible AI** (many questions have governance angle)
4. **Do rough calculations on paper** (show working if allowed)
5. **Time management:** ~1.8 min per question; don't get stuck on one
6. **Review:** If finish early, review flagged questions (but don't second-guess correct answers)

## Resources

**Official:**
- [Google Cloud Certification Page](https://cloud.google.com/certification/cloud-certified-generative-ai-leader)
- Google Cloud Skills Boost (free limited; £40/month unlimited)
- Vertex AI documentation

**This Repository:**
- All study guides, practice questions, business use cases
- Model answers and exam tips

**External:**
- Google Cloud Responsible AI documentation
- UK-specific compliance guides (GDPR, NHS)

## After Passing

**Next certifications to consider:**
- Professional ML Engineer (technical depth)
- Associate Cloud Engineer (platform breadth)
- Cloud Architect (enterprise design)

**Skills to build:**
- Hands-on projects with Vertex AI
- Explore healthcare/regulated industry applications
- Specialise in responsible AI governance
- Get experience deploying GenAI in production

---

**Last Updated:** November 30, 2025  
**Exam Information:** Accurate as of Nov 2025; verify at Google Cloud Certification Page before booking
