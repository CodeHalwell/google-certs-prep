"""Example: Deploy a Vertex AI model to an endpoint for online prediction."""

from google.cloud import aiplatform


def deploy_model_to_endpoint(
    project_id: str,
    region: str,
    model_id: str,
    display_name: str,
) -> aiplatform.Endpoint:
    aiplatform.init(project=project_id, location=region)
    model = aiplatform.Model(model_id)
    endpoint = model.deploy(
        traffic_split={"0": 100},
        deployed_model_display_name=display_name,
        machine_type="n1-standard-4",
    )
    print(f"Model deployed to endpoint: {endpoint.resource_name}")
    return endpoint


if __name__ == "__main__":
    deploy_model_to_endpoint(
        project_id="your-project-id",
        region="europe-west2",
        model_id="projects/123/locations/europe-west2/models/789",
        display_name="pmle-endpoint-demo",
    )
