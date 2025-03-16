import boto3
from botocore.exceptions import ClientError
import os
import json

def send_email(event, context):
    try:
        # If the request comes from function URL, the data might be in the body
        if isinstance(event, dict) and 'body' in event:
            # Check if body is a string (JSON) and parse it
            if isinstance(event['body'], str):
                try:
                    body = json.loads(event['body'])
                except json.JSONDecodeError:
                    body = event['body']
            else:
                body = event['body']
        else:
            body = event
            
        region_name = os.environ.get('region_name')
        print(f"send_email region is : {region_name}")
        from_email = body.get('from')
        print(f"sender is : {from_email}")
        to_email = body.get('to')
        print(f"receiver is : {to_email}")
        cc_email = body.get('cc')
        print(f"cc is : {cc_email}")
        first_name = body.get('first_name')
        sur_name = body.get('sur_name')
        cust_email = body.get('cust_email')
        query_type = body.get('query_type')
        print(f"query type is : {query_type}")
        query = body.get('query')
        print(f"query is : {query}")
        
        subject = f"German classes - {query_type}"
        html_text = f'<html><body><h1>{query_type} - from {cust_email} </h1><p>{query}</p></body></html>'
        
        aws_access_key_id = os.environ.get('aws_access_key_id')
        aws_secret_access_key = os.environ.get('aws_secret_access_key') 
        ses_client = boto3.client('ses', 
                               region_name=region_name,
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key)
        
        response = ses_client.send_email(
            Source=from_email,
            Destination={
                'ToAddresses': [to_email],
                'CcAddresses': [cc_email] if cc_email else [],
                'BccAddresses': []
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': query,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': html_text,
                        'Charset': 'UTF-8'
                    }
                }
            },
            ReplyToAddresses=['tanmay@germanwakad.click']
        )
        
        print(f"Email sent! Message ID: {response['MessageId']}")
        
        # Return proper HTTP response for function URL
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Email sent successfully',
                'messageId': response['MessageId']
            })
        }
        
    except ClientError as e:
        error_message = e.response['Error']['Message']
        print(f"Error: {error_message}")
        
        # Return error response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Failed to send email',
                'message': error_message
            })
        }
    except Exception as e:
        # Catch all other exceptions
        print(f"Unexpected error: {str(e)}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'An unexpected error occurred',
                'message': str(e)
            })
        }