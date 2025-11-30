# Compute Engine – Associate Cloud Engineer

_Last Updated: November 30, 2025_

## Overview

Google Cloud Compute Engine provides scalable, high-performance virtual machines (VMs). Core service for ACE exam (10–15% of questions).

---

## Key Concepts

### VM Instances
- **Machine type:** CPU + memory configuration (e.g., n1-standard-2 = 2 vCPU, 7.5 GB RAM)
- **Image:** OS + software (Debian, CentOS, Windows, custom)
- **Disk:** Boot disk (system), data disks (persistent volumes)
- **Metadata:** User-defined key-value pairs + startup scripts

### Machine Types
| Type | Use Case | Cost |
|------|----------|------|
| n1-standard | General-purpose | £0.024/hour |
| n1-highmem | Memory-intensive (databases) | £0.030/hour |
| n1-highcpu | CPU-intensive (ML training) | £0.017/hour |
| e2-standard | Budget-friendly | £0.014/hour |
| custom | User-defined (e.g., 3 vCPU, 10 GB RAM) | Variable |

### Creating a VM
```bash
# Create VM
gcloud compute instances create my-instance \
  --machine-type n1-standard-2 \
  --image-family debian-11 \
  --image-project debian-cloud \
  --zone us-central1-a

# View instances
gcloud compute instances list

# SSH into VM
gcloud compute ssh my-instance --zone us-central1-a
```

### Disks
- **Boot disk:** Required; deleted with instance (by default)
- **Persistent disk:** Survives instance deletion (manual delete needed)
- **Local SSD:** Faster but ephemeral (lost if instance stops)
- **Snapshots:** Point-in-time backups for recovery

```bash
# Create persistent disk
gcloud compute disks create my-disk --size 100GB --zone us-central1-a

# Attach to running instance
gcloud compute instances attach-disk my-instance --disk my-disk --zone us-central1-a
```

---

## Managed Instance Groups (MIG)

**Purpose:** Automate VM creation/deletion based on load.

### Stateless MIG (Recommended)
- All VMs identical (stateless)
- Automatically scales up/down
- Cost: ~£0.01/hour per VM (n1-standard-1)

```bash
# Create instance template
gcloud compute instance-templates create my-template \
  --machine-type n1-standard-1 \
  --image-family debian-11 \
  --scopes default,cloud-platform

# Create MIG
gcloud compute instance-groups managed create my-mig \
  --base-instance-name my-vm \
  --template my-template \
  --size 2 \
  --zone us-central1-a

# Enable autoscaling
gcloud compute instance-groups managed set-autoscaling my-mig \
  --max-num-replicas 5 \
  --min-num-replicas 2 \
  --target-cpu-utilization 0.70 \
  --zone us-central1-a
```

### Stateful MIG
- VMs retain local disks + network settings
- Use: Databases, clustered apps

---

## Preemptible & Spot VMs

**Trade-off:** 60–70% cheaper, but can be terminated anytime (24-hour max lifespan).

### When to Use
- Batch jobs (data processing, image rendering)
- CI/CD pipelines (acceptable to restart)
- Dev/test environments

### When NOT to Use
- Production databases (data loss risk)
- Real-time services (customers affected)

```bash
# Create preemptible VM (saves £50/month on n1-standard-4)
gcloud compute instances create my-batch-job \
  --preemptible \
  --machine-type n1-standard-4 \
  --zone us-central1-a
```

**Cost Comparison (Monthly):**
| Config | Regular | Preemptible | Savings |
|--------|---------|-------------|---------|
| n1-standard-4 (730 hours) | £58.44 | £17.53 | 70% |
| n1-highcpu-16 | £142.90 | £42.87 | 70% |

---

## Startup Scripts

Run commands automatically when VM boots. Common uses: install software, configure firewall, pull code.

```bash
# Create startup script
cat > startup.sh << 'EOF'
#!/bin/bash
apt-get update
apt-get install -y apache2
systemctl start apache2
echo "Hello from $(hostname)" > /var/www/html/index.html
EOF

# Create VM with startup script
gcloud compute instances create my-web-server \
  --machine-type n1-standard-1 \
  --metadata-from-file startup-script=startup.sh \
  --zone us-central1-a
```

---

## Common ACE Exam Questions

**Q1:** Which machine type for data warehouse (1TB+ RAM, 64 vCPU)?
- A) n1-standard-2
- B) n1-highmem-64 ✅
- C) n1-highcpu-16
- D) e2-standard-2

**Answer:** B. High-memory workloads need highmem; highcpu for CPU-bound (not RAM).

**Q2:** Batch job stops unexpectedly mid-processing. Why?
- A) Instance ran out of disk space
- B) Preemptible VM was terminated
- C) Network timeout
- D) OOM (out of memory)

**Answer:** B (most likely if cost-optimised). Preemptible VMs get 24-hour TTL or termination notice.

**Q3:** Autoscaling policy: target-cpu-utilization 70%, max-replicas 5. At 90% CPU, what happens?
- A) Scale down (too much capacity)
- B) Scale up (add VMs until CPU ≤ 70%)
- C) No change (already at max)
- D) Alert only (no action)

**Answer:** B. Until reaching 5 replicas or target utilization hit.

---

## Cost Optimisation

- Use preemptible VMs for batch (save 70%)
- Right-size instances (n1-standard-1 vs 4?)
- Enable autoscaling (pay only for used capacity)
- Use committed discounts (1-/3-year contracts, save 30%)

---

## Links

- [Compute Engine Documentation](https://cloud.google.com/compute/docs)
- [Machine Types Pricing](https://cloud.google.com/compute/pricing)
- [Instances & Images Guide](https://cloud.google.com/compute/docs/instances)