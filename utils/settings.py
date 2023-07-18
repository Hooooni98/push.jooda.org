import boto3
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebase_service_account_key.json")
firebase_admin.initialize_app(cred)

AWS_ACCESS_KEY = "##############"
AWS_SECRET_KEY = "##############"

S3_CLIENT = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
)
dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="ap-northeast-2",
)
