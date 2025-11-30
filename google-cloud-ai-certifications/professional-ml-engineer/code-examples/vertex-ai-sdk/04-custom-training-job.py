"""Example: Submit a custom training job to Vertex AI.

Assumes you have a Docker image with training code pushed to Artifact Registry.
"""

from google.cloud import aiplatform


def launch_custom_training_job(
    project_id: str,
    region: str,
    display_name: str,
    image_uri: str,
    args: list[str] | None = None,
) -> aiplatform.CustomJob:
    aiplatform.init(project=project_id, location=region)
    job = aiplatform.CustomJob(
        display_name=display_name,
        worker_pool_specs=[
            {
                "machine_spec": {"machine_type": "n1-standard-4"},
                "replica_count": 1,
                "container_spec": {
                    "image_uri": image_uri,
                    "args": args or [],
                },
            }
        ],
    )
    job.run(sync=True)
    print(f"Custom training job finished: {job.resource_name}")
    return job


if __name__ == "__main__":
    launch_custom_training_job(
        project_id="your-project-id",
        region="europe-west2",
        display_name="pmle-custom-training-demo",
        image_uri="europe-west2-docker.pkg.dev/your-project-id/ml/train-image:latest",
        args=["--epochs=5", "--batch_size=64"],
    )
