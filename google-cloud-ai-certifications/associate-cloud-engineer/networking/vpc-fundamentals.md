# VPC Fundamentals – ACE

_Last Updated: November 30, 2025_

## Overview

Virtual Private Cloud (VPC) isolates your resources from internet & other projects. Core networking service (8–12% of ACE exam).

---

## VPC Structure

```
VPC (my-vpc, 10.0.0.0/8)
├─ Subnet 1 (us-central1, 10.0.1.0/24)
│  └─ GCE Instance A
├─ Subnet 2 (europe-west1, 10.0.2.0/24)
│  └─ GCE Instance B
├─ Firewall Rules (allow SSH, deny by default)
├─ Cloud Router (connect to on-prem)
├─ Cloud VPN (encrypted tunnel)
└─ Cloud NAT (private instances → internet)
```

---

## Creating VPC

```bash
# Create VPC (custom subnet mode recommended)
gcloud compute networks create my-vpc \
  --subnet-mode custom

# Create subnet
gcloud compute networks subnets create my-subnet \
  --network my-vpc \
  --range 10.0.1.0/24 \
  --region us-central1

# Create firewall rule (allow SSH from office)
gcloud compute firewall-rules create allow-ssh \
  --network my-vpc \
  --allow tcp:22 \
  --source-ranges 203.0.113.0/24

# Create firewall rule (deny all else)
gcloud compute firewall-rules create deny-all \
  --network my-vpc \
  --deny all \
  --priority 65534

# Create instance in VPC
gcloud compute instances create my-vm \
  --network my-vpc \
  --subnet my-subnet \
  --zone us-central1-a
```

---

## Firewall Rules

- **Default:** Allow all internal traffic, deny inbound external
- **Rules:** Stateful (outbound allowed if inbound allowed)
- **Priority:** Lower = higher priority (0–65534)

---

## Cloud NAT

Allow private instances to reach internet (for updates, downloads).

```bash
# Create Cloud Router
gcloud compute routers create my-router \
  --network my-vpc \
  --region us-central1

# Create Cloud NAT
gcloud compute routers nats create my-nat \
  --router my-router \
  --region us-central1 \
  --auto-allocate-nat-external-ips \
  --nat-all-subnet-ip-ranges
```

---

## VPN & Hybrid

Connect on-premises network to GCP VPC.

```bash
# Create Cloud VPN gateway
gcloud compute vpn-gateways create my-gateway \
  --network my-vpc \
  --region us-central1

# Create tunnel (simplifies VPN setup)
```

---

## Common ACE Questions

**Q1:** Production database must be private (not accessible from internet). Setup?
- A) Create VPC + subnet + deny firewall rule
- B) Use default VPC (auto-deny external)
- C) Both acceptable
- D) Make instance on internet (with firewall)

**Answer:** A. Custom VPC + explicit firewall rules (most secure).

**Q2:** Instance needs to download OS updates (from internet) but must be private. Setup?
- A) Allow outbound HTTP/HTTPS via firewall
- B) Use Cloud NAT (private IP → internet)
- C) Both acceptable
- D) Connect via VPN only

**Answer:** B. Cloud NAT cleanest (no need to expose instance on internet).

---

## Links

- [VPC Documentation](https://cloud.google.com/vpc/docs)
- [Firewall Rules](https://cloud.google.com/vpc/docs/firewalls)