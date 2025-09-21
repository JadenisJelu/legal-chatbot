import os
import json
import boto3
import uuid
from datetime import datetime
import traceback
import base64

# Set up the S3 client
s3_client = boto3.client('s3')

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def lambda_handler(event, context):
    print(f"Event is: {event}")
    
    # Check if S3_BUCKET_NAME is configured
    if not S3_BUCKET_NAME:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'success': False,
                'error': 'S3_BUCKET_NAME environment variable not configured'
            })
        }
    
    try:
        # Handle the request body
        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({'error': 'No file data received'})
            }

        # Decode the body if it's base64 encoded
        body = event['body']
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body)
        elif isinstance(body, str):
            try:
                body = base64.b64decode(body)
            except:
                # If it's not base64, treat as raw bytes
                body = body.encode('utf-8')

        # For multipart form data, we need to parse it
        # This is a simplified parser for demonstration
        # In production, you'd want to use a proper multipart parser like python-multipart
        
        # Extract filename from Content-Disposition header if available
        filename = None
        if 'headers' in event:
            content_disposition = event['headers'].get('content-disposition', '')
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"')
        
        # Generate unique filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"uploaded_documents/{timestamp}_{unique_id}.pdf"
        else:
            # Sanitize filename and add timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            safe_filename = filename.replace(' ', '_').replace('/', '_')
            filename = f"uploaded_documents/{timestamp}_{unique_id}_{safe_filename}"

        # Determine content type
        content_type = 'application/octet-stream'
        if filename.lower().endswith('.pdf'):
            content_type = 'application/pdf'
        elif filename.lower().endswith(('.txt', '.text')):
            content_type = 'text/plain'
        elif filename.lower().endswith(('.doc', '.docx')):
            content_type = 'application/msword'
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename,
            Body=body,
            ContentType=content_type,
            Metadata={
                'uploaded-by': 'legal-chatbot',
                'upload-timestamp': datetime.now().isoformat()
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'success': True,
                'message': 'File uploaded successfully',
                'filename': filename,
                's3_key': filename,
                'content_type': content_type
            })
        }

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        stack_trace = traceback.format_exc()
        print(f"stack trace: {stack_trace}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Upload failed: {str(e)}'
            })
        }
