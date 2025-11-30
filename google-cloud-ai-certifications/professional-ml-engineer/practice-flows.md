# Practice Flows – Professional ML Engineer

_Last Updated: November 30, 2025_

Use this guide to connect the code examples and notebook in this folder to specific exam domains and hands-on practice.

## Flow 1 – AutoML Tabular E2E (Frame, Architect, Develop, Deploy)

- [ ] Read: `learning-paths/01-ml-on-gcp.md`
- [ ] Run notebook: `pmle-end-to-end.ipynb`
  - Create a tabular dataset from Cloud Storage
  - Launch an AutoML training job
  - Deploy to an endpoint
  - Send a test prediction

**Domains:**
- Frame ML problems
- Architect ML solutions
- Design data preparation and processing systems
- Develop ML models
- Automate/orchestrate (if you later wrap this in a pipeline)
- Monitor/maintain (extend with logging/monitoring)

## Flow 2 – Custom Training + Deployment Scripts

- [ ] Study: `learning-paths/02-vertex-ai.md` and `03-tensorflow-keras.md`
- [ ] Use examples in `code-examples/tensorflow-examples/` to build a small Keras model.
- [ ] Containerise training or inference code and submit a custom job using:
  - `code-examples/vertex-ai-sdk/04-custom-training-job.py`
- [ ] Deploy the resulting model with:
  - `code-examples/vertex-ai-sdk/05-model-deployment.py`

**Domains:**
- Develop ML models
- Architect ML solutions
- Automate and orchestrate ML pipelines

## Flow 3 – FastAPI + Cloud Run Inference Gateway

- [ ] Build and deploy the FastAPI service:
  - `code-examples/deployment-scripts/fastapi-vertex-endpoint/`
- [ ] Wire it up to a Vertex AI endpoint and test `/predict` locally and on Cloud Run.

**Domains:**
- Architect ML solutions (serving patterns)
- Deploy and operate ML systems in production
- Monitor, optimise, and maintain ML solutions (extend with logging and monitoring)

## Flow 4 – Pipelines and MLOps

- [ ] Study: `learning-paths/04-mlops-deployment.md`
- [ ] Compile and inspect the pipeline skeleton:
  - `code-examples/vertex-ai-sdk/07-pipeline-creation.py`
- [ ] Gradually expand it into a full pipeline that:
  - Ingests data
  - Trains a model
  - Evaluates and possibly deploys

**Domains:**
- Automate and orchestrate ML pipelines
- Monitor, optimise, and maintain ML solutions

Tick off flows as you complete them and adapt them to your own healthcare and consultancy scenarios.
