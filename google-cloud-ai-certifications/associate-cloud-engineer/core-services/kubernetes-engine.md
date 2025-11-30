# Kubernetes Engine – Associate Cloud Engineer

_Last Updated: November 30, 2025_

## Overview

Google Kubernetes Engine (GKE) provides managed Kubernetes clusters. Container orchestration for deploying & scaling microservices. 8–12% of ACE exam.

---

## Key Concepts

### Kubernetes Basics
- **Pod:** Smallest deployable unit (usually 1 container)
- **Deployment:** Manages pods (replicas, rolling updates)
- **Service:** Exposes pods (load balancing, DNS)
- **Namespace:** Logical isolation within cluster

### GKE vs DIY Kubernetes
| Aspect | GKE (Managed) | DIY on GCE |
|--------|-------------|----------|
| Master management | Google handles | You manage |
| Upgrades | Automatic | Manual |
| Cost | Higher (convenience) | Lower (but effort) |
| Security | Built-in | Your responsibility |

---

## Creating a GKE Cluster

```bash
# Create cluster (3 nodes, n1-standard-1)
gcloud container clusters create my-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-1

# Connect to cluster
gcloud container clusters get-credentials my-cluster --zone us-central1-a

# Verify
kubectl cluster-info
kubectl get nodes

# Scale cluster (add 2 more nodes)
gcloud container clusters resize my-cluster --num-nodes 5 --zone us-central1-a
```

### Cluster Features
- **Autoscaling:** Add nodes when pods pending
- **Network policy:** Control traffic between pods
- **RBAC:** Role-based access control
- **Monitoring:** Integrated with Cloud Logging & Monitoring

---

## Deploying Applications

### Simple Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: app
        image: gcr.io/my-project/my-app:v1
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

```bash
# Deploy
kubectl apply -f deployment.yaml

# Monitor rollout
kubectl rollout status deployment/my-app

# Update image (rolling update)
kubectl set image deployment/my-app app=gcr.io/my-project/my-app:v2

# Scale manually
kubectl scale deployment/my-app --replicas 5
```

---

## Services & Load Balancing

### Service Types
| Type | Use Case | Cost |
|------|----------|------|
| ClusterIP | Internal only | Free |
| NodePort | External via node port (31000+) | Free |
| LoadBalancer | External via GCP LB | £13/month per service |
| Ingress | HTTP/HTTPS, advanced routing | £13/month |

```bash
# Expose via LoadBalancer
kubectl expose deployment my-app \
  --type LoadBalancer \
  --port 80 \
  --target-port 8080

# Get external IP
kubectl get service my-app
# Example output: EXTERNAL-IP 35.1.2.3

# Access
curl http://35.1.2.3
```

---

## Common ACE Exam Questions

**Q1:** Cluster in zone us-central1-a fails (hardware). Impact?
- A) All pods lost (single zone risk)
- B) Workload migrates automatically
- C) Manual recreate needed
- D) No impact (GKE handles)

**Answer:** A. Single-zone clusters vulnerable to zone outage. Solution: regional cluster (3 zones, automatic failover).

```bash
# Create regional cluster (recommended)
gcloud container clusters create my-cluster \
  --region us-central1 \
  --num-nodes 1  # per zone = 3 total
```

**Q2:** Pod crashing repeatedly (CrashLoopBackOff). How to debug?
- A) kubectl describe pod <pod-name>
- B) kubectl logs <pod-name>
- C) kubectl exec to shell into container
- D) All of above

**Answer:** D. describe = metadata/events; logs = application output; exec = interactive debugging.

**Q3:** Roll back bad deployment to previous version. Command?
- A) kubectl rollout undo deployment/my-app
- B) kubectl apply -f old-deployment.yaml
- C) kubectl rollout history deployment/my-app
- D) A or B (both work)

**Answer:** D. A = native rollback; B = explicit re-apply. A preferred (tracks history).

---

## Cost Optimisation

- Use regional clusters (high availability, minimal extra cost)
- Enable autoscaling (scale nodes when pods pending)
- Use preemptible nodes (70% savings, acceptable for non-critical)
- Resource requests/limits (prevent oversizing)

---

## GKE Best Practices

| Practice | Benefit | Effort |
|----------|---------|--------|
| Resource requests/limits | Efficient scheduling | Low |
| Health checks (readiness/liveness) | Auto-restart crashed pods | Low |
| Namespaces | Multi-tenant isolation | Low |
| Network policies | Restrict inter-pod traffic | Medium |
| RBAC | Access control | Medium |
| Regional cluster | High availability | High (but recommended) |

---

## Links

- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [Kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)