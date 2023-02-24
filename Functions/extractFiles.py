import boto3


# function extract files from s3 bucket
def extract_files(bucket_name, prefix):
    s3 = boto3.resource('s3')
    result = []
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=prefix):
        result.append(obj.key.rsplit('/', 1)[-1])
    return result
