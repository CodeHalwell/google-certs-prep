# Error Reporting & Debugging – ACE

_Last Updated: November 30, 2025_

## Overview

Error Reporting (centralised crash dashboard) + Cloud Trace (performance profiling). Troubleshooting tools (2–3% of ACE exam).

---

## Cloud Error Reporting

Automatically aggregate errors from apps.

```bash
# Errors appear automatically in Cloud Logging
# View in UI: Cloud Error Reporting

# Manually report error (from code)
import google.cloud.logging
logging.Client().logging_api.write_entries([
    {"severity": "ERROR", "message": "App crashed"}
])
```

---

## Cloud Trace

Performance profiling; identify slow requests.

```bash
# Enable Trace in code (Flask example)
from google.cloud import trace
trace_client = trace.Client()
tracer = trace_client.tracer('my-app')

with tracer.span('expensive-operation') as span:
    # Do work
    pass
```

---

## Cloud Debugger

Debug production apps without stopping execution.

```bash
# Set snapshot (capture variables at breakpoint)
gcloud beta debug snapshots create \
  --target app=my-app \
  --location file.py:42
```

---

## Common ACE Questions

**Q1:** Multiple app instances crashing. Best approach to diagnose?
- A) SSH to each VM + check logs manually
- B) Cloud Error Reporting (aggregated crash dashboard)
- C) Both
- D) Restart instances

**Answer:** B. Error Reporting shows crash patterns across all instances instantly.

---

## Links

- [Error Reporting Documentation](https://cloud.google.com/error-reporting/docs)
- [Cloud Trace Documentation](https://cloud.google.com/trace/docs)