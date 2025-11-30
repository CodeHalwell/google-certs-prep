# ACE Hands-On Labs

_Last Updated: November 30, 2025_

Practical exercises for core ACE services. Labs assume: GCP project, gcloud CLI, basic Linux/Docker knowledge.

---

## Lab 1: Deploy Web Server on Compute Engine

**Scenario:** Deploy 3-tier Flask web app on Compute Engine (frontend on VM, storage on Cloud Storage, database on Cloud SQL).

**Prerequisites:**
- GCP project with billing enabled
- gcloud CLI installed
- SSH key pair generated

**Steps:**

1. **Create VM instance**
   ```bash
   gcloud compute instances create web-server \
     --machine-type=e2-medium \
     --zone=us-central1-a \
     --image-family=debian-12 \
     --image-project=debian-cloud \
     --metadata-from-file startup-script=startup.sh
   ```

2. **Create startup script** (`startup.sh`)
   ```bash
   #!/bin/bash
   apt-get update
   apt-get install -y python3 python3-pip
   pip3 install flask google-cloud-storage
   
   cat > app.py << 'EOF'
   from flask import Flask, jsonify
   from google.cloud import storage
   
   app = Flask(__name__)
   storage_client = storage.Client()
   
   @app.route('/health', methods=['GET'])
   def health():
       return jsonify({"status": "healthy"}), 200
   
   @app.route('/files', methods=['GET'])
   def list_files():
       bucket = storage_client.bucket('my-bucket')
       return jsonify({"files": [blob.name for blob in bucket.list_blobs()]})
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   EOF
   
   python3 app.py &
   ```

3. **Allow firewall traffic**
   ```bash
   gcloud compute firewall-rules create allow-http \
     --allow=tcp:5000 \
     --source-ranges=0.0.0.0/0
   ```

4. **Get external IP**
   ```bash
   gcloud compute instances describe web-server \
     --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
   ```

**Validation:**
```bash
curl http://<EXTERNAL_IP>:5000/health
# Expected: {"status": "healthy"}
```

**Cleanup:**
```bash
gcloud compute instances delete web-server --zone=us-central1-a
gcloud compute firewall-rules delete allow-http
```

**Exam Tips:**
- Distinguish between instance-level (startup script) and network-level (firewall) configuration
- Cost: e2-medium ~£25/month; storage ~£0.02/GB; typical bill: £40–50/month
- Know when to use Compute Engine vs App Engine vs Cloud Run

---

## Lab 2: Deploy Multi-Tier App on GKE

**Scenario:** Deploy containerised Flask frontend + Redis cache on Kubernetes.

**Prerequisites:**
- Docker installed
- GKE cluster created: `gcloud container clusters create my-cluster --zone=us-central1-a`

**Steps:**

1. **Create Dockerfile** (Flask app)
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY app.py .
   CMD ["python", "app.py"]
   ```

2. **Create requirements.txt**
   ```
   Flask==2.3.0
   redis==4.5.0
   google-cloud-storage==2.7.0
   ```

3. **Build and push image**
   ```bash
   docker build -t gcr.io/PROJECT_ID/web-app:v1 .
   docker push gcr.io/PROJECT_ID/web-app:v1
   ```

4. **Create Kubernetes deployment**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: web-app
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: web-app
     template:
       metadata:
         labels:
           app: web-app
       spec:
         containers:
         - name: app
           image: gcr.io/PROJECT_ID/web-app:v1
           ports:
           - containerPort: 5000
           resources:
             requests:
               memory: "256Mi"
               cpu: "250m"
             limits:
               memory: "512Mi"
               cpu: "500m"
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: web-app-service
   spec:
     type: LoadBalancer
     ports:
     - port: 80
       targetPort: 5000
     selector:
       app: web-app
   ```

5. **Deploy to GKE**
   ```bash
   kubectl apply -f deployment.yaml
   kubectl get svc web-app-service
   # Wait for EXTERNAL-IP
   curl http://<EXTERNAL_IP>/health
   ```

**Validation:**
```bash
kubectl logs -l app=web-app | head -20
kubectl describe svc web-app-service
```

**Cleanup:**
```bash
kubectl delete -f deployment.yaml
gcloud container clusters delete my-cluster --zone=us-central1-a
```

**Exam Tips:**
- GKE: ~3 nodes × £50 = £150/month minimum
- Know: Deployment (spec) → ReplicaSet (enforces replicas) → Pod (runs container)
- Load Balancer vs ClusterIP vs NodePort service types

---

## Lab 3: Deploy App on App Engine

**Scenario:** Deploy Flask app using App Engine Standard (auto-scales to zero).

**Prerequisites:**
- gcloud CLI configured
- App Engine API enabled

**Steps:**

