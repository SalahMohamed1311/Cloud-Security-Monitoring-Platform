import json
import logging
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    detail = event.get('detail', {})
    user_name = detail.get('requestParameters', {}).get('userName', 'Unknown')
    
    message = f"SECURITY ALERT: A new IAM User was created in your AWS account.\nUsername: {user_name}"
    
    logger.warning(message)
    
    if SNS_TOPIC_ARN:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="[Security Alert] New IAM User Created",
            Message=message
        )
        
    return {"status": "Alert sent", "user": user_name}