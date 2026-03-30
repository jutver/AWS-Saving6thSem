import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import os

DYNAMODB_REGION = os.environ.get("DYNAMODB_REGION", "ap-southeast-1")
dynamodb = boto3.resource("dynamodb", region_name=DYNAMODB_REGION)
USERS_TABLE = "Users"

s3_client = boto3.client("s3")
S3_BUCKET = os.environ.get("S3_BUCKET", "one4allthings")

def lambda_handler(event, context):
    """
    Cognito Post Confirmation Trigger.
    Write record into DynamoDB when a user completes registration and verifies their email. Also create S3 prefixes for the new user.
    """
    print(f"Cognito Event Triggered: {event['triggerSource']}")

    if event["triggerSource"] == "PostConfirmation_ConfirmSignUp":
        user_attributes = event["request"]["userAttributes"]
        user_id = user_attributes.get("sub")
        email = user_attributes.get("email", "")
        
        if not user_id:
            print("Error: No 'sub' found in user attributes.")
            return event
        
        try:
            table = dynamodb.Table(USERS_TABLE)
            table.put_item(
                Item={
                    "user_id": user_id,
                    "email": email,
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "total_files": 0,
                    "storage_used_bytes": 0,
                    "total_audio_duration": 0,
                },
                ConditionExpression="attribute_not_exists(user_id)"
            )
            print(f"Successfully provisioned DynamoDB record for user: {user_id}")
            
            try:
                audio_folder = f"raw_audio/{user_id}/"
                transcript_folder = f"transcript/{user_id}/"
                s3_client.put_object(Bucket=S3_BUCKET, Key=audio_folder)
                s3_client.put_object(Bucket=S3_BUCKET, Key=transcript_folder)
                print(f"Successfully provisioned S3 directory pattern for user: {user_id}")
            except Exception as e:
                print(f"Warning: Failed to create S3 prefixes for {user_id}: {e}")
        
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                print(f"User {user_id} already exists in DynamoDB. Skipping insertion.")
            else:
                print(f"Failed to insert user into DynamoDB: {e}")
                
    return event
