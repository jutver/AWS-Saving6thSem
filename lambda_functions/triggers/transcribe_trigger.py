import json
import boto3
import uuid
import urllib.parse
import os

transcribe_client = boto3.client('transcribe')

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            if 'Records' not in body: continue
            
            for s3_record in body['Records']:
                bucket_name = s3_record['s3']['bucket']['name']
                key = urllib.parse.unquote_plus(s3_record['s3']['object']['key'])
                
                # Lấy tên file để đặt tên cho file JSON đầu ra
                filename_only = os.path.basename(key)
                name_no_ext, ext = os.path.splitext(filename_only)
                
                # Tạo Job Name ngẫu nhiên (bắt buộc duy nhất)
                job_name = f"Job-{uuid.uuid4().hex[:8]}"
                file_uri = f"s3://{bucket_name}/{key}"
                
                print(f"--- Đang gửi lệnh Transcribe (Tiếng Việt) cho: {key} ---")
                
                # GỬI LỆNH VỚI LANGUAGE CODE CỐ ĐỊNH
                transcribe_client.start_transcription_job(
                    TranscriptionJobName=job_name,
                    Media={'MediaFileUri': file_uri},
                    MediaFormat=ext[1:].lower() if ext else 'mp3',
                    
                    # CHỖ NÀY LÀ QUAN TRỌNG NHẤT:
                    LanguageCode='vi-VN', 
                    
                    OutputBucketName='one4allthings',
                    OutputKey=f"transcript/{name_no_ext}.json"
                )
                print(f"--- Đã gửi thành công Job: {job_name} ---")
                
        except Exception as e:
            print(f"LỖI: {str(e)}")
            raise e

    return {'statusCode': 200}