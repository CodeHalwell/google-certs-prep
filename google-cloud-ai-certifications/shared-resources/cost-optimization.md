# Cost Optimisation on Google Cloud

_Last Updated: November 30, 2025_

All figures below are **illustrative** and should be validated in the Google Cloud Pricing Calculator with current GBP rates.

## Core Strategies

- [ ] Choose appropriate machine types and use committed use discounts where viable.
- [ ] Prefer Cloud Run or GKE Autopilot for bursty workloads.
- [ ] Use preemptible/Spot VMs for non‑critical batch jobs.
- [ ] Configure lifecycle policies for Cloud Storage and delete unused buckets.
- [ ] Turn off idle endpoints and notebooks in Vertex AI.

## Example Monthly Budgets (GBP)

### ACE Lab Environment (Foundation)

- 1 x small Compute Engine instance for admin tasks: ~£15–£25/month
- Light use of Cloud Storage (tens of GB): ~£1–£5/month
- Monitoring and logging within free tier for low‑traffic workloads

**Target:** Keep foundational practice under **£40–£50/month**.

### PMLE Practice Environment (Vertex AI + GPUs)

- Occasional use of an NVIDIA T4‑class GPU for training: ~£0.35–£0.60/hour
- Vertex AI custom jobs and AutoML training: a few tens of pounds per run, depending on duration
- Cloud Storage and BigQuery for datasets: ~£5–£20/month for moderate usage

**Target:** Budget **£100–£200/month** during intensive PMLE preparation, scaling down when idle.

### GenAI Prototyping with Vertex AI

- Prompt‑based use of Vertex AI models (pay‑per‑token): small prototypes often stay under **£20–£40/month**.
- RAG prototypes may add storage and vector index costs; budget an extra **£20–£50/month**.

**Target:** Keep early GenAI prototypes in the **£50–£100/month** range until ready to scale.

