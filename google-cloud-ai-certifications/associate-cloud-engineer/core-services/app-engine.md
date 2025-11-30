# App Engine – Associate Cloud Engineer

_Last Updated: November 30, 2025_

## Overview

App Engine provides fully managed platform-as-a-service (PaaS) for web applications. No server management; automatic scaling. 5–8% of ACE exam.

---

## Standard vs Flexible

| Feature | Standard | Flexible |
|---------|----------|----------|
| Runtime | Python, Node.js, Java, Go, PHP, Ruby | Any (Dockerfile) |
| Scaling | Auto (cold start ~1–5s) | Auto (but slower) |
| Max latency | 60s timeout | 24h timeout |
| Minimum instances | 0 (can sleep) | 1+ (baseline cost) |
| Cost | £0.05/hour instance (but scales to 0) | £0.026/hour (always running) |
| Use case | Simple web apps | Complex, custom apps |

---

## Standard (Recommended for ACE)

### Deployment
```bash
# Initialize project
gcloud app create --region=us-central

# Create app.yaml
cat > app.yaml << 'EOF'
runtime: python39

env: standard

handlers:
- url: /.*
  script: auto
EOF

# Create main.py
cat > main.py << 'EOF'
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
EOF

# Deploy
gcloud app deploy

# View application
gcloud app open  # Opens in browser

# View logs
gcloud app logs read -n 50
```

### Scaling
```yaml
# app.yaml with scaling
runtime: python39
auto_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.70
```

### Versions & Traffic Split
```bash
# Deploy new version (v2)
gcloud app deploy --version=v2

# Route 10% traffic to v2 for testing
gcloud app services set-traffic default --splits v1=0.9,v2=0.1

# Monitor metrics
gcloud app describe

# Full migration to v2
gcloud app services set-traffic default --splits v2=1.0

# Rollback to v1
gcloud app services set-traffic default --splits v1=1.0
```

---

## Flexible (Custom Runtimes)

Use Flexible when Standard doesn't support your runtime (e.g., C++, Rust) or needs custom libraries.

```yaml
# app.yaml (Flexible)
runtime: custom
env: flex

env_variables:
  BUCKET_NAME: "my-bucket"

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.70
```

### Dockerfile
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT main:app
```

---

## Common ACE Exam Questions

**Q1:** Startup time critical for app. Standard vs Flexible?
- A) Standard (fast cold start, ~1–5s)
- B) Flexible (slower cold start, ~30s+)
- C) Doesn't matter (same performance)
- D) Depends on runtime

**Answer:** A. Standard designed for quick scaling; Flexible slower.

**Q2:** Deploy Python app with custom C++ library. Runtime choice?
- A) Standard Python (simplest)
- B) Flexible (custom Dockerfile)
- C) Compute Engine (full control)
- D) GKE (overkill)

**Answer:** B. Standard doesn't support C++; need Flexible (Dockerfile) or Compute Engine.

**Q3:** Production app needs 2x peak capacity during sales. Scaling strategy?
- A) Manual scaling (adjust replicas)
- B) Auto scaling (target CPU 70%)
- C) Pre-warming (keep instances ready)
- D) B or C (auto + pre-warm)

**Answer:** D. Auto-scaling handles typical load; pre-warming (min_instances) ensures no cold-start delays during peak.

---

## Cost Optimisation

- Standard: Set min_instances to 0 (sleep during off-hours, £0 cost)
- Flexible: Minimum £0.026/hour (always running); use for critical services only
- Traffic split: Test new versions (v2) with 1% traffic before full migration

**Monthly Cost Example:**
- Standard (0–10 instances, 1M requests/month): £2–10
- Flexible (2 instances, always running): £38/month

---

## App Engine Best Practices

| Practice | Benefit |
|----------|---------|
| Use Standard for typical web apps | Simplicity + cost savings |
| Version & traffic split for testing | Safe deployments (1% canary) |
| Logs & monitoring integration | Built-in observability |
| Environment variables | Config without redeployment |
| Auto-scaling tuning | Optimal cost/performance |

---

## Links

- [App Engine Documentation](https://cloud.google.com/appengine/docs)
- [App Engine Quotas](https://cloud.google.com/appengine/quotas)
- [Deployment Best Practices](https://cloud.google.com/appengine/docs/standard/python3/how-instances-are-managed)