# ACE Practice Exam

_Last Updated: November 30, 2025_

6 full scenario-based questions mirroring the real Associate Cloud Engineer exam. Each question: 3–5 sub-parts; model answers; scoring rubric.

---

## Question 1: Multi-Tier Web App Deployment

**Scenario:**

You're designing a web application for an e-commerce platform. Requirements:
- Handles variable traffic (peak: 1,000 req/s; off-peak: 10 req/s)
- Multiple service tiers: frontend (REST API), backend (worker), database
- 99.9% availability SLA
- Budget: £200/month
- Team: 3 engineers (need simple ops)

Your manager asks: "What's our deployment strategy?"

**Sub-Questions:**

1. **Compute:** Which platform for the REST API frontend?
   - A) Compute Engine (manually manage VMs)
   - B) App Engine Standard (auto-scales to zero)
   - C) GKE (container orchestration)
   - D) Cloud Functions (serverless)
   
   **Model Answer:** B (App Engine Standard)
   - Rationale: Auto-scales from 0–N instances based on traffic; cheapest for variable workloads; minimal ops overhead; 99.9% SLA built-in
   - Cost: 0–£50/month depending on traffic
   - Supports: Flask, Django, Python 3
   - Alternative: C is defensible if team prefers full container control, but adds operational complexity
   
2. **Database:** How should you set up Cloud SQL (PostgreSQL)?
   - A) Single instance (us-central1-a)
   - B) Regional HA (multi-zone failover)
   - C) Read replicas in multiple regions
   - D) Managed serverless (Firebase Realtime DB)
   
   **Model Answer:** B (Regional HA)
   - Rationale: Meets 99.9% SLA; automatic failover if zone fails; backup window configurable
   - Cost: db-f1-micro with HA: ~£30/month
   - Alternative: A is cheaper (£15/month) but fails SLA; C adds unnecessary cost without SLA benefit
   
3. **Background Jobs:** Process orders (rate: 10 jobs/sec, ~30s each). Which service?
   - A) Cloud Functions (timeout: 540s)
   - B) Cloud Tasks (distributed task queue)
   - C) Cloud Pub/Sub + Cloud Run (event-driven)
   - D) Compute Engine (manually manage)
   
   **Model Answer:** C (Cloud Pub/Sub + Cloud Run)
   - Rationale: Pub/Sub ensures job delivery; Cloud Run auto-scales to handle 10 req/s; 540s timeout sufficient
   - Cost: £0.40/M Pub/Sub messages (~£0.003/day) + Cloud Run compute
   - Alternative: B (Cloud Tasks) is valid if you prefer explicit scheduling; A works but Pub/Sub offers decoupling
   
4. **Network Security:** Architect VPC security for this setup.
   - A) All services in public subnet; rely on firewall
   - B) Private subnet (10.0.0.0/24); Cloud NAT for egress; deny-all-default firewall rules
   - C) No VPC; use default VPC
   - D) Public subnet with security groups
   
   **Model Answer:** B (Private subnet + Cloud NAT + deny-all-default)
   - Rationale: Defence-in-depth principle; isolates services from internet; deny-all-default + allow-by-need pattern
   - Cloud NAT: ~£32/month + egress charges
   - App Engine/Cloud Run have private VPC integration built-in
   
5. **Cost Breakdown:** Estimate monthly cost for 1,000 req/s peak, 10 req/s avg.
   - Compute: App Engine £25/month
   - Database: Cloud SQL HA £30/month
   - Network: Cloud NAT £35/month + £5 egress
   - Pub/Sub: £3/month
   - **Total: ~£98/month** ✓ Under £200 budget
   
   **Exam Tip:** Show cost calculations; real ACE questions ask "Which service for [budget + SLA + traffic]?"

---

## Question 2: Database Selection Decision Tree

**Scenario:**

Your team is choosing a database for three use cases. Budget: £100/month total.

**Use Case A:** Mobile app with offline-first sync (users read/write locally; cloud syncs later)
**Use Case B:** Time-series sensor data (IoT devices: 1M readings/day; analytical queries; retention: 7 years)
**Use Case C:** Relational app (orders, customers, inventory; complex joins; transactions)

Your task: Recommend a database per use case. Justify cost + architecture tradeoffs.

