# Load Balancing – ACE

_Last Updated: November 30, 2025_

## Overview

Distribute traffic across multiple instances (high availability + horizontal scaling).

---

## Load Balancer Types

| Type | Layer | Protocol | Use Case | Cost |
|------|-------|----------|----------|------|
| Network LB | L4 (TCP/UDP) | TCP, UDP | Games, video | ~£0.10/hour |
| HTTP(S) LB | L7 (Application) | HTTP, HTTPS | Web apps, API | ~£0.10/hour |
| Internal LB | L4 | TCP, UDP | Private services | Free* |

*Traffic charges apply.

---

## HTTP(S) Load Balancer (Recommended for ACE)

```bash
# 1. Create backend service
gcloud compute backend-services create my-backend \
  --protocol HTTP \
  --port-name http \
  --global

# 2. Add instance group
gcloud compute instance-groups managed create my-mig \
  --base-instance-name web \
  --template my-template \
  --size 3 \
  --zone us-central1-a

gcloud compute backend-services add-backends my-backend \
  --instance-group my-mig \
  --instance-group-zone us-central1-a

# 3. Create health check
gcloud compute health-checks create http my-health-check \
  --port 80 \
  --request-path /

# 4. Create URL map (routing rules)
gcloud compute url-maps create my-lb \
  --default-service my-backend

# 5. Create HTTPS certificate
gcloud compute ssl-certificates create my-cert \
  --certificate cert.pem \
  --private-key key.pem

# 6. Create target HTTPS proxy
gcloud compute target-https-proxies create my-proxy \
  --url-map my-lb \
  --ssl-certificates my-cert

# 7. Create forwarding rule (public IP)
gcloud compute forwarding-rules create my-forwarding-rule \
  --global \
  --target-https-proxy my-proxy \
  --address my-lb-ip \
  --ports 443
```

---

## Health Checks

Monitor instance health; replace unhealthy ones.

```bash
# Create HTTP health check
gcloud compute health-checks create http my-check \
  --port 80 \
  --request-path /health \
  --check-interval 30s \
  --timeout 10s \
  --unhealthy-threshold 3 \
  --healthy-threshold 2

# Attach to backend
gcloud compute backend-services update my-backend \
  --health-checks my-check
```

---

## Session Affinity (Sticky Sessions)

Route requests from same client to same instance.

```bash
# Enable session affinity
gcloud compute backend-services update my-backend \
  --session-affinity CLIENT_IP \
  --affinity-cookie-ttl 60
```

---

## Common ACE Questions

**Q1:** Web app needs high availability. Setup?
- A) Single instance (simple)
- B) Multiple instances + HTTP LB + MIG + health checks
- C) Both (B recommended)
- D) Manually manage instances

**Answer:** B. LB distributes traffic; MIG auto-scales; health checks replace failed instances.

**Q2:** Instance unhealthy (not responding). LB behavior?
- A) Keep routing traffic (customer sees error)
- B) Stop routing traffic to that instance (use healthy ones)
- C) Alert operator
- D) Destroy and recreate instance

**Answer:** B. Health checks detect unhealthy instance → LB routes around it → MIG triggers replacement.

**Q3:** SSL certificate expires tomorrow. Deployment impact?
- A) No impact (LB uses new cert automatically)
- B) HTTPS requests fail
- C) Need to recreate LB (downtime)
- D) Update cert before expiry (no downtime)

**Answer:** D. Pre-update cert; LB uses new cert transparently (zero downtime if done before expiry).

---

## Links

- [Load Balancing Documentation](https://cloud.google.com/load-balancing/docs)
- [HTTP(S) LB Setup Guide](https://cloud.google.com/load-balancing/docs/https)