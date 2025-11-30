"""Skeleton: Configure basic Vertex AI model monitoring for an endpoint."""

from google.cloud import aiplatform


def enable_model_monitoring(
    project_id: str,
    region: str,
    endpoint_id: str,
) -> None:
    aiplatform.init(project=project_id, location=region)
    endpoint = aiplatform.Endpoint(endpoint_id)
    # Placeholder for monitoring configuration; refer to Vertex AI docs for full options.
    print(f"Model monitoring should be configured for endpoint: {endpoint.resource_name}")


if __name__ == "__main__":
    enable_model_monitoring(
        project_id="your-project-id",
        region="europe-west2",
        endpoint_id="projects/123/locations/europe-west2/endpoints/999",
    )
