"""Basic environment setup for Vertex AI SDK.

Run this from a local machine or Cloud Shell after configuring gcloud.

Expected output:
- Prints the active project and region.
- Confirms Vertex AI initialisation.
"""

import os

from google.cloud import aiplatform


def init_vertex_ai(project_id: str, region: str = "europe-west2") -> None:
    """Initialise Vertex AI with the given project and region.

    Args:
        project_id: Google Cloud project identifier.
        region: Default region for Vertex AI resources.
    """

    aiplatform.init(project=project_id, location=region)
    print(f"Vertex AI initialised for project={project_id}, region={region}")


if __name__ == "__main__":
    gcp_project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    gcp_region = os.environ.get("VERTEX_REGION", "europe-west2")
    init_vertex_ai(gcp_project, gcp_region)
