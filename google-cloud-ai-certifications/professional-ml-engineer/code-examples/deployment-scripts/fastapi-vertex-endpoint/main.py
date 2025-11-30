"""FastAPI service that forwards requests to a Vertex AI endpoint.

Intended for deployment to Cloud Run as a lightweight inference gateway.
"""

import os
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import aiplatform


PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
REGION = os.environ.get("VERTEX_REGION", "europe-west2")
ENDPOINT_ID = os.environ.get("VERTEX_ENDPOINT_ID", "projects/123/locations/europe-west2/endpoints/999")


class PredictionRequest(BaseModel):
    instances: list[Dict[str, Any]]


app = FastAPI(title="PMLE FastAPI → Vertex AI Gateway")


@app.on_event("startup")
def _startup() -> None:
    aiplatform.init(project=PROJECT_ID, location=REGION)


@app.post("/predict")
def predict(request: PredictionRequest) -> Dict[str, Any]:
    try:
        endpoint = aiplatform.Endpoint(ENDPOINT_ID)
        prediction = endpoint.predict(instances=request.instances)
        return {"predictions": prediction.predictions}
    except Exception as exc:  # pragma: no cover - runtime error path
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok"}
