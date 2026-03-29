import json
import boto3
import os
import math

# Using numpy would normally be best for similarity, but to avoid packaging layers 
# for a simple Lambda, we will write a highly performant native python dot product.
def cosine_similarity(vec1, vec2):
    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(v ** 2 for v in vec1))
    magnitude2 = math.sqrt(sum(v ** 2 for v in vec2))
    if not magnitude1 or not magnitude2:
        return 0
    return dot_product / (magnitude1 * magnitude2)

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'ap-southeast-2'))
bedrock_runtime = boto3.client('bedrock-runtime')

S3_BUCKET = os.environ.get('S3_BUCKET', 'one4allthings')
CHAT_TABLE = os.environ.get('CHAT_TABLE', 'ChatSessions')
BEDROCK_EMBED_MODEL = os.environ.get('BEDROCK_EMBED_MODEL', 'amazon.titan-embed-text-v2:0')
BEDROCK_LLM_MODEL = os.environ.get('BEDROCK_LLM_MODEL', 'anthropic.claude-3-haiku-20240307-v1:0')

def generate_embedding(text):
    response = bedrock_runtime.invoke_model(
        modelId=BEDROCK_EMBED_MODEL,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": text})
    )
    return json.loads(response['body'].read().decode('utf-8'))['embedding']

def retrieve_top_k(query_vec, vectors, k=3):
    scores = []
    for chunk in vectors:
        sim = cosine_similarity(query_vec, chunk['vector'])
        scores.append((sim, chunk['text']))
    
    # Sort by descending similarity and return top k
    scores.sort(key=lambda x: x[0], reverse=True)
    return [ctx for sim, ctx in scores[:k]]

def lambda_handler(event, context):
    try:
        # Extract payloads from API Gateway POST
        body = json.loads(event.get('body', '{}'))
        session_id = body.get('session_id')
        audio_file_id = body.get('audio_file_id') # e.g., name_no_ext from previously
        user_query = body.get('user_query', '')
        
        if not session_id or not audio_file_id or not user_query:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing required fields"})}
        
        # 1. Fetch relevant vector file from S3
        vector_key = f"vector_db/{audio_file_id}_vectors.json"
        
        try:
            s3_resp = s3_client.get_object(Bucket=S3_BUCKET, Key=vector_key)
            db_vectors = json.loads(s3_resp['Body'].read().decode('utf-8'))
        except Exception:
            return {"statusCode": 404, "body": json.dumps({"error": "Transcripts processing not finished or vectors missing"})}

        # 2. Embed user query & perform local semantic search
        query_vec = generate_embedding(user_query)
        top_chunks = retrieve_top_k(query_vec, db_vectors)
        context_string = "\n".join(f"- {c}" for c in top_chunks)
        
        # 3. Fetch recent history from DynamoDB
        table = dynamodb.Table(CHAT_TABLE)
        history_resp = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('session_id').eq(session_id),
            ScanIndexForward=False,
            Limit=5 # Fetch last 5 interactions to maintain short context
        )
        
        messages = [{"role": "system", "content": f"You are a helpful meeting summarizer. Use the context to answer.\nContext:\n{context_string}"}]
        
        # Bedrock Claude expects distinct alternates. Let's form the string context or array.
        # Format depends heavily on Claude 3 API structure, typically role and content.
        for item in reversed(history_resp.get('Items', [])):
            messages.append({"role": item['role'], "content": item['text']})
            
        messages.append({"role": "user", "content": user_query})
        
        # 4. Invoke LLM Bedrock (Claude 3 standard message structure)
        claude_payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": messages[1:],  # excluding system prompt from messages array for standard params
            "system": messages[0]['content'] # System passed as a top-level param
        }
        
        llm_response = bedrock_runtime.invoke_model(
            modelId=BEDROCK_LLM_MODEL,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(claude_payload)
        )
        llm_res_body = json.loads(llm_response['body'].read().decode('utf-8'))
        assistant_reply = llm_res_body.get('content', [{}])[0].get('text', '')
        
        # 5. Save history to DynamoDB
        import time
        timestamp = str(int(time.time() * 1000))
        table.put_item(Item={"session_id": session_id, "timestamp": timestamp, "role": "user", "text": user_query})
        table.put_item(Item={"session_id": session_id, "timestamp": str(int(timestamp)+1), "role": "assistant", "text": assistant_reply})
        
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"reply": assistant_reply})
        }
        
    except Exception as e:
        print(f"Error serving chatbot request: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
