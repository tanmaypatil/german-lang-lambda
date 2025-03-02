import boto3
from botocore.exceptions import ClientError

def send_email():
    ses_client = boto3.client('ses', 
                             region_name='us-east-1',  # Use your region
                             aws_access_key_id='YOUR_ACCESS_KEY',
                             aws_secret_access_key='YOUR_SECRET_KEY')
    
    try:
        response = ses_client.send_email(
            Source='tanmay@germanwakad.click',
            Destination={
                'ToAddresses': ['tany.patil77@gmail.com'],
                'CcAddresses': ['tany.germanwakad@gmail.com'],
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