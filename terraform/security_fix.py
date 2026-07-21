import boto3
import json

def lambda_handler(event, context):
    # إعداد العميل الخاص بـ EC2
    ec2 = boto3.client('ec2')
    
    # الحصول على الـ Security Group ID من الـ Event (الحدث)
    # ده هيجينا من الـ CloudWatch Rule اللي هنظبطها لاحقاً
    sg_id = event['detail']['requestParameters']['groupId']
    
    # إزالة قاعدة السماح بـ SSH (بورت 22) للـ 0.0.0.0/0
    try:
        ec2.revoke_security_group_ingress(
            GroupId=sg_id,
            IpProtocol='tcp',
            FromPort=22,
            ToPort=22,
            CidrIp='0.0.0.0/0'
        )
        print(f"تم إغلاق البورت 22 في الـ Security Group: {sg_id}")
    except Exception as e:
        print(f"خطأ أثناء محاولة إغلاق البورت: {str(e)}")
        
    return {
        'statusCode': 200,
        'body': json.dumps('تمت عملية التأمين بنجاح!')
    }