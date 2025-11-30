# Vertex AI Overview for Leaders

_Last Updated: November 30, 2025_

Vertex AI is Google Cloud's unified platform for machine learning. It consolidates services previously scattered across Google Cloud (AutoML, Vertex AI, AI Platform) into one integrated experience.

## Core Services for Leaders

### Vertex AI Studio (Generative AI)

**What it is:** No-code environment for working with LLMs, multimodal models, and embeddings.

**Key capabilities:**
- **Prompt Engineering:** Test variations instantly; iterate to improve results
- **Model Selection:** Access Gemini, PaLM 2, and other Google models
- **Custom Tuning:** Fine-tune on proprietary data without coding
- **Conversational Agents:** Build chatbots with knowledge bases, API integrations, web search

**Business value:**
- **Speed:** Launch AI applications in days, not months
- **Cost-Efficiency:** Pre-trained models = no training infrastructure
- **Adaptability:** Fine-tune on company data for domain-specific knowledge
- **Governance:** All data stays in your GCP project; no sharing with Google

**ROI example:** Bank reduces customer support costs by 40% using Vertex AI Studio chatbot (no development team needed).

### Vertex AI Search and Conversation

**What it is:** Pre-built solution for semantic search and question-answering over custom company data.

**How it differs from traditional search:**
- **Traditional:** Exact keyword match (e.g., searching "vacation policies" misses "time off")
- **Vertex AI Search:** Semantic understanding (understands intent; finds documents even with different wording)

**Setup (no code required):**
1. Upload documents (PDFs, web pages, internal databases)
2. Vertex AI indexes and creates embeddings
3. Employees/customers ask questions via chat
4. System retrieves relevant docs and synthesises answers

**Business applications:**
- **Internal Knowledge:** Employees search company policies, procedures, training docs
- **Customer Support:** Self-service Q&A reduces support tickets
- **Sales Enablement:** Salespeople quickly find product specs, case studies, pricing
- **Compliance:** Regulatory teams search policies and audit trails

**Cost-Benefit:**
- Setup: ~£1000–5000 (one-time infrastructure)
- Per query: ~£0.05–0.10 (much cheaper than human support)
- ROI: Company reduces support tickets 30–50%

### Model Garden

**What it is:** Marketplace of pre-trained foundation models, with easy deployment.

**Models available:**
- **Gemini Family:** Text, multimodal (image + text), vision-only
- **Open-source:** Llama 2, Mistral, and others (hosted on GCP)
- **Specialized:** Code generation, medical imaging, document intelligence
- **Third-party:** Partner models (e.g., Anthropic, Aleph Alpha)

**Use cases:**
- **Image Analysis:** Detect objects, read text, assess quality
- **Document Processing:** Extract information from PDFs, contracts, invoices
- **Code Generation:** Auto-complete, bug detection, documentation
- **Industry-Specific:** Medical diagnosis support, legal document review

### Vertex AI Workbench

**What it is:** Managed Jupyter notebooks for collaborative data exploration and ML prototyping.

**For business leaders (high-level):**
- Data scientists iterate rapidly without managing infrastructure
- Reduces development time from months to weeks
- Cost-effective: pay only for compute hours used

### Vertex AI Pipelines

**What it is:** Automated workflows for training and retraining models.

**For business leaders (high-level):**
- **Reproducibility:** Same results every time
- **Automation:** Retrain weekly/daily without manual intervention
- **Governance:** Audit trail of what data/code produced each model
- **Reliability:** Automatically retry on failure; alert on issues

**Business benefit:** Models stay accurate as data evolves; no human oversight required.

## Architecture: Typical Enterprise AI System

```
Data Sources (BigQuery, Cloud Storage, APIs)
         ↓
[Vertex AI Pipelines]
    ├── Data Ingestion (load daily transactions)
    ├── Preprocessing (clean, normalise)
    ├── Feature Engineering (derive new variables)
    ├── Training (build model)
    ├── Evaluation (check accuracy, fairness)
    └── Conditional Deploy (push to endpoint if accuracy > threshold)
         ↓
[Vertex AI Endpoints]
    ├── Real-Time API (e.g., fraud detection on every transaction)
    ├── Auto-Scaling (handles traffic spikes)
    └── Monitoring (alerts on accuracy drop)
         ↓
Applications (Mobile App, Web Service, CRM)
```

## Cost Considerations

### Development Phase

| Service | Cost/Month (GBP) | Use Case |
|---------|---|----------|
| Vertex AI Studio | Free (limited) / £50+ | Prompt engineering, testing models |
| Model Garden | Free access / £10+ deployment | Trying pre-trained models |
| Workbench (CPU) | £20–50 | Data exploration |
| Workbench (GPU) | £200–500 | Complex model prototyping |

### Production Phase

| Service | Cost/Month (GBP) | Scaling Notes |
|---------|---|----------|
| Endpoints (1 CPU) | £50–100 | Baseline for low-traffic APIs |
| Endpoints (4 CPU + GPU) | £200–400 | Production-grade serving |
| Pipelines | £0 (pay for compute) | Schedule training; costs depend on frequency |
| Search & Conversation | £0.05–0.10 per query | Scales efficiently; per-query pricing |

**Tip:** Use batch prediction (cheaper) for non-urgent workloads; online endpoints (pricier) for real-time requirements.

## Governance and Responsible AI

### Data Privacy

- All data processed within your GCP project
- No data sent to Google for training other models (unless opted-in)
- Encryption in transit and at rest
- Compliance with GDPR, HIPAA, NHS standards

### Bias and Fairness

Vertex AI includes tools to:
- Detect fairness issues (model performs differently across demographics)
- Log feature importance (which inputs drove a prediction)
- Audit model decisions (for compliance, explainability)

### Model Governance

- **Versioning:** Track which model version is in production
- **Approval Workflows:** Require sign-off before deployment
- **Incident Response:** Quickly rollback if model misbehaves
- **Audit Logs:** Record who accessed/modified models, when

## Key Business Questions

**Q: Should we build custom models or use pre-trained?**

A: Use pre-trained (Vertex AI Studio, Model Garden) for speed/cost; build custom only if domain-specific accuracy is critical (e.g., proprietary fraud patterns).

**Q: How long to deploy an AI application?**

A: Using Vertex AI Studio: 2–4 weeks. Custom training: 2–6 months.

**Q: What are typical ROI timelines?**

A: Cost savings (efficiency gains): 3–6 months. Revenue generation (new services): 6–12 months.

**Q: Is GenAI production-ready?**

A: Yes, with guardrails:
- Use for augmentation (assist humans) not automation (replace humans) initially
- Monitor accuracy closely
- Plan for failure (have human fallback)

## Exam Focus

**GenAI Leader will test:**
- [ ] Use cases for Vertex AI Studio vs Search vs AutoML
- [ ] Cost estimation for different workloads
- [ ] Responsible AI principles (fairness, privacy, governance)
- [ ] ROI calculation for AI projects
- [ ] Architecture trade-offs (batch vs online, cost vs latency)
- [ ] When to build custom vs use pre-trained models

## Cross-References

- See `genai-fundamentals.md` for LLM concepts
- See `business-use-cases.md` for real-world applications
- See `responsible-ai.md` for governance and compliance
