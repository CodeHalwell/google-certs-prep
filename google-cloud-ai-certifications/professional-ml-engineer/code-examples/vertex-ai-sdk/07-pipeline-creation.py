"""Skeleton: Create and compile a simple Vertex AI Pipeline.

This focuses on structure rather than a full pipeline implementation.
"""

from kfp import dsl
from google_cloud_pipeline_components import aiplatform as gcc_aip


@dsl.pipeline(name="pmle-demo-pipeline")
def demo_pipeline(project_id: str, location: str) -> None:
    gcc_aip.TabularDatasetCreateOp(
        project=project_id,
        display_name="pmle-pipeline-dataset",
        gcs_source="gs://your-bucket/data/train.csv",
        location=location,
    )


if __name__ == "__main__":
    from kfp import compiler

    compiler.Compiler().compile(
        pipeline_func=demo_pipeline,
        package_path="demo_pipeline.json",
    )
    print("Pipeline spec written to demo_pipeline.json")
