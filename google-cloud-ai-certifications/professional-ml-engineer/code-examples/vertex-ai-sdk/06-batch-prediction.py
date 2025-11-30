"""Example: Run a batch prediction job on Vertex AI."""

from google.cloud import aiplatform


def run_batch_prediction(
    project_id: str,
    region: str,
    model_id: str,
    job_display_name: str,
    gcs_source_uri: str,
    gcs_destination_output_uri_prefix: str,
) -> aiplatform.BatchPredictionJob:
    aiplatform.init(project=project_id, location=region)
    model = aiplatform.Model(model_id)
    batch_job = model.batch_predict(
        job_display_name=job_display_name,
        gcs_source=gcs_source_uri,
        gcs_destination_prefix=gcs_destination_output_uri_prefix,
        sync=True,
    )
    print(f"Batch prediction job: {batch_job.resource_name}")
    return batch_job


if __name__ == "__main__":
    run_batch_prediction(
        project_id="your-project-id",
        region="europe-west2",
        model_id="projects/123/locations/europe-west2/models/789",
        job_display_name="pmle-batch-prediction-demo",
        gcs_source_uri="gs://your-bucket/batch/input.jsonl",
        gcs_destination_output_uri_prefix="gs://your-bucket/batch/output/",
    )