**Sub-Questions:**

1. **Use Case A – Offline-First Sync:** Which database?
   - A) Cloud SQL (PostgreSQL)
   - B) Firestore (real-time document DB)
   - C) Bigtable (massive-scale NoSQL)
   - D) BigQuery (data warehouse)
   
   **Model Answer:** B (Firestore)
   - Rationale: Built-in offline support; real-time sync when online; flexible schema; mobile SDKs (iOS, Android)
   - Cost: Pay-per-read/write (~£0.06/100k reads); typical: £5–10/month
   - Alternative: A works but requires manual sync logic; C designed for analytical, not transactional
   
2. **Use Case B – Time-Series Analytics:** Which database?
   - A) Cloud SQL
   - B) Firestore
   - C) Bigtable
   - D) BigQuery
   
   **Model Answer:** D (BigQuery) OR C (Bigtable)
   - Rationale D: 1M rows/day = 365M rows/year = manageable in BigQuery; SQL for analytics; 7-year retention trivial
     - Cost: £0.0769/GB scanned; typical: £10–20/month
   - Rationale C: If read-heavy analytics + writes are critical; massive scale support
     - Cost: 3-node cluster: £150/month (over budget)
   - **Recommended: D (BigQuery)** for analytics; cost-effective
   
3. **Use Case C – Relational App:** Which database?
   - A) Cloud SQL
   - B) Firestore
   - C) Bigtable
   - D) BigQuery
   
   **Model Answer:** A (Cloud SQL)
   - Rationale: ACID transactions; JOIN support; relational schema (orders→customers→inventory)
   - Cost: db-f1-micro: £15/month; sufficient for typical app
   - Firestore: Non-relational; complex joins awkward
   
4. **Total Cost Estimate:**
   - Use Case A (Firestore): £8/month
   - Use Case B (BigQuery): £15/month
   - Use Case C (Cloud SQL): £15/month
   - **Total: ~£38/month** ✓ Under £100
   
   **Exam Tip:** Know decision matrix: Firestore (offline mobile), BigQuery (analytics), Cloud SQL (relational), Bigtable (massive scale + read-heavy)

---

## Question 3: High Availability & Disaster Recovery

**Scenario:**

Your company runs a financial API on GCP (monthly transactions: £10M). Current setup: Single Compute Engine instance (zone: us-central1-a). CEO asks: "What happens if the zone fails?"

**Requirements:**
- RTO (Recovery Time Objective): < 5 minutes
- RPO (Recovery Point Objective): < 1 minute (no data loss)
- Budget: < £500/month additional

Your task: Design HA/DR strategy.

**Sub-Questions:**

1. **Compute HA:** How to ensure API remains up if zone fails?
   - A) Same instance in another zone (manual failover)
   - B) Multi-zone Managed Instance Group (auto-failover)
   - C) App Engine (regional, built-in HA)
   - D) GKE (multi-zone cluster)
   
   **Model Answer:** B (Multi-zone MIG) OR C (App Engine)
   - Rationale B: 2-3 instances across zones; health checks trigger auto-restart; HTTP(S) LB distributes traffic; meets RTO < 5 min
     - Cost: 2 × e2-medium: ~£50/month; LB: ~£5/month
   - Rationale C: Regional deployment; auto-scales; 99.9% SLA standard
     - Cost: £20–50/month depending on traffic
   - Both meet SLA; B gives more control; C simpler ops
   
2. **Data HA:** Protect database (Cloud SQL).
   - A) Manual backups (daily)
   - B) Automated backups + read replicas in same region
   - C) Regional failover (automatic HA setup)
   - D) Cross-region read replicas
   
   **Model Answer:** C (Regional failover) + D (Cross-region read replicas for disaster recovery)
   - Rationale: Regional failover: auto-promoted replica; meets RPO < 1 min (continuous replication)
     - Cost: +20% on instance cost (~£6/month for db-f1-micro)
   - Cross-region replica: For true DR (zone + region failure); slower failover but data safety
     - Cost: +100% (full replica in another region: £15/month)
   - Recommended: C (regional) for HA + D (cross-region) for DR
   
