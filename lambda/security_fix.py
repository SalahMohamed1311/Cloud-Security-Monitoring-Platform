import json
import boto3
import os

sns_client = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    print("Received event: ", json.dumps(event))
    
    event_detail = event.get('detail', {})
    event_name = event_detail.get('eventName')
    user_identity = event_detail.get('userIdentity', {}).get('userName', 'Unknown')
    
    message = f"Security Alert! Event: {event_name} triggered by user: {user_identity}"
    
    if event_name in ['CreateUser', 'CreateAccessKey']:
        if SNS_TOPIC_ARN:
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject=f"AWS Security Incident: {event_name}"
            )
            print(f"Alert sent for {event_name}")
            
    return {
        'statusCode': 200,
        'body': json.dumps('Event processed successfully!')
    }