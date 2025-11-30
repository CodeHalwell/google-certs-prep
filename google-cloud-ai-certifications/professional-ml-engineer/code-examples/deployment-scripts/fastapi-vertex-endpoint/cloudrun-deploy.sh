#!/usr/bin/env bash

set -euo pipefail

SERVICE_NAME="pmle-fastapi-vertex"
REGION="europe-west2"
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-your-project-id}"

gcloud builds submit --tag "europe-west2-docker.pkg.dev/${PROJECT_ID}/services/${SERVICE_NAME}:latest"

gcloud run deploy "${SERVICE_NAME}" \
  --image="europe-west2-docker.pkg.dev/${PROJECT_ID}/services/${SERVICE_NAME}:latest" \
  --region="${REGION}" \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" \
  --set-env-vars "VERTEX_REGION=${REGION}" \
  --set-env-vars "VERTEX_ENDPOINT_ID=projects/123/locations/${REGION}/endpoints/999"
