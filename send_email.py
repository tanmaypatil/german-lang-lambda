import boto3
from botocore.exceptions import ClientError
import os 


def send_email(event,context):
    region_name = os.environ.get('region_name')
    print(f"send_email region is : {region_name}")
    from_email = event.get('from')
    print(f"receiver is : {from_email}")
    to_email = event.get('to')
    print(f"receiver is : {to_email}")
    cc_email = event.get('cc')
    print(f"cc is : {cc_email}")
    # Query type 
    query_type = event.get('query_type')
    print(f"query is : {query_type}")
    # Detailed query 
    query = event.get('query')
    print(f"query is : {query}")
    # create a subject 
    subject = f"German classes - {query_type}"
    # full html text
    html_text = f'<html><body><h1>{query_type} - from {from_email} </h1><p>{query}</p></body></html>'
    
    aws_access_key_id = os.environ.get('aws_access_key_id')
    aws_secret_access_key = os.environ.get('aws_secret_access_key') 
    ses_client = boto3.client('ses', 
                             region_name=region_name,  # Use your region
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
    
    try:
        response = ses_client.send_email(
            Source=from_email,
            Destination={
                'ToAddresses': [to_email],
                'CcAddresses': [cc_email],
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
        return response
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
        return None