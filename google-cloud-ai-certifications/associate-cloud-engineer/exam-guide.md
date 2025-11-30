# ACE Exam Study Guide

_Last Updated: November 30, 2025_

Comprehensive 6-week study plan for the Associate Cloud Engineer exam. Estimated time: 60–80 hours.

---

## Exam Overview

**Format:** Multiple-choice + scenario-based questions (50 questions, 2 hours)  
**Cost:** £128  
**Pass Mark:** 70% (~35 questions)  
**Domains:** 5 focus areas with varying weights

---

## Exam Domains & Weights

| Domain | Weight | Topics |
|--------|--------|--------|
| **Compute Engine** | 30% | VMs, MIGs, preemptible, startup scripts, SSH |
| **GKE & Containers** | 20% | Clusters, deployments, services, rolling updates |
| **App Engine & Cloud Run** | 15% | Runtimes, scaling, traffic split, serverless |
| **Storage & Databases** | 20% | Cloud SQL, Firestore, Bigtable, Cloud Storage |
| **Security & Networking** | 15% | IAM, VPC, firewall, load balancing, Cloud NAT |

---

## 6-Week Study Plan

### Week 1: Compute Engine & VMs

**Topics:**
- VM instances, machine types (e2, n2, c2 series)
- Managed Instance Groups (MIGs), autoscaling
- Preemptible VMs (70% discount, 24-hour max lifetime)
- Startup scripts, cloud-init
- SSH access, IAP (Identity-Aware Proxy)

