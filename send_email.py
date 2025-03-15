import boto3
from botocore.exceptions import ClientError
import os 


def send_email(event,context):
    region_name = os.environ.get('region_name')
    print(f"send_email region is : {region_name}")
    receiver = event.get('to')
    print(f"receiver is : {receiver}")
    cc_email = event.get('cc')
    aws_access_key_id = os.environ.get('aws_access_key_id')
    aws_secret_access_key = os.environ.get('aws_secret_access_key') 
    ses_client = boto3.client('ses', 
                             region_name=region_name,  # Use your region
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
    
    try:
        response = ses_client.send_email(
            Source='tany.germanwakad@gmail.com',
            Destination={
                'ToAddresses': ['tany.patil77@gmail.com'],
                'CcAddresses': [cc_email],
                'BccAddresses': []
            },
            Message={
                'Subject': {
                    'Data': 'german classes',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'This is the first mail for german classes',
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': '<html><body><h1>German classes </h1><p>This is the first mail for german classes</p></body></html>',
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