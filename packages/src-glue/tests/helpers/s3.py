import boto3

from tests.helpers.config import S3_ENDPOINT_URL

session = boto3.Session()
s3_resource = session.resource("s3", endpoint_url=S3_ENDPOINT_URL)


def create_bucket(bucket_name):
    s3_resource.create_bucket(Bucket=bucket_name)


def delete_bucket(bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()


def list_objects(bucket_name, prefix):
    bucket = s3_resource.Bucket(bucket_name)
    filtered_objects = bucket.objects.filter(Prefix=prefix)
    s3_file_names = list(map(lambda obj: obj.key, filtered_objects))

    return s3_file_names


def download_object(bucket_name, file_path, local_path):
    bucket = s3_resource.Bucket(bucket_name)
    bucket.download_file(file_path, local_path)


def upload_file_to_s3(bucket_name, file_path, s3_file_name):
    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(file_path, s3_file_name)


def delete_file_from_s3(bucket_name, s3_file_name):
    obj = s3_resource.Object(bucket_name, s3_file_name)
    obj.delete()
