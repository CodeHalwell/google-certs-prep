# Identity & Access Management (IAM) – ACE

_Last Updated: November 30, 2025_

## Overview

IAM controls who (identity) can do what (action) on which resources. Core security concept (8–12% of ACE exam).

---

## Key Concepts

### IAM Model
**Identity → Role → Resources**
- **Identity:** Google Account, Service Account, Google Group, Workspace Domain
- **Role:** Collection of permissions (e.g., roles/viewer = read-only)
- **Resource:** GCP service (GCE instance, BigQuery dataset, Cloud Storage bucket)

### Roles

| Role Type | Use | Example |
|-----------|-----|---------|
| Predefined (Google-managed) | Most common | roles/viewer, roles/editor, roles/owner |
| Custom | Org-specific | roles/custom-ml-engineer |
| Basic | Legacy (avoid) | Editor, Viewer, Owner |

### Permission Hierarchy

```
Predefined Role (e.g., roles/viewer)
├─ compute.instances.list
├─ storage.buckets.list
└─ resourcemanager.projects.get
```

---

## Service Accounts

Programmatic identities (not human users). Used by VMs, Cloud Functions, CI/CD pipelines.

```bash
# Create service account
gcloud iam service-accounts create my-app-sa \
  --display-name "My App Service Account"

# Grant role
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member serviceAccount:my-app-sa@PROJECT-ID.iam.gserviceaccount.com \
  --role roles/viewer

# Create key (for external apps)
gcloud iam service-accounts keys create key.json \
  --iam-account my-app-sa@PROJECT-ID.iam.gserviceaccount.com

# Verify permissions
gcloud projects get-iam-policy PROJECT-ID \
  --flatten='bindings[].members' \
  --filter='bindings.members:serviceAccount:*'
```

---

## Granting Permissions

```bash
# Grant individual role
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member user:alice@example.com \
  --role roles/compute.admin

# Grant multiple roles
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member user:bob@example.com \
  --role roles/storage.admin

# Revoke role
gcloud projects remove-iam-policy-binding PROJECT-ID \
  --member user:alice@example.com \
  --role roles/compute.admin
```

---

## Common Roles (ACE Exam Focus)

| Role | Permissions |
|------|-------------|
| roles/viewer | Read-only all resources |
| roles/editor | Full control (avoid in prod) |
| roles/owner | Admin + billing |
| roles/compute.admin | Full GCE control |
| roles/storage.admin | Full Cloud Storage control |
| roles/bigquery.admin | Full BigQuery control |
| roles/iam.securityAdmin | Grant/revoke roles |
| roles/resourcemanager.projectCreator | Create projects |

---

## Common ACE Exam Questions

**Q1:** App needs to read from Cloud Storage, but no compute.admin. Correct role?
- A) roles/viewer (too permissive)
- B) roles/storage.objectViewer (read-only objects) ✅
- C) roles/owner (too much)
- D) roles/editor (overkill)

**Answer:** B. Least privilege: grant only what's needed (read objects, not all GCP).

**Q2:** Service account crashes. Need to audit which permission was missing. Where?
- A) IAM policy (shows granted roles)
- B) Cloud Audit Logs (shows access attempts)
- C) Cloud Monitoring (shows errors)
- D) All of above

**Answer:** D. IAM shows what roles granted; Audit Logs show denied requests; Monitoring shows error patterns.

**Q3:** Team member needs to grant Cloud Storage access to colleagues. Minimum role?
- A) roles/iam.securityAdmin (full IAM control)
- B) roles/storage.admin (full storage control)
- C) roles/iam.securityAdmin + roles/storage.admin (overkill)
- D) Custom role (fine-grained)

**Answer:** A (minimum to grant roles). Custom better (least privilege), but A sufficient.

---

## Best Practices

- **Least privilege:** Grant minimum necessary roles
- **Service accounts:** Use instead of user credentials in apps
- **Audit logs:** Monitor who did what (compliance)
- **Avoid basic roles:** Use predefined or custom

---

## Links

- [IAM Documentation](https://cloud.google.com/iam/docs)
- [Predefined Roles](https://cloud.google.com/iam/docs/understanding-roles)