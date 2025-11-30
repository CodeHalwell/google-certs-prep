# Firestore & Datastore – ACE

_Last Updated: November 30, 2025_

## Overview

NoSQL document databases. Firestore (recommended) for new apps; Datastore (legacy).

---

## Firestore

Scalable NoSQL document database.

```bash
# Create database
gcloud firestore databases create --location us-central1

# Add document
gcloud firestore documents create \
  --collection users \
  --document alice \
  --data name=Alice,age=30

# Query
gcloud firestore documents list --collection users

# Update
gcloud firestore documents update \
  --collection users \
  --document alice \
  --data age=31
```

### Query Example
```python
from google.cloud import firestore
db = firestore.Client()
docs = db.collection('users').where('age', '>', 25).get()
```

---

## When to Use

**Choose Firestore if:**
- Flexible schema (no fixed columns)
- Real-time queries + subscriptions
- Mobile/web apps (offline sync)

**Choose Cloud SQL if:**
- Structured data (fixed schema)
- Complex joins
- Strong consistency required

---

## Common ACE Questions

**Q1:** Mobile app needs offline-first database (sync when online). Choice?
- A) Cloud SQL (doesn't sync offline)
- B) Firestore (built-in offline + sync)
- C) Cloud Storage (not database)
- D) BigQuery (read-only, batch)

**Answer:** B. Firestore designed for mobile.

---

## Links

- [Firestore Documentation](https://cloud.google.com/firestore/docs)