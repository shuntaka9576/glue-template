import gzip
import os

import pytest

from src import convert_fruits_job
from tests.helpers import s3
from tests.helpers.config import S3_BUCKET_NAME


@pytest.fixture()
def setup_sample_data():
    s3_file_name = "input/year=2023/month=01/day=05/hour=07/input-data-7-2024-01-21-23-42-22-ac74facb-bc41-3931-a76e-66e445872d60.gz"
    s3.create_bucket(S3_BUCKET_NAME)
    s3.upload_file_to_s3(
        S3_BUCKET_NAME, "tests/testdata/input-data.jsonl", s3_file_name
    )
    yield
    s3.delete_file_from_s3(S3_BUCKET_NAME, s3_file_name)
    s3.delete_bucket(S3_BUCKET_NAME)


class TestConvertFruitsJob:
    def test_run_job(self, fixture_setup_glue, setup_sample_data):
        convert_fruits_job.run_job(
            fixture_setup_glue,
            S3_BUCKET_NAME,
            "2023",
            "01",
            "05",
            "07",
        )

        file_prefix = "output/2023/01/05/07"
        s3_object_paths = s3.list_objects(S3_BUCKET_NAME, file_prefix)
        assert len(s3_object_paths) == 1

        s3_object_path = s3_object_paths[0]
        s3_object_name = os.path.basename(s3_object_path)
        local_path = f"/tmp/{s3_object_name}"
        s3.download_object(S3_BUCKET_NAME, f"{s3_object_path}", local_path)

        expected_output_lines = [
            b'{"code":2,"name":"orange"}\n',
            b'{"code":5,"name":"banana"}\n',
            b'{"code":3,"name":"grape"}\n',
            b'{"code":4,"name":"pear"}\n',
            b'{"code":1,"name":"apple"}\n',
        ]

        with gzip.open(local_path) as f:
            content = f.read()
            assert content == b"".join(expected_output_lines)
