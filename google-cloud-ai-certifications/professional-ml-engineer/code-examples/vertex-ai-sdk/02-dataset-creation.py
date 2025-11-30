"""Example: Create a Vertex AI tabular dataset from Cloud Storage.

Prerequisites:
- A CSV file in a Cloud Storage bucket (e.g. gs://your-bucket/data/train.csv).
- The first row contains headers.

Expected output:
- Prints the created dataset resource name.
"""

from google.cloud import aiplatform


def create_tabular_dataset(
    project_id: str,
    region: str,
    display_name: str,
    gcs_uri: str,
) -> aiplatform.TabularDataset:
    aiplatform.init(project=project_id, location=region)
    dataset = aiplatform.TabularDataset.create(
        display_name=display_name,
        gcs_source=[gcs_uri],
    )
    print(f"Created dataset: {dataset.resource_name}")
    return dataset


if __name__ == "__main__":
    create_tabular_dataset(
        project_id="your-project-id",
        region="europe-west2",
        display_name="pmle-tabular-demo",
        gcs_uri="gs://your-bucket/data/train.csv",
    )
