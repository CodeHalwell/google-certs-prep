# Firewall & Cloud Armor – ACE

_Last Updated: November 30, 2025_

## Firewall Rules

Control traffic between resources.

### Rule Components
```bash
Name: allow-http
Direction: INGRESS (inbound)
Priority: 1000
Network: default
Source IP: 0.0.0.0/0 (anywhere)
Destination IP: N/A (applies to all resources)
Protocol: tcp
Port: 80
Action: ALLOW
```

### Creating Rules

```bash
# Allow HTTP from anywhere
gcloud compute firewall-rules create allow-http \
  --network my-vpc \
  --allow tcp:80,tcp:443 \
  --source-ranges 0.0.0.0/0

# Deny SSH except from office
gcloud compute firewall-rules create deny-ssh-external \
  --network my-vpc \
  --deny tcp:22 \
  --source-ranges 0.0.0.0/0 \
  --priority 900

gcloud compute firewall-rules create allow-ssh-office \
  --network my-vpc \
  --allow tcp:22 \
  --source-ranges 203.0.113.0/24 \
  --priority 800
```

### Firewall Best Practices
- Default deny, explicit allow
- Lower priority = evaluated first
- Use service accounts + network tags (more flexible than CIDR)
- Audit rules quarterly

---

## Cloud Armor (WAF + DDoS)

Web Application Firewall. Protect cloud load balancers from attacks.

```bash
# Create Cloud Armor policy
gcloud compute security-policies create my-policy

# Add rule: Block SQL injection attempts
gcloud compute security-policies rules create 100 \
  --security-policy my-policy \
  --action deny-403 \
  --expression 'evaluatePreconfiguredExpr("sqli-stable")'

# Add rule: Block high request rate (DDoS)
gcloud compute security-policies rules create 200 \
  --security-policy my-policy \
  --action rate-based-ban \
  --rate-limit-options enforce-on-key=IP banning-duration-sec=600 \
  --enforce-on-key IP \
  --ban-duration-sec 600 \
  --rate-limit-threshold-count 100 \
  --rate-limit-threshold-interval-sec 60

# Attach to load balancer
gcloud compute backend-services update my-backend \
  --security-policy my-policy
```

---

## Load Balancing

### Types
| Type | Use | Cost |
|------|-----|------|
| Network Load Balancer (NLB) | Ultra-high throughput | ~£0.10/hour |
| HTTP(S) LB | Web apps, API | ~£0.10/hour |
| Internal LB | Private services | Free (traffic charges apply) |

```bash
# Create HTTP LB
gcloud compute load-balancers create my-lb \
  --type HTTP \
  --region us-central1

# Create backend service
gcloud compute backend-services create my-backend \
  --protocol HTTP \
  --global

# Add instances to backend
gcloud compute backend-services add-backends my-backend \
  --instance-group my-instance-group \
  --instance-group-zone us-central1-a
```

---

## Common ACE Questions

**Q1:** Block traffic from malicious IPs (DDoS attempt). Approach?
- A) Firewall rule (blocks all DDoS)
- B) Cloud Armor (application-level filtering)
- C) Both (firewall + Armor layered defense)
- D) Network LB (traffic absorption)

**Answer:** C. Firewall filters L4 (IP/port); Armor filters L7 (application layer). Both needed.

**Q2:** Web app under DDoS attack. Recovery?
- A) Increase instance count (absorbs traffic)
- B) Enable Cloud Armor rate-limiting
- C) Both
- D) Move to static content

**Answer:** C. Armor blocks attackers; scaling helps legitimate traffic.

---

## Links

- [Firewall Rules](https://cloud.google.com/vpc/docs/firewalls)
- [Cloud Armor Documentation](https://cloud.google.com/armor/docs)