import boto3
import configparser
import os


config = configparser.ConfigParser()
config.read('dwh.cfg')
os.environ["AWS_ACCESS_KEY_ID"] = config.get("AWS", "KEY")
os.environ["AWS_SECRET_ACCESS_KEY"] = config.get("AWS", "SECRET")
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

s3 = boto3.client('s3')


bucket_name = 'udacity-deng-capstone-project'
s3.create_bucket(Bucket=bucket_name
                 , CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})

s3.upload_file("temperature_US.csv", bucket_name, 
                "temperature_US.csv")
    
s3.upload_file("i94_laos.csv", bucket_name, 
                "i94_laos.csv")

s3.upload_file("us-cities-demographics.csv", bucket_name, 
                "us-cities-demographics.csv")


