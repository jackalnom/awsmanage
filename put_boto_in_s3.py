import boto3

client = boto3.client('s3')
x
bucket = 'boto-big-bucket-test'
object = 'bototype'
contents = 'am I real?'

client.put_object(Key=object, Bucket=bucket, Body=contents)