3. **State Management:** How to sync session state across instances?
   - A) Store in VM local disk
   - B) Store in Cloud SQL (all instances query)
   - C) Store in Cloud Memorystore (Redis)
   - D) Store in Application state object
   
   **Model Answer:** C (Cloud Memorystore/Redis)
   - Rationale: Sub-millisecond latency; replicated; survives instance failure; session affinity not needed
   - Cost: 1GB redis: ~£15/month
   - Alternative: B works but slower; D fails if instance dies
   
4. **Disaster Recovery Test:** How to verify RTO/RPO?
   - A) Kill one instance; measure failover time
   - B) Manually restore from backup; measure restore time
   - C) Perform monthly DR drill; simulate zone failure
   - D) Use disaster recovery plan only in emergency
   
   **Model Answer:** C (Monthly DR drill) + A (test failover)
   - Rationale: Monthly drills catch issues early; real incidents should not be first test
   - Simulate zone failure: Delete instance; verify traffic redirects to replica
   - Measure: Failover time (should be < 5 min) + session data recovery
   
5. **Cost Summary:**
   - Compute (MIG): £50/month
   - Database (Cloud SQL HA): £30/month
   - Redis: £15/month
   - LB: £5/month
   - **Total additional: £100/month** ✓ Under £500
   
   **Exam Tip:** Real exam questions: "Minimize RTO/RPO within budget" + "Explain tradeoffs" (cost vs availability)

---

## Question 4: Network Architecture & Security

**Scenario:**

Your startup runs a web API + mobile app backend. Requirements:
- API servers: Must be private (not exposed to internet)
- Mobile app: Calls API via HTTPS (secure)
- Database: Private (only API servers can access)
- Operations: Need to SSH to API servers for debugging

Your task: Design VPC architecture meeting all requirements.

**Sub-Questions:**

1. **VPC Design:** Which architecture?
   - A) All services in default VPC (public)
   - B) Custom VPC; public subnet (API), private subnet (DB)
   - C) Custom VPC; all services private; Cloud NAT for egress; load balancer for ingress
   - D) Multiple VPCs per service (complex)
   
   **Model Answer:** C (Custom VPC with load balancer + Cloud NAT)
   - Rationale: API servers private (no direct internet access); LB accepts ingress traffic; Cloud NAT handles outbound
   - Security benefit: No server exposed to internet; attack surface minimal
   
2. **Load Balancer Setup:** How to route traffic?
   ```
   Mobile App → HTTPS LB → API (private instances) → Cloud SQL (private)
   ```
   - A) Network LB (Layer 4)
   - B) HTTP(S) LB (Layer 7) with SSL offloading
   - C) Cloud Armor (WAF only)
   - D) VPC peering
   
   **Model Answer:** B (HTTP(S) LB with SSL offloading)
   - Rationale: Terminates HTTPS from mobile app; forwards to API instances (HTTP); TLS offloading reduces server CPU
   - SSL certificate: Google-managed (free) or custom (£0.20/cert/month)
   
3. **SSH Access:** How to debug private API servers?
   - A) Create public IP for each server (violates security)
   - B) Bastion host (public VM, SSH from there)
   - C) Cloud Shell + Identity-Aware Proxy (IAP)
   - D) VPN (complex setup)
   
   **Model Answer:** C (Identity-Aware Proxy)
   - Rationale: `gcloud compute ssh my-instance --tunnel-through-iap`; no bastion needed; role-based access control
   - Setup: Enable IAP; grant roles/compute.osLoginServiceAccountUser + roles/iam.serviceAccountUser
   
4. **Firewall Rules:** Protect database access.
   - Database rules should:
     - ✓ Allow traffic from API servers only
     - ✗ Deny all public traffic
   
   ```bash
   gcloud compute firewall-rules create allow-api-to-db \
     --network=my-vpc \
     --direction=INGRESS \
     --source-tags=api-server \
     --target-tags=database \
     --rules=tcp:5432
   
   gcloud compute firewall-rules create deny-all-ingress \
     --network=my-vpc \
     --direction=INGRESS \
     --action=DENY \
     --priority=1000 \
     --source-ranges=0.0.0.0/0
   ```
   
   **Model Answer:** Above rules (tag-based + deny-all-default)
   - Benefit: Explicit allow (source-tags); implicit deny for everything else
   
