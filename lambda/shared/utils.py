# lambda/shared/utils.py
import json
import logging
import os
import boto3

# إعداد اللوجات بـ Level مناسب
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_client = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def log_event(event, message="Received event"):
    """دالة موحدة لتسجيل الأحداث بوضوح"""
    logger.info(f"{message}: {json.dumps(event)}")

def send_security_alert(subject, message):
    """دالة مشتركة لإرسال التنبيهات على SNS"""
    logger.warning(message)
    if SNS_TOPIC_ARN:
        try:
            response = sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=subject,
                Message=message
            )
            logger.info(f"SNS Alert sent successfully. MessageId: {response.get('MessageId')}")
            return response
        except Exception as e:
            logger.error(f"Failed to send SNS alert: {str(e)}")
            raise e
    else:
        logger.warning("SNS_TOPIC_ARN is not set in environment variables.")
        return None