"""Example: Launch an AutoML tabular training job on Vertex AI.

This script assumes a target column in your dataset and uses a basic
AutoML configuration suitable for PMLE practice.
"""

from google.cloud import aiplatform


def run_automl_training(
    project_id: str,
    region: str,
    display_name: str,
    dataset_id: str,
    target_column: str,
) -> aiplatform.Model:
    aiplatform.init(project=project_id, location=region)
    dataset = aiplatform.TabularDataset(dataset_id)

    job = aiplatform.AutoMLTabularTrainingJob(
        display_name=display_name,
        optimization_prediction_type="regression",
        target_column=target_column,
    )

    model = job.run(dataset=dataset, model_display_name=f"{display_name}-model")
    print(f"Training complete. Model resource: {model.resource_name}")
    return model


if __name__ == "__main__":
    run_automl_training(
        project_id="your-project-id",
        region="europe-west2",
        display_name="pmle-automl-demo",
        dataset_id="projects/123/locations/europe-west2/datasets/456",
        target_column="label",
    )
