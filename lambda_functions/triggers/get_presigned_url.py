import json
import boto3
import os
import uuid

s3_client = boto3.client('s3')
S3_BUCKET = os.environ.get('S3_BUCKET', 'one4allthings')
URL_EXPIRATION_SECONDS = 3600

def lambda_handler(event, context):
    """
    Generate an S3 pre-signed URL to upload audio files.
    The user's identity is extracted from the Cognito Authorizer in API Gateway.
    """
    try:
        # Extract sub (User ID) from API Gateway Cognito Authorizer context
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        user_id = claims.get('sub')
        
        # Fallback for local testing or unauthenticated usage if not strictly enforced
        if not user_id:
            user_id = 'unauthenticated-user'
            
        # Get filename and content type from the query string
        query_params = event.get('queryStringParameters', {}) or {}
        file_name = query_params.get('file_name', f"{uuid.uuid4().hex}.mp3")
        content_type = query_params.get('content_type', 'audio/mpeg')
        
        # Enforce exactly the user's directory
        object_key = f"raw_audio/{user_id}/{file_name}"
        
        # Generate the presigned URL via Boto3
        # We use generate_presigned_url because we just want a simple PUT request
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': object_key,
                'ContentType': content_type
            },
            ExpiresIn=URL_EXPIRATION_SECONDS
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # Adjust in production
            },
            'body': json.dumps({
                'upload_url': url,
                'file_key': object_key
            })
        }
        
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Could not generate upload URL.'})
        }
