#!/usr/bin/python3

import datetime
import logging
import os
import sys

import boto3
import requests
from botocore.client import ClientError
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('parse.log'))
logger.setLevel(logging.INFO)


def parse(url):
    aws_bucket= "burtsev-log"

    try:
        r = requests.get(url)
    except RequestException:
        logger.critical("Not valid url")
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

    logger.info(timestamp + " " + url + " " + sum_tags + " {" + sorted_stats_str + "}")

    upload_to_s3(aws_bucket)

def upload_to_s3(bucket_name):
    s3 = boto3.resource('s3')

    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except ClientError:
        logger.warning('The bucket does not exist or you have no access.')
        logger.warning('Trying to create bucket.')
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'us-east-2'
            }
        )

    logfile = os.path.basename(logger.handlers[0].baseFilename)
    s3.Bucket(bucket_name).upload_file(logfile, logfile)

def main(argv):
    try:
        link=sys.argv[1]
    except IndexError:
        logger.critical('parser.py <url>')
        sys.exit(2)

    parse(link)

if __name__ == "__main__":
    main(sys.argv[1:])

