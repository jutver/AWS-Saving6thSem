import json
import boto3
import os
import hashlib
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'ap-southeast-1'))

S3_BUCKET = os.environ.get('S3_BUCKET', 'one4allthings')
AUDIO_TABLE = os.environ.get('AUDIO_TABLE', 'AudioFiles')
URL_EXPIRATION_SECONDS = 3600

def generate_hash(file_name):
    # Hash the file name combined with the current timestamp
    timestamp_str = datetime.utcnow().isoformat()
    raw_str = f"{file_name}-{timestamp_str}"
    # Use sha256 to ensure robust collision avoidance
    return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()[:16] # Shortened for practicality

def lambda_handler(event, context):
    """
    Generate an S3 pre-signed URL to upload audio files.
    The user's identity is extracted from Cognito Authorizer.
    It expects JSON payload from FE containing:
    { "file_name": "meeting.mp3", "file_type": "audio/mpeg", "duration": 120, "title": "Quarterly Sync" }
    """
    try:
        # Extract sub (User ID) from API Gateway Cognito Authorizer context
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        user_id = claims.get('sub')
        
        if not user_id:
            # Fallback block or strict return
            user_id = 'unauthenticated-user' # Remove logic in production
            
        # Parse Required Fields from FE Payload
        body = json.loads(event.get('body', '{}'))
        file_name = body.get('fileName')
        file_type = body.get('contentType')
        file_size = body.get('fileSize')
        duration = body.get('durationSec')
        title = body.get('title', file_name)

        if not all([file_name, file_type, file_size, duration]):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Missing required fields: file_name, file_type, or duration'})
            }
            
        # Extract extension and generate safe Hash ID
        _, ext = os.path.splitext(file_name)
        hash_id = generate_hash(file_name)
        
        # Provision DB Record first
        table = dynamodb.Table(AUDIO_TABLE)
        
        s3_audio_path = f"raw_audio/{user_id}/{hash_id}"
        
        table.put_item(
            Item={
                "user_id": user_id,            # Partition Key
                "file_id": hash_id,            # Sort Key
                "created_at": datetime.utcnow().isoformat() + "Z",
                "duration": duration,
                "file_type": file_type,
                "file_size": file_size,
                "file_name": file_name,        # Original File Name
                "title": title,                # Display Name
                "s3_audio": f"s3://{S3_BUCKET}/{s3_audio_path}",
                "s3_transcript": "",
                "job_id": "",
                "stage": "Uploading",
                "status": "Pending",
                "summary": ""
            }
        )
        
        # Generate the presigned URL
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': s3_audio_path,
                'ContentType': file_type
            },
            ExpiresIn=URL_EXPIRATION_SECONDS
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'data': {
                    'uploadUrl': url,
                    'recordingId': hash_id,
                    'fileUrl': f"s3://{S3_BUCKET}/{s3_audio_path}"
                }
            })
        }
        
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Could not generate upload URL and initialize DB record.'})
        }
