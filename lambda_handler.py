import os 
import json


def lambda_handler(event, context):
    print(f" region is : {os.environ['region']}")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }