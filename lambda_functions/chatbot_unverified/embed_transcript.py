import json
import boto3
import os
import urllib.parse

s3_client = boto3.client('s3')
bedrock_runtime = boto3.client('bedrock-runtime')
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'amazon.titan-embed-text-v2:0')

def chunk_text(text, chunk_size=500):
    """
    Very basic sliding window or pure chunking strategy.
    Optimizing for standard text chunks without complex NLP dependencies.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def generate_embedding(text):
    """
    Call Amazon Bedrock to generate vector embeddings.
    """
    try:
        response = bedrock_runtime.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": text})
        )
        response_body = json.loads(response['body'].read().decode('utf-8'))
        return response_body['embedding']
    except Exception as e:
        print(f"Error invoking Bedrock for embedding: {str(e)}")
        raise e

def lambda_handler(event, context):
    """
    Triggered by S3 PUT events in `transcript/`.
    Reads transcript, breaks it into chunks, hits Bedrock for embeddings,
    and saves the Vector JSON payload back into `vector_db/`.
    """
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        print(f"Processing transcript for embedding: {key}")
        
        try:
            # 1. Fetch transcript JSON
            response = s3_client.get_object(Bucket=bucket_name, Key=key)
            transcript_content = json.loads(response['Body'].read().decode('utf-8'))
            
            # Extract standard Transcribe structural text
            # Format varies slightly but usually transcript string is under results.transcripts[0].transcript
            raw_text = transcript_content['results']['transcripts'][0]['transcript']
            
            # 2. Chunk text
            paragraphs = chunk_text(raw_text)
            
            # 3. Generate embeddings
            vectors = []
            for idx, p in enumerate(paragraphs):
                emb = generate_embedding(p)
                vectors.append({
                    "chunk_id": idx,
                    "text": p,
                    "vector": emb
                })
                
            # 4. Save to vector_db
            # If key is transcript/audio_file.json -> vector_db/audio_file_vectors.json
            filename_only = os.path.basename(key)
            name_no_ext, ext = os.path.splitext(filename_only)
            # Ideally the transcript has the user `{sub}` in the path if we enforce it. 
            # We'll save it with the same unique name.
            vector_key = f"vector_db/{name_no_ext}_vectors.json"
            
            s3_client.put_object(
                Bucket=bucket_name,
                Key=vector_key,
                Body=json.dumps(vectors),
                ContentType="application/json"
            )
            print(f"Successfully saved embeddings to {vector_key}")

        except Exception as e:
            print(f"Error processing embeddings for {key}: {str(e)}")
            raise e

    return {"statusCode": 200}