5. **Cost Breakdown:**
   - VPC: Free
   - Cloud NAT: ~£32/month + egress
   - HTTP(S) LB: ~£5/month
   - Firewall rules: Free
   - **Total: ~£40/month**
   
   **Exam Tip:** Know firewall rule priority (0–65534); lower = higher priority

---

## Question 5: Cost Optimization Challenge

**Scenario:**

Your current GCP bill: £1,500/month. CEO wants 30% cost reduction (target: £1,050/month).

Current setup:
- 10 Compute Engine e2-standard-4 instances (always on): £500/month
- Cloud SQL db-n1-highmem-8 instance: £600/month
- Cloud Storage (infrequent access): £200/month
- Data transfer (internet egress): £200/month

Your task: Recommend optimizations without sacrificing 99.9% SLA.

**Sub-Questions:**

1. **Compute Optimization:** Current cost £500/month for 10 VMs.
   - A) Downsize to e2-medium (1/4 CPU)
   - B) Use preemptible VMs (70% discount)
   - C) Switch to App Engine Standard (auto-scales)
   - D) Use GKE with multi-zone (auto-heal)
   
   **Model Answer:** B (Preemptible VMs) OR C (App Engine)
   - Rationale B: Preemptible VMs: ~£150/month (70% save) + 1 always-on instance (£50) = £200 total
     - Risk: 24-hour max lifetime; best for batch/non-critical
     - Suitable if workload: tolerates interruptions; can quickly restart
   - Rationale C: App Engine: Pay-per-use; if mostly idle, cost drops to £20–50/month
   - **Potential save: £300–350/month**
   
2. **Database Optimization:** Current db-n1-highmem-8: £600/month.
   - A) Downsize to db-f1-micro (50× cheaper: £15/month)
   - B) Enable automated backups (already done; saves manual backup labor)
   - C) Use BigQuery for analytics (separate from transactional DB)
   - D) Migrate to Firestore (auto-scales)
   
   **Model Answer:** C (BigQuery for analytics) + downsize transactional DB
   - Rationale: Separate OLTP (small Cloud SQL) from OLAP (BigQuery); n1-highmem suggests heavy analytics
   - New cost: db-f1-micro (£15) + BigQuery (pay-per-query, ~£50–100): ~£70–120 total
   - **Potential save: £500/month**
   
3. **Storage Optimization:** Current £200/month for infrequent access.
   - A) Enable lifecycle policies (auto-delete old data)
   - B) Switch to Coldline/Archive classes (cheaper for old data)
   - C) Use BigTable (cheaper at massive scale)
   - D) No savings possible
   
   **Model Answer:** A + B (Lifecycle + archive class)
   - Rationale: If data > 30 days old, auto-transition to Archive (60% cheaper)
   - Lifecycle example: `age > 30 days → Archive class`
   - Cost drop: £200 → £100/month
   - **Potential save: £100/month**
   
4. **Data Transfer Optimization:** Current £200/month internet egress.
   - A) Use Cloud NAT (consolidate egress): ~£35/month
   - B) Cache data closer (Cloud CDN): £0.085/GB
   - C) Use private Google API endpoints (no egress charges for Google services)
   - D) No savings possible
   
   **Model Answer:** C (Private API endpoints) + A (Cloud NAT if still needed)
   - Rationale: If egress = calls to Google services (Cloud Storage, BigQuery, APIs), use private endpoints (zero egress charge)
   - Cost drop: £200 → £50/month
   - **Potential save: £150/month**
   
5. **Total Savings:**
   - Compute: £300/month save
   - Database: £500/month save
   - Storage: £100/month save
   - Egress: £150/month save
   - **Total: £1,050/month** ✓ 30% reduction achieved
   
   **Exam Tip:** Real exam: "Reduce costs without SLA impact" + "Tradeoffs of each option"

---

## Question 6: Incident Response & Troubleshooting

**Scenario:**

Friday 5 PM: Your API starts returning 500 errors. Customers affected: 10% of traffic. Your on-call engineer is on vacation.

**Immediate Actions (first 10 minutes):**

