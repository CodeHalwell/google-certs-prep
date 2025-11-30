# Cloud Storage – ACE

_Last Updated: November 30, 2025_

## Overview

Object storage (files, images, backups). Unlimited scale, globally accessible. 8–12% of ACE exam.

---

## Storage Classes

| Class | Latency | Cost | Use Case |
|-------|---------|------|----------|
| Standard | Immediate | £0.020/GB | Active data |
| Nearline | Minutes | £0.010/GB | Accessed <1x/month |
| Coldline | Hours | £0.004/GB | Accessed <1x/year |
| Archive | Hours | £0.0012/GB | Compliance archive |

---

## Buckets & Objects

```bash
# Create bucket (globally unique name)
gsutil mb gs://my-unique-bucket-name

# Upload file
gsutil cp local-file.txt gs://my-unique-bucket-name/

# Download file
gsutil cp gs://my-unique-bucket-name/local-file.txt .

# List files
gsutil ls gs://my-unique-bucket-name/

# Delete object
gsutil rm gs://my-unique-bucket-name/local-file.txt

# Delete bucket
gsutil rm -r gs://my-unique-bucket-name/
```

---

## Access Control

- **Uniform bucket-level (recommended):** IAM controls all access
- **Fine-grained:** Per-object ACL (complex, avoid)

```bash
# Grant read access to user
gsutil iam ch user:alice@example.com:objectViewer gs://my-bucket

# Grant write access
gsutil iam ch user:bob@example.com:objectEditor gs://my-bucket
```

---

## Versioning & Lifecycle

```bash
# Enable versioning (keep old versions)
gsutil versioning set on gs://my-bucket

# Set lifecycle policy (auto-delete old versions)
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 365}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
        "condition": {"age": 90}
      }
    ]
  }
}
EOF

gsutil lifecycle set lifecycle.json gs://my-bucket
```

---

## Common ACE Questions

**Q1:** Store images (accessed 1x/month). Cheapest storage class?
- A) Standard (£0.020/GB)
- B) Nearline (£0.010/GB, ideal for <1x/month)
- C) Coldline (£0.004/GB, but slow retrieval)
- D) Archive (£0.0012/GB, very slow)

**Answer:** B. Nearline balances cost + latency.

**Q2:** Bucket needs public read access (website assets). Setup?
- A) Grant public user:* permissions
- B) Make all objects public (unsafe)
- C) Use bucket policy (allow allUsers:ObjectViewer)
- D) Create signed URLs (time-limited access)

**Answer:** C or D. C = always public; D = temporary access (more flexible).

---

## Links

- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)