import json
import boto3
import urllib.parse
import os

DYNAMODB_REGION = os.environ.get('DYNAMODB_REGION', 'ap-southeast-1')
transcribe_client = boto3.client('transcribe')
dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_REGION)
AUDIO_TABLE = os.environ.get('AUDIO_TABLE', 'AudioFiles')

def lambda_handler(event, context):
    """
    Triggered by S3 -> SQS when an audio file is uploaded to raw_audio/
    Initiates AWS Transcribe job and marks the DB AudioFiles stage as Transcribing.
    """
    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            if 'Records' not in body: continue
            
            for s3_record in body['Records']:
                bucket_name = s3_record['s3']['bucket']['name']
                key = urllib.parse.unquote_plus(s3_record['s3']['object']['key'])
                
                # Extract User ID and Hash ID from path `raw_audio/{user_id}/{hash_id}.ext`
                parts = key.split('/')
                if len(parts) < 3:
                    print(f"Skipping key {key} due to unexpected root structure.")
                    continue
                    
                user_id = parts[1]
                filename_only = parts[2]
                hash_id, ext = os.path.splitext(filename_only)
                
                # Follow user's strict formatting schema
                job_name = f"Job-{user_id}-{hash_id}"
                file_uri = f"s3://{bucket_name}/{key}"
                output_key = f"transcript/{user_id}/{hash_id}.json"
                
                print(f"--- Sending Transcribe task (Vietnamese) for: {key} ---")
                
                # Send task with fixed language code
                transcribe_client.start_transcription_job(
                    TranscriptionJobName=job_name,
                    Media={'MediaFileUri': file_uri},
                    MediaFormat=ext[1:].lower() if ext else 'mp3',
                    LanguageCode='vi-VN', 
                    OutputBucketName=bucket_name,
                    OutputKey=output_key
                )
                
                # Update DynamoDB table
                try:
                    table = dynamodb.Table(AUDIO_TABLE)
                    table.update_item(
                        Key={
                            'user_id': user_id,
                            'file_id': hash_id
                        },
                        UpdateExpression="SET stage = :s, job_id = :j, s3_transcript = :t",
                        ExpressionAttributeValues={
                            ':s': 'Transcribing',
                            ':j': job_name,
                            ':t': f"s3://{bucket_name}/{output_key}"
                        }
                    )
                    print(f"Updated DynamoDB AudioFiles {hash_id} stage to Transcribing.")
                except Exception as db_err:
                    print(f"Warning: Transcribe Job started but failed to update DB: {db_err}")
                
        except Exception as e:
            print(f"ERROR: {str(e)}")
            raise e

    return {'statusCode': 200}