1. **Detect the problem:** Where do you check first?
   - A) SSH to each VM (slow)
   - B) Cloud Error Reporting (automatic error dashboard)
   - C) Check Cloud Logging manually
   - D) Wait for monitoring alert
   
   **Model Answer:** B (Cloud Error Reporting) + monitoring alert (already triggered)
   - Cloud Error Reporting shows: "500 errors spike in last 2 minutes"
   - Root cause visible: "Out of memory exception in app.py line 42"
   
2. **Diagnosis:** Application memory leak suspected.
   - A) Restart all instances (quick fix; hides problem)
   - B) Scale down instances (saves cost; wrong direction)
   - C) Check Cloud Trace (performance profiling)
   - D) Check Cloud Debugger (set snapshot on line 42)
   
   **Model Answer:** D (Cloud Debugger) + examine logs
   - Set snapshot: `gcloud beta debug snapshots create --location app.py:42`
   - Inspect variables; identify leak cause
   - Alternative: C (Cloud Trace) shows slow requests but less detailed than Debugger
   
3. **Immediate Mitigation (Restore Service):**
   - A) Restart instances (buys time for diagnosis)
   - B) Increase instance size (vertical scale; costs more)
   - C) Add instances via MIG (horizontal scale)
   - D) Roll back last deployment
   
   **Model Answer:** A (restart) OR C (scale up MIG) + investigate root cause
   - Restart: ~2 min; 95% uptime restored temporarily
   - Scale MIG: +1 instance (adds capacity while investigating)
   - Combined: Restart + scale = immediate relief + capacity breathing room
   
4. **Root Cause Analysis:**
   - Check: Git log; see last deploy 1 hour ago introduced recursive function call
   - Fix: Revert recursive call to iterative (memory-efficient)
   - Test: Deploy to canary (1 instance); verify 30 min; if OK, roll out to all
   
   **Model Answer:** Rollback deployment + canary deploy new fix
   - RTO: 5 min (restart) + 10 min (rollback) = 15 min total downtime
   - RPO: ~0 (stateless API; no data loss during restart)
   
5. **Post-Incident (Blameless Postmortem):**
   - A) Blame engineer; dock pay
   - B) Conduct blameless postmortem; identify process gaps
   - C) Add monitoring alert for memory usage
   - D) Increase on-call rotation
   
   **Model Answer:** B + C + D
   - Postmortem: Why didn't memory tests catch leak? Why no alert on memory?
   - Add: Memory threshold alert (>80% instance memory trigger page)
   - Implement: Pre-deployment load test; memory profiling in CI/CD
   - Rotation: Spread on-call so no single point of failure

---

## Scoring Rubric

Each question: 5 parts × 20 points = 100 points per question

**Scoring by Question:**

- **Q1 (Multi-Tier App):** Compute (20), Database (20), Background Jobs (20), Network (20), Cost (20) = 100 points
- **Q2 (Database Selection):** Use Case A (20), Use Case B (20), Use Case C (20), Cost Estimate (20), Tradeoffs (20) = 100 points
- **Q3 (HA/DR):** Compute HA (20), Data HA (20), State Management (20), DR Testing (20), Cost (20) = 100 points
- **Q4 (Network):** VPC Design (20), Load Balancer (20), SSH Access (20), Firewall (20), Cost (20) = 100 points
- **Q5 (Cost Optimization):** Compute (20), Database (20), Storage (20), Transfer (20), Total Savings (20) = 100 points
- **Q6 (Incident Response):** Detection (20), Diagnosis (20), Mitigation (20), Root Cause (20), Post-Incident (20) = 100 points

**Total: 600 points (Full practice exam)**

**Passing Threshold:** 70% = 420 points

---

## Real Exam Tips

- **Time Management:** 6 questions × 3 hours = 30 min per question
- **Format:** Multiple-choice + scenario-based (this practice exam mirrors real format)
- **Focus Areas:** Compute (30%), Networking (25%), Storage/Databases (20%), Security (15%), Cost (10%)
- **Weak Areas:** Review any question scoring < 70 points; study that domain deeper

---

## Links

- [Cloud Error Reporting](https://cloud.google.com/error-reporting/docs)
- [Cloud Trace](https://cloud.google.com/trace/docs)
- [Cloud Debugger](https://cloud.google.com/debugger/docs)
- [ACE Exam Overview](https://cloud.google.com/certification/cloud-engineer)