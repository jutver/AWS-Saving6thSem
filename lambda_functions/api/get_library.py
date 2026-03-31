import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'ap-southeast-1'))
AUDIO_TABLE = os.environ.get('AUDIO_TABLE', 'AudioFiles')

def lambda_handler(event, context):
    """
    Retrieves the Library AudioFiles belonging exclusively to the Cognito Authenticated User.
    Handles In-Memory Chronological Sorting and standard Page Limit offsets.
    """
    try:
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        user_id = claims.get('sub')
        
        if not user_id:
            return {
                'statusCode': 401,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Unauthorized: Missing strict user identity.'})
            }
            
        params = event.get('queryStringParameters', {}) or {}
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 20))
        
        table = dynamodb.Table(AUDIO_TABLE)
        
        # 1. Broadly pull ALL records belonging to the authenticated User from DynamoDB
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        items = response.get('Items', [])
        
        while 'LastEvaluatedKey' in response:
            response = table.query(
                KeyConditionExpression=Key('user_id').eq(user_id),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))
            
        # 2. Native Memory Sorting (Newest to Oldest)
        items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        # 3. Apply standard URL Pagination parameters directly onto the List offset
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_items = items[start_idx:end_idx]
        
        formatted_items = []
        for item in paginated_items:
            # Map DB snake_case columns to the arbitrary camelCase schema configured in LibraryPage.jsx
            formatted_items.append({
                "id": item.get('file_id', ''),
                "title": item.get('title', item.get('file_name', 'Untitled')),
                "fileName": item.get('file_name', 'Untitled'),
                "status": item.get('status', 'processing').lower(),
                "createdAt": item.get('created_at', ''),
                "durationSec": int(item.get('duration', 0)),
                "summaryShort": item.get('summary', '')
            })
            
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'data': {
                    'items': formatted_items,
                    'total': len(items),
                    'page': page,
                    'limit': limit
                }
            })
        }
    except Exception as e:
        print(f"Error fetching library: {e}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error while retrieving Library.'})
        }
