# Service Accounts – ACE

_Last Updated: November 30, 2025_

## Overview

Service Accounts = programmatic identities. VMs, Cloud Functions, CI/CD use service accounts (not personal Google accounts).

---

## Key Concepts

### Service Account vs User Account
| Aspect | User | Service Account |
|--------|------|-----------------|
| Credentials | Password + 2FA | Key file (JSON) |
| Use case | Human interaction | Applications, automation |
| TTL | Indefinite | Can expire tokens |
| Audit | Identifies person | Identifies app/service |

### Structure
```
Service Account: my-app-sa@PROJECT-ID.iam.gserviceaccount.com
├─ Email-like identifier
├─ Unique ID (123456789)
└─ Keys (for authentication)
```

---

## Creating & Managing

```bash
# Create service account
gcloud iam service-accounts create my-app-sa \
  --display-name "My Application"

# List service accounts
gcloud iam service-accounts list

# Grant role to service account
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member serviceAccount:my-app-sa@PROJECT-ID.iam.gserviceaccount.com \
  --role roles/storage.admin

# Create key (for external use)
gcloud iam service-accounts keys create key.json \
  --iam-account my-app-sa@PROJECT-ID.iam.gserviceaccount.com

# View keys
gcloud iam service-accounts keys list \
  --iam-account my-app-sa@PROJECT-ID.iam.gserviceaccount.com

# Delete key (security: rotate regularly)
gcloud iam service-accounts keys delete KEY-ID \
  --iam-account my-app-sa@PROJECT-ID.iam.gserviceaccount.com

# Assign service account to VM
gcloud compute instances create my-vm \
  --service-account my-app-sa@PROJECT-ID.iam.gserviceaccount.com
```

---

## Default Service Accounts

GCP creates default service accounts per project:
- **Compute Engine default:** `PROJECT-ID-compute@developer.gserviceaccount.com` (all GCE permissions by default - risky)
- **App Engine default:** `PROJECT-ID@appspot.gserviceaccount.com`
- **Cloud Functions default:** `PROJECT-ID@cloudfunctions.gserviceaccount.com`

**Security Tip:** Disable default service accounts; create least-privilege custom accounts.

```bash
# Disable Compute Engine default
gcloud iam service-accounts disable PROJECT-ID-compute@developer.gserviceaccount.com
```

---

## Key Rotation

```bash
# 1. Create new key
gcloud iam service-accounts keys create new-key.json \
  --iam-account my-app-sa@PROJECT-ID.iam.gserviceaccount.com

# 2. Update app to use new-key.json

# 3. Delete old key (after app switched)
gcloud iam service-accounts keys delete OLD-KEY-ID \
  --iam-account my-app-sa@PROJECT-ID.iam.gserviceaccount.com
```

---

## Common ACE Exam Questions

**Q1:** GCE instance needs to read Cloud Storage (for backups). Setup?
- A) Create personal Google account key (security risk)
- B) Use default Compute Engine service account (high permissions)
- C) Create custom service account + grant storage.admin role
- D) No auth needed (open access)

**Answer:** C. Least privilege: custom SA, specific role (storage.objectViewer, not admin).

**Q2:** Application runs on GCE instance. How to authenticate to BigQuery?
- A) Hardcode credentials in code (risky)
- B) Use service account (assigned to VM)
- C) Use personal API key
- D) No authentication (public dataset only)

**Answer:** B. VM automatically authenticates via service account (no key in code).

**Q3:** Rotate credentials for service account running production app. Process?
- A) Create new key, delete old key immediately (downtime)
- B) Create new key, test app, delete old key (safe)
- C) Single key per service account (no rotation)
- D) Use passwords (human accounts only)

**Answer:** B. Create new key → deploy to app → verify → delete old key (zero downtime).

---

## Best Practices

- Create custom service accounts (not default)
- Grant least-privilege roles (not Owner/Editor)
- Rotate keys regularly (e.g., quarterly)
- Use Cloud Audit Logs (monitor SA usage)
- Never share key files (one key per app)

---

## Links

- [Service Accounts Documentation](https://cloud.google.com/iam/docs/service-accounts)
- [Service Account Keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)