**Study Materials:**
- [compute-engine.md](./core-services/compute-engine.md)
- [Hands-On Lab 1](./hands-on-labs.md#lab-1-deploy-web-server-on-compute-engine)

**Key Commands:**
```bash
gcloud compute instances create NAME --machine-type=e2-medium
gcloud compute instance-groups managed create NAME --template=TEMPLATE
gcloud compute backend-services create NAME
```

**Common Exam Questions:**
- "Which instance type for high CPU workload?" → **c2** or **n2** series
- "How to save 70% on compute cost?" → **Preemptible VMs** (with fallback strategy)
- "Reduce RTO if zone fails?" → **Multi-zone MIG** + load balancer

---

### Week 2: GKE & Container Orchestration

**Topics:**
- GKE cluster creation, node pools
- Kubernetes workloads: Deployments, StatefulSets, Jobs
- Services (ClusterIP, NodePort, LoadBalancer)
- Rolling updates, traffic policies
- Helm basics, GitOps

**Study Materials:**
- [kubernetes-engine.md](./core-services/kubernetes-engine.md)
- [Hands-On Lab 2](./hands-on-labs.md#lab-2-deploy-multi-tier-app-on-gke)

**Key Commands:**
```bash
gcloud container clusters create CLUSTER_NAME --zone=ZONE --num-nodes=3
kubectl apply -f deployment.yaml
kubectl set image deployment/app app=IMAGE:v2
kubectl rollout status deployment/app
```

**Common Exam Questions:**
- "How to safely update running pods?" → **Rolling updates** (old pods terminate, new start)
- "Service type for internal-only communication?" → **ClusterIP**
- "Multi-zone resilience?" → **Regional GKE cluster**

---

### Week 3: App Engine & Cloud Run

**Topics:**
- App Engine Standard vs Flexible
- Runtime support (Python, Node.js, Java)
- Automatic scaling (0–N instances)
- Cloud Run: containers, Pub/Sub triggers, HTTP triggers
- Traffic splitting, canary deployments
- Cost comparison (pay-per-instance vs pay-per-request)

**Study Materials:**
- [app-engine.md](./core-services/app-engine.md)
- [cloud-run.md](./core-services/cloud-run.md)
- [Hands-On Lab 3](./hands-on-labs.md#lab-3-deploy-app-on-app-engine)
- [Hands-On Lab 4](./hands-on-labs.md#lab-4-trigger-cloud-function-via-pubsub)

**Key Commands:**
```bash
gcloud app deploy
gcloud run deploy SERVICE --image=IMAGE --platform managed
gcloud run services update SERVICE --traffic=REVISION=100
```

**Common Exam Questions:**
- "Cheapest for variable traffic?" → **App Engine Standard** or **Cloud Run** (pay-per-use)
- "Long-running batch job?" → **Compute Engine** or **Cloud Run** (540s timeout)
- "Canary deployment?" → **Cloud Run traffic splitting** (50% old, 50% new version)

---

### Week 4: Storage & Databases

**Topics:**
- Cloud Storage classes (Standard, Nearline, Coldline, Archive)
- Storage lifecycle policies (auto-delete, auto-transition)
- Cloud SQL (MySQL, PostgreSQL, SQL Server), HA setup, backups, PITR
- Firestore vs Datastore (NoSQL, document-based)
- Bigtable (massive scale, time-series, IoT)
- BigQuery (data warehouse, analytics)
- When-to-use decision matrix

**Study Materials:**
- [cloud-storage.md](./storage-databases/cloud-storage.md)
- [cloud-sql.md](./storage-databases/cloud-sql.md)
- [firestore-datastore.md](./storage-databases/firestore-datastore.md)
- [bigtable.md](./storage-databases/bigtable.md)
- [Hands-On Lab 5](./hands-on-labs.md#lab-5-create-cloud-sql-database--connect-app)

**Key Commands:**
```bash
gsutil mb -c STORAGE_CLASS gs://BUCKET_NAME
gcloud sql instances create INSTANCE --tier=db-f1-micro
gcloud firestore databases create --database=default
```

**Common Exam Questions:**
- "Which database for real-time mobile sync?" → **Firestore** (offline support)
- "Which for analytics + 7-year retention?" → **BigQuery** (cost-effective, unlimited retention)
- "Which for massive-scale time-series (petabytes)?" → **Bigtable**

---

### Week 5: Networking & Security

**Topics:**
- VPC design, custom subnets, firewall rules (deny-all-default pattern)
- Cloud NAT (for private instances egress)
- Cloud Armor (WAF + DDoS protection)
- Load balancers (Network LB, HTTP/S LB, Internal)
- IAM (roles, service accounts, least privilege)
- VPC peering, Cloud VPN, hybrid connectivity

**Study Materials:**
- [vpc-fundamentals.md](./networking/vpc-fundamentals.md)
- [firewall-cloud-armor.md](./networking/firewall-cloud-armor.md)
- [load-balancing.md](./networking/load-balancing.md)
- [identity-access-management.md](./iam-security/identity-access-management.md)
- [security-best-practices.md](./iam-security/security-best-practices.md)
- [Hands-On Lab 6](./hands-on-labs.md#lab-6-configure-vpc-firewall--cloud-nat)

**Key Commands:**
```bash
gcloud compute networks create VPC --subnet-mode=custom
gcloud compute firewall-rules create RULE --allow=tcp:5432 --source-tags=api-server
gcloud compute routers nats create NAT --nat-all-subnet-ip-ranges
```

**Common Exam Questions:**
- "How to allow SSH only from office (203.0.113.0/24)?" → **Firewall rule with source-ranges**
- "Private database needs internet access for apt-get?" → **Cloud NAT**
- "DDoS + Layer-7 attack protection?" → **Cloud Armor** on HTTP(S) LB
- "Grant least privilege?" → **Custom role** with minimal permissions

---

### Week 6: Monitoring, Cost & Scenarios

**Topics:**
- Cloud Monitoring (metrics, dashboards, alerts)
- Cloud Logging (log sinks, exports, archival)
- Error Reporting, Cloud Trace, Cloud Debugger
- Cost optimization (reserved instances, committed use discounts, preemptible VMs)
- Incident response, troubleshooting
- Real-world scenarios (multi-tier app, HA/DR, cost reduction)

**Study Materials:**
- [monitoring-logging.md](./monitoring-operations/monitoring-logging.md)
- [error-reporting-debugging.md](./monitoring-operations/error-reporting-debugging.md)
- [practice-exam.md](./practice-exam.md)

**Key Commands:**
```bash
gcloud monitoring dashboards create --config-from-file=dashboard.yaml
gcloud logging sinks create NAME DESTINATION --log-filter='severity="ERROR"'
gcloud beta debug snapshots create --location=FILE:LINE
```

**Common Exam Questions:**
- "Cost reduction without SLA impact?" → **Preemptible VMs** + **BigQuery** (separate analytics)
- "Memory leak diagnosis?" → **Cloud Debugger** (snapshot) + **Cloud Logging** (stack traces)
- "Archive logs 7 years?" → **Cloud Logging sink** → **Cloud Storage Archive class**

---

## Study Checklist

**Checkpoint 1 (Week 2):**
- [ ] Completed Compute Engine learning path
- [ ] Completed GKE learning path
- [ ] Passed Compute + GKE sections of practice exam (score ≥ 70%)

**Checkpoint 2 (Week 4):**
- [ ] Completed App Engine + Cloud Run learning paths
- [ ] Completed Storage + Database learning path
- [ ] Passed App Engine + Storage sections of practice exam (score ≥ 70%)

**Checkpoint 3 (Week 6):**
- [ ] Completed Networking + Security learning path
- [ ] Completed Monitoring + Cost learning path
- [ ] Passed full practice exam (score ≥ 420/600)
- [ ] Completed all 6 hands-on labs

**Final Week:**
- [ ] Retake practice exam (target: 500+/600)
- [ ] Review weak areas (domain-specific review)
- [ ] Do 2–3 practice questions per domain daily

---

## Weak Area Strategy

If you score < 70% on a domain:

1. **Compute Engine** (< 70%):
   - Review: Machine types, MIGs, preemptible VMs
   - Lab: Recreate Compute Engine instance + MIG with autoscaling
   - Practice: 5 more compute-focused questions

2. **GKE** (< 70%):
   - Review: Deployments, services, rolling updates
   - Lab: Deploy + update app on GKE; measure rollout time
   - Practice: 5 more GKE-focused questions

3. **App Engine / Cloud Run** (< 70%):
   - Review: Scaling, traffic splitting, costs
   - Lab: Deploy Flask to App Engine; compare cost with Cloud Run
   - Practice: 5 more serverless-focused questions

4. **Storage/Databases** (< 70%):
   - Review: Decision matrix (Cloud SQL vs Firestore vs BigQuery vs Bigtable)
   - Lab: Create 3 different database types; compare costs
   - Practice: 5 more database-focused questions

5. **Networking/Security** (< 70%):
   - Review: VPC, firewall, IAM roles, load balancers
   - Lab: Design private VPC + deny-all-default firewall + Cloud NAT
   - Practice: 5 more network-focused questions

---

## Exam Day Tips

- **Time Management:** 50 questions ÷ 120 minutes = 2.4 min per question
  - Spend 1 min reading; 1 min deciding; 0.4 min for certainty check
  - Flag difficult questions; return if time permits

- **Strategy:**
  - Answer easy questions first (80% certainty)
  - Defer hard scenarios (flag + return)
  - Last 5 min: Review flagged questions

- **Common Mistakes to Avoid:**
  - Confusing Firestore (offline mobile) with Cloud SQL (relational)
  - Forgetting Cloud NAT for private VMs needing internet
  - Choosing db-n1-highmem for small workloads (overkill cost)
  - Assuming all services are free (read pricing!)

---

## Cost Estimate (Hands-On Labs)

Running all 6 labs (assuming cleanup after each):
- Compute Engine: ~£2
- GKE cluster (1-2 hours): ~£1
- App Engine: £0 (free tier)
- Cloud Run: ~£0.10
- Cloud SQL: £0.50 (1-2 hours runtime)
- VPC + NAT: £0.20
- **Total: ~£4–5**

---

## Post-Exam

**If You Pass:**
- Celebrate! 🎉 You're now ACE-certified
- Update resume + LinkedIn
- Consider: Professional ML Engineer or Generative AI Leader (next cert)

**If You Don't Pass:**
- Don't panic; most people pass on 2nd attempt
- Review: Which domain scored < 60%?
- Focus: 2–3 weeks on weak areas
- Retake: Reschedule exam for 2–3 weeks later

---

## Links

- [Compute Engine Learning Path](./core-services/compute-engine.md)
- [GKE Learning Path](./core-services/kubernetes-engine.md)
- [Networking Learning Path](./networking/vpc-fundamentals.md)
- [Practice Exam](./practice-exam.md)
- [Hands-On Labs](./hands-on-labs.md)
- [Official Exam Guide](https://cloud.google.com/certification/cloud-engineer)