1. **Create Flask app** (`main.py`)
   ```python
   from flask import Flask, jsonify
   import os
   
   app = Flask(__name__)
   
   @app.route('/', methods=['GET'])
   def index():
       return jsonify({"message": "Hello from App Engine", "env": os.environ.get('GAE_ENV')})
   
   if __name__ == '__main__':
       app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 8080)))
   ```

2. **Create requirements.txt**
   ```
   Flask==2.3.0
   Werkzeug==2.3.0
   ```

3. **Create app.yaml** (App Engine config)
   ```yaml
   runtime: python311
   
   env: standard
   
   entrypoint: gunicorn -b :$PORT main:app
   
   handlers:
   - url: /.*
     script: auto
   
   automatic_scaling:
     max_instances: 10
     min_instances: 0
   ```

4. **Deploy**
   ```bash
   gcloud app deploy
   gcloud app browse
   ```

**Validation:**
```bash
gcloud app logs read
# Expected: Flask app serving requests
```

**Cleanup:**
```bash
gcloud app versions delete [VERSION_ID]
```

**Exam Tips:**
- App Engine: £0.05/hour instance time; scales to zero (no cost when idle)
- Suitable for: Web apps, APIs, background jobs
- NOT suitable: Long-running tasks, batch processing (use Compute Engine or Cloud Run)

---

## Lab 4: Trigger Cloud Function via Pub/Sub

**Scenario:** Publish message to Pub/Sub topic; Cloud Function processes and writes to Cloud Storage.

**Prerequisites:**
- Cloud Functions API enabled
- Pub/Sub API enabled

**Steps:**

1. **Create Pub/Sub topic**
   ```bash
   gcloud pubsub topics create my-topic
   gcloud pubsub subscriptions create my-subscription --topic=my-topic
   ```

2. **Create Cloud Function** (`main.py`)
   ```python
   import functions_framework
   import json
   from google.cloud import storage
   
   @functions_framework.cloud_event
   def process_message(cloud_event):
       pubsub_message = base64.b64decode(cloud_event.data["message"]["data"])
       message_data = json.loads(pubsub_message)
       
       # Write to Cloud Storage
       client = storage.Client()
       bucket = client.bucket('my-bucket')
       blob = bucket.blob(f"messages/{message_data['id']}.json")
       blob.upload_from_string(json.dumps(message_data))
       
       return f"Processed: {message_data['id']}"
   ```

3. **Create requirements.txt**
   ```
   google-cloud-storage==2.7.0
   functions-framework==3.0.0
   ```

4. **Deploy function**
   ```bash
   gcloud functions deploy process_message \
     --runtime python311 \
     --trigger-topic my-topic \
     --entry-point process_message
   ```

5. **Publish message**
   ```bash
   gcloud pubsub topics publish my-topic \
     --message='{"id": "msg-001", "payload": "test"}'
   ```

**Validation:**
```bash
gcloud functions logs read process_message --limit 20
gcloud storage ls gs://my-bucket/messages/
```

**Cleanup:**
```bash
gcloud functions delete process_message
gcloud pubsub subscriptions delete my-subscription
gcloud pubsub topics delete my-topic
```

**Exam Tips:**
- Cloud Functions Gen 2: 90-second timeout (up from 60s in Gen 1)
- Cost: £0.40 per 1M requests; typical: £1–5/month for low-volume apps
- When to use: Event-driven tasks, webhooks, lightweight ETL

---

## Lab 5: Create Cloud SQL Database & Connect App

**Scenario:** Create managed PostgreSQL instance; deploy app that queries database.

**Prerequisites:**
- Cloud SQL API enabled
- Compute Engine VM (from Lab 1) or use Cloud Shell

**Steps:**

1. **Create Cloud SQL instance**
   ```bash
   gcloud sql instances create my-db \
     --database-version=POSTGRES_15 \
     --tier=db-f1-micro \
     --region=us-central1 \
     --availability-type=REGIONAL
   ```

2. **Create database & user**
   ```bash
   gcloud sql databases create my_app_db --instance=my-db
   gcloud sql users create app_user \
     --instance=my-db \
     --password=YOUR_PASSWORD
   ```

3. **Create table**
   ```bash
   gcloud sql connect my-db --user=postgres
   # In psql prompt:
   CREATE TABLE IF NOT EXISTS users (
       id SERIAL PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       created_at TIMESTAMP DEFAULT NOW()
   );
   \q
   ```

4. **Connect from app** (Python)
   ```python
   import psycopg2
   
   conn = psycopg2.connect(
       host="CLOUD_SQL_IP",  # Get via: gcloud sql instances describe my-db
       user="app_user",
       password="YOUR_PASSWORD",
       database="my_app_db"
   )
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM users LIMIT 5")
   print(cursor.fetchall())
   cursor.close()
   ```

