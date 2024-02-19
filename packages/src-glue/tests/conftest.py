import pytest
from awsglue.context import GlueContext
from awsglue.job import Job
from helpers.config import S3_ENDPOINT_URL
from pyspark.sql import SparkSession


@pytest.fixture()
def fixture_setup_glue():
    sc = SparkSession.builder.getOrCreate()
    sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", S3_ENDPOINT_URL)
    sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
    sc._jsc.hadoopConfiguration().set("fs.s3a.signing-algorithm", "S3SignerType")
    sc._jsc.hadoopConfiguration().set("fs.s3a.change.detection.mode", "None")
    sc._jsc.hadoopConfiguration().set(
        "fs.s3a.change.detection.version.required", "false"
    )
    context = GlueContext(sc)
    job = Job(context)

    yield (context)

    job.commit()
    sc.stop()
