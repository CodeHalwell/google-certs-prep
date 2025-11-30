# Cloud SQL – ACE

_Last Updated: November 30, 2025_

## Overview

Managed relational database (MySQL, PostgreSQL, SQL Server). Automatic backups, replication, failover. 5–8% of ACE exam.

---

## Creating Instance

```bash
# Create Cloud SQL instance (MySQL)
gcloud sql instances create my-db \
  --database-version MYSQL_8_0 \
  --tier db-n1-standard-1 \
  --region us-central1

# Create database
gcloud sql databases create my-app-db \
  --instance my-db

# Create user
gcloud sql users create my-user \
  --instance my-db \
  --password my-password

# Get connection info
gcloud sql instances describe my-db

# Connect locally
cloud_sql_proxy -instances PROJECT:us-central1:my-db=tcp:3306 &
mysql -h 127.0.0.1 -u my-user -p
```

---

## High Availability

```bash
# Enable automatic failover
gcloud sql instances patch my-db \
  --enable-bin-log \
  --backup-start-time 03:00 \
  --availability-type REGIONAL
```

---

## Backup & Recovery

```bash
# Create backup
gcloud sql backups create \
  --instance my-db

# List backups
gcloud sql backups list --instance my-db

# Restore from backup
gcloud sql backups restore BACKUP-ID \
  --backup-instance my-db \
  --target-instance my-db
```

---

## Common ACE Questions

**Q1:** Production database needs 99.95% uptime (SLA). Setup?
- A) Single instance (no redundancy)
- B) Regional HA (replica in different zone)
- C) Both; B recommended
- D) Manual failover

**Answer:** B. Cloud SQL regional HA auto-failover if primary fails.

**Q2:** Backup strategy: daily backups for 30 days. Configuration?
- A) Default (7-day retention)
- B) Custom: set backup frequency + retention
- C) Manual backups only
- D) No backup (risky)

**Answer:** B. Set automated backups with 30-day retention window.

---

## Links

- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)