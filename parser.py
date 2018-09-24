import boto3
import requests
from bs4 import BeautifulSoup
from botocore.client import ClientError

# to_bucket_name = "to-bucket"
# to_bucket = 0
# from_bucket_list_names = ["from-bucket-1", "from-bucket-2"]
# s3 = boto3.resource('s3')
#
# try:
#     to_bucket = s3.meta.client.head_bucket(Bucket=to_bucket_name)
# except ClientError:
#     print("The bucket does not exist or you have no access.")
#     print("Trying to create bucket.")
#     to_bucket_obj = s3.create_bucket(
#         Bucket=to_bucket_name,
# CreateBucketConfiguration={
#             'LocationConstraint': 'us-east-2'
# }
#     )
#
# to_bucket = s3.Bucket(to_bucket_name)
#
# for from_bucket_name in from_bucket_list_names:
#     from_bucket = s3.Bucket(from_bucket_name)
#
#     for file in from_bucket.objects.all():
#         copy_source = {
#             'Bucket': from_bucket,
# 'Key': file
#         }
#         to_bucket.copy(copy_source, file)
#
# for bucket in s3.buckets.all():
#     print(bucket.name)

r = requests.get('https://ya.ru')

soup = BeautifulSoup(r.text, 'html.parser')

stats={}

raw = [tag.name for tag in soup.find_all()]

for key in raw:
    if key in stats:
        stats[key] = stats[key] + 1
    else:
        stats[key] = 1

sum_tags = len(raw)
print(sum_tags)
print(sorted(stats.keys()))
