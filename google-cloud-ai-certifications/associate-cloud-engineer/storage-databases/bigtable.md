# Bigtable – ACE

_Last Updated: November 30, 2025_

## Overview

Massive-scale NoSQL database (petabytes). Time-series, analytics, IoT data. Less common in ACE (2–3%).

---

## Use Cases

- Time-series (metrics, logs)
- IoT sensors (millions of data points)
- Analytics (petabyte-scale)

---

## Instance Structure

```
Bigtable Instance
├─ Cluster 1 (us-central1)
│  └─ Nodes (3+)
├─ Cluster 2 (europe-west1)
├─ Table (e.g., sensor-data)
│  └─ Column families
│     ├─ cf1 (data)
│     └─ cf2 (metadata)
```

---

## Creating Instance

```bash
# Create instance
gcloud bigtable instances create my-instance \
  --cluster my-cluster \
  --cluster-zone us-central1-a \
  --instance-type PRODUCTION

# Create table
gcloud bigtable tables create my-table \
  --instance my-instance \
  --split-keys 1,2,3

# Write data
```

---

## When to Use

**Choose Bigtable if:**
- Massive scale (>1TB data)
- Time-series or analytics
- Millions of writes/sec

**Don't choose if:**
- Small dataset (<100GB, use Cloud SQL)
- Complex queries (use BigQuery)

---

## Links

- [Bigtable Documentation](https://cloud.google.com/bigtable/docs)