# Cloud Monitoring & Logging – ACE

_Last Updated: November 30, 2025_

## Overview

Cloud Monitoring (metrics, dashboards, alerts) + Cloud Logging (centralized logs). Observability core (5–8% of ACE exam).

---

## Cloud Monitoring

Track metrics (CPU, memory, latency) in real-time.

```bash
# Create custom metric
gcloud monitoring metrics-descriptors create \
  --display-name "App Requests" \
  --metric-kind GAUGE \
  --value-type INT64 \
  --resource-labels resource.type=global

# Create dashboard
gcloud monitoring dashboards create \
  --config-from-file dashboard.json

# Create alert
gcloud alpha monitoring policies create \
  --notification-channels CHANNEL_ID \
  --display-name "High CPU Alert" \
  --condition-display-name "CPU > 80%"
```

---

## Cloud Logging

Centralized logs from all services.

```bash
# View logs
gcloud logging read "resource.type=gce_instance" --limit 10

# Create log sink (export to Cloud Storage)
gcloud logging sinks create my-sink gs://my-bucket/ \
  --log-filter 'severity=ERROR'

# Stream logs in real-time
gcloud logging read --stream
```

---

## Common ACE Questions

**Q1:** CPU spiking on production VM. Diagnose?
- A) Cloud Monitoring (shows CPU metric history)
- B) Cloud Logging (shows application errors)
- C) Both
- D) SSH + top command

**Answer:** C. Monitoring shows CPU spike; Logging reveals error causing spike.

**Q2:** Archive old logs (compliance requirement: 7 years). Setup?
- A) Keep in Cloud Logging (too expensive)
- B) Export to Cloud Storage (cheaper)
- C) Export to BigQuery (queryable archive)
- D) B or C

**Answer:** D. Storage cheaper for cold storage; BigQuery if need to query.

---

## Links

- [Cloud Monitoring Documentation](https://cloud.google.com/monitoring/docs)
- [Cloud Logging Documentation](https://cloud.google.com/logging/docs)