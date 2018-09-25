#!/usr/bin/python3

import sys
import logging

import datetime
from collections import OrderedDict

import boto3
import requests
from bs4 import BeautifulSoup
from botocore.client import ClientError

logging.basicConfig(filename='parse.log',level=logging.INFO)

from requests.exceptions import MissingSchema, RequestException


def parse(url):
    try:
        r = requests.get(url)
    except RequestException:
        logging.critical("Not valid url")
        sys.exit(3)

    soup = BeautifulSoup(r.text, 'html.parser')

    stats={}

    raw = [tag.name for tag in soup.find_all()]

    for key in raw:
        if key in stats:
            stats[key] = stats[key] + 1
        else:
            stats[key] = 1

    sum_tags = str(len(raw))

    sorted_stats_str=', '.join('\'' + tpl[0] + '\':' + str(tpl[1]) for tpl in sorted(stats.items(),key=lambda item: item[1], reverse=True))

    timestamp = datetime.datetime.now().strftime("%Y/%W/%m/%d %H:%M")

    logging.info(timestamp + " " + url + " " + sum_tags + " {" + sorted_stats_str + "}")

def upload_to_s3(bucket_name):
    to_bucket_name = "burtsevyg-logs"
    from_bucket_list_names = ["from-bucket-1", "from-bucket-2"]
    s3 = boto3.resource('s3')

    try:
        to_bucket = s3.meta.client.head_bucket(Bucket=to_bucket_name)
    except ClientError:
        print("The bucket does not exist or you have no access.")
        print("Trying to create bucket.")
        to_bucket_obj = s3.create_bucket(
            Bucket=to_bucket_name,
    CreateBucketConfiguration={
                'LocationConstraint': 'us-east-2'
    }
        )

    to_bucket = s3.Bucket(to_bucket_name)

    for from_bucket_name in from_bucket_list_names:
        from_bucket = s3.Bucket(from_bucket_name)

        for file in from_bucket.objects.all():
            copy_source = {
                'Bucket': from_bucket,
    'Key': file
            }
            to_bucket.copy(copy_source, file)

    for bucket in s3.buckets.all():
        print(bucket.name)


def main(argv):
    try:
        link=sys.argv[1]
    except IndexError:
        logging.critical('parser.py <url>')
        sys.exit(2)

    parse(link)

if __name__ == "__main__":
    main(sys.argv[1:])

