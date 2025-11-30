# Security Best Practices – ACE

_Last Updated: November 30, 2025_

## Overview

Secure GCP projects: identity, network, data, audit. Security questions scattered across ACE exam (5–8%).

---

## Core Principles

1. **Least Privilege:** Grant minimum necessary permissions
2. **Defence in Depth:** Multiple layers (network, IAM, encryption, audit)
3. **Encryption:** Data at rest & in transit
4. **Audit:** Log all access (Cloud Audit Logs)

---

## Security Best Practices

### IAM Security
- Use service accounts (not personal accounts) for apps
- Enable Cloud Audit Logs (track who did what)
- Review IAM policy quarterly (remove unused roles)
- Avoid basic roles (Editor, Owner, Viewer)

```bash
# Enable Cloud Audit Logs
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member serviceAccount:logging-service@cloudfunctions.gserviceaccount.com \
  --role roles/logging.logWriter

# Review IAM policy
gcloud projects get-iam-policy PROJECT-ID
```

### Network Security
- **VPC:** Isolate resources (not on public internet)
- **Firewall rules:** Default deny, explicit allow
- **Cloud Armor:** DDoS + WAF protection
- **VPN:** Private tunnel to on-prem

```bash
# Create VPC
gcloud compute networks create my-vpc --subnet-mode custom

# Create firewall rule (allow SSH from office only)
gcloud compute firewall-rules create allow-ssh \
  --network my-vpc \
  --allow tcp:22 \
  --source-ranges 203.0.113.0/24

# Deny all by default, allow what's needed
gcloud compute firewall-rules create deny-all \
  --network my-vpc \
  --deny all \
  --priority 65534
```

### Data Security
- **Encryption at rest:** Default enabled (Google-managed keys)
- **Encryption in transit:** TLS for all APIs
- **Key management:** Cloud KMS for customer-managed keys

```bash
# Create Cloud KMS key
gcloud kms keyrings create my-ring --location global
gcloud kms keys create my-key --location global --keyring my-ring \
  --purpose encryption

# Encrypt data with key
gcloud kms encrypt --plaintext-file data.txt \
  --ciphertext-file data.txt.enc \
  --location global --keyring my-ring --key my-key
```

### API Security
- Disable unnecessary APIs (reduce attack surface)
- Use OAuth2 + API keys (not passwords)
- Enable API quotas (prevent abuse)

```bash
# List enabled APIs
gcloud services list --enabled

# Disable unused API
gcloud services disable compute.googleapis.com
```

---

## VPC Fundamentals

### Components
- **VPC:** Virtual network (isolated from internet)
- **Subnet:** IP address range within VPC
- **Firewall:** Rules to allow/deny traffic
- **Cloud Router:** Connect to on-prem networks
- **Cloud VPN:** Encrypted tunnel to on-prem

### Architecture
```
On-Premises
    ↓
[Cloud VPN Tunnel] (encrypted)
    ↓
[Cloud Router] (routing)
    ↓
[VPC] (my-vpc)
  ├─ Subnet 1 (10.0.1.0/24, us-central1)
  ├─ Subnet 2 (10.0.2.0/24, europe-west1)
  └─ Firewall rules (allow SSH, deny by default)
    ↓
[GCE Instance] (runs in subnet)
```

---

## Common ACE Exam Questions

**Q1:** Instance is accessible from the internet (security risk). Fix?
- A) Add firewall rule: deny all
- B) Create VPC (isolate from internet)
- C) Both A + B
- D) Change machine type

**Answer:** C. VPC isolates network; firewall enforces rules. Both needed.

**Q2:** Audit: which users accessed my Cloud Storage bucket yesterday?
- A) Cloud Storage logs (built-in)
- B) Cloud Audit Logs (access logs)
- C) Cloud Monitoring (metrics only)
- D) None (no audit available)

**Answer:** B. Cloud Audit Logs tracks access; Cloud Storage logs don't exist (must use Audit Logs).

**Q3:** Service account needs to encrypt data with customer-managed key (compliance). Setup?
- A) Google-managed encryption (default)
- B) Create Cloud KMS key; grant service account permission
- C) Use Cloud Storage encryption (insufficient)
- D) Disable encryption (not needed)

**Answer:** B. Cloud KMS + IAM grant = customer-managed encryption (auditable, compliant).

---

## Links

- [Cloud IAM Best Practices](https://cloud.google.com/iam/docs/best-practices)
- [VPC Documentation](https://cloud.google.com/vpc/docs)
- [Cloud KMS Documentation](https://cloud.google.com/kms/docs)