5. **Enable Public IP & authorise VM**
   ```bash
   gcloud sql instances patch my-db --assign-ip
   CLOUD_SQL_IP=$(gcloud sql instances describe my-db --format='get(ipAddresses[0].ipAddress)')
   
   VM_IP=$(gcloud compute instances describe web-server --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
   
   gcloud sql instances patch my-db \
     --allowed-networks=$VM_IP/32
   ```

**Validation:**
```bash
gcloud sql instances describe my-db
# Check: IP address assigned, backup window set, HA status
```

**Cleanup:**
```bash
gcloud sql instances delete my-db
```

**Exam Tips:**
- Cost: db-f1-micro £25/month; regional HA adds ~20% cost
- Always use Private IP (via VPC connector) for production; Public IP is test-only
- Know: Automatic backups, PITR (point-in-time recovery), automated failover
- Diff: Cloud SQL (managed RDBMS) vs Firestore (serverless document DB) vs Bigtable (massive scale)

---

## Lab 6: Configure VPC, Firewall & Cloud NAT

**Scenario:** Create custom VPC; create private subnet; route egress traffic via Cloud NAT.

**Prerequisites:**
- gcloud CLI

**Steps:**

1. **Create custom VPC**
   ```bash
   gcloud compute networks create my-vpc \
     --subnet-mode=custom
   
   gcloud compute networks subnets create my-subnet \
     --network=my-vpc \
     --region=us-central1 \
     --range=10.0.0.0/24
   ```

2. **Create deny-all firewall rule (default deny)**
   ```bash
   gcloud compute firewall-rules create deny-all-ingress \
     --network=my-vpc \
     --direction=INGRESS \
     --action=DENY \
     --priority=1000 \
     --source-ranges=0.0.0.0/0
   ```

3. **Allow SSH (for testing)**
   ```bash
   gcloud compute firewall-rules create allow-ssh \
     --network=my-vpc \
     --direction=INGRESS \
     --action=ALLOW \
     --priority=100 \
     --source-ranges=203.0.113.0/24 \
     --rules=tcp:22
   ```

4. **Create private VM (no external IP)**
   ```bash
   gcloud compute instances create private-vm \
     --network-interface=network=my-vpc,subnet=my-subnet,no-address \
     --zone=us-central1-a \
     --image-family=debian-12
   ```

5. **Create Cloud NAT (for egress)**
   ```bash
   gcloud compute routers create nat-router \
     --network=my-vpc \
     --region=us-central1
   
   gcloud compute routers nats create nat-config \
     --router=nat-router \
     --region=us-central1 \
     --nat-all-subnet-ip-ranges \
     --auto-allocate-nat-external-ips
   ```

6. **Verify private VM can reach internet**
   ```bash
   gcloud compute ssh private-vm --zone=us-central1-a --tunnel-through-iap
   # Inside VM:
   curl https://www.google.com -I
   # Expected: HTTP 200 (via Cloud NAT)
   exit
   ```

**Validation:**
```bash
gcloud compute firewall-rules list --filter="network:my-vpc"
gcloud compute routers describe nat-router --region=us-central1
```

**Cleanup:**
```bash
gcloud compute instances delete private-vm --zone=us-central1-a
gcloud compute routers nats delete nat-config --router=nat-router --region=us-central1
gcloud compute routers delete nat-router --region=us-central1
gcloud compute firewall-rules delete allow-ssh deny-all-ingress
gcloud compute networks subnets delete my-subnet --region=us-central1
gcloud compute networks delete my-vpc
```

**Exam Tips:**
- VPC: Custom subnets allow fine-grained IP allocation (avoid large auto subnets in prod)
- Firewall: Default deny + allow-by-need pattern is security best practice
- Cloud NAT: Required if private VMs need internet access (e.g., apt-get, pip install)
- Cost: Cloud NAT: ~£32/month + £0.045/GB egress; VPC: free

---

## Exam Focus

Each lab tests 2–3 core ACE competencies:
- **Lab 1:** Compute Engine, firewall, storage basics
- **Lab 2:** GKE deployment, services, load balancing
- **Lab 3:** App Engine deployment, scaling, runtimes
- **Lab 4:** Cloud Functions, Pub/Sub event-driven architecture
- **Lab 5:** Cloud SQL, database connectivity, HA setup
- **Lab 6:** VPC, network isolation, Cloud NAT

Common exam questions: "Which service for [scenario]?" + "What's the cost?" + "How to secure this?"

---

## Links

- [Compute Engine Labs](https://cloud.google.com/compute/docs/tutorials)
- [GKE Labs](https://cloud.google.com/kubernetes-engine/docs/tutorials)
- [App Engine Labs](https://cloud.google.com/appengine/docs/standard/python3)
- [Cloud Functions Labs](https://cloud.google.com/functions/docs/tutorials)
- [Cloud SQL Labs](https://cloud.google.com/sql/docs/postgres/quickstart)
- [VPC Labs](https://cloud.google.com/vpc/docs/tutorials)