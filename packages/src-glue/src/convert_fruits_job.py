import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType


def run_job(
    glue_context,
    s3_bucket,
    target_year,
    target_month,
    target_day,
    target_hour,
):
    dyf = glue_context.create_dynamic_frame.from_options(
        format_options={"multiline": False},
        connection_type="s3",
        format="json",
        connection_options={
            "paths": [
                f"s3://{s3_bucket}/input/year={target_year}/month={target_month}/day={target_day}/hour={target_hour}/"
            ],
            "recurse": True,
        },
        transformation_ctx="dyf",
    )
    df = dyf.toDF()

    if df.count() <= 0:
        raise Exception("No Data.")

    code_to_fruit_udf = udf(code_to_fruit, StringType())
    df = df.withColumn("name", code_to_fruit_udf(df["code"]))

    df.coalesce(1).write.option("compression", "gzip").mode("overwrite").json(
        f"s3://{s3_bucket}/output/{target_year}/{target_month}/{target_day}/{target_hour}"
    )


def code_to_fruit(code):
    fruits = {
        1: "apple",
        2: "orange",
        3: "grape",
        4: "pear",
        5: "banana",
        6: "cherry",
        7: "strawberry",
        8: "kiwi",
        9: "peach",
        10: "melon",
    }

    return fruits.get(code, "unknown")


def main():
    args = getResolvedOptions(sys.argv, ["JOB_NAME", "IO_S3_BUCKET"])
    job_name = args["JOB_NAME"]
    s3_bucket = args["IO_S3_BUCKET"]

    [target_year, target_month, target_day, target_hour] = ["2023", "01", "05", "07"]

    sc = SparkContext()
    glue_context = GlueContext(sc)
    job = Job(glue_context)

    job.init(job_name, args)
    run_job(
        glue_context,
        s3_bucket,
        target_year,
        target_month,
        target_day,
        target_hour,
    )
    job.commit()


if __name__ == "__main__":
    main()
