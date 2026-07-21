import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        detail = event.get('detail', {})
        request_parameters = detail.get('requestParameters', {})
        
        # استخراج الـ Security Group ID (يدعم التسميتين في الـ API الجديد والقديم)
        group_id = request_parameters.get('groupId') or request_parameters.get('securityGroupId')
        if not group_id:
            logger.info("No groupId found in request parameters.")
            return {"status": "No action needed"}

        # معالجة الهياكل المختلفة للـ permissions بين الـ APIs القديمة والجديدة
        ip_permissions = []
        
        # الهيكل القديم (AuthorizeSecurityGroupIngress)
        if 'ipPermissions' in request_parameters:
            ip_permissions = request_parameters.get('ipPermissions', {}).get('items', [])
            
        # الهيكل الجديد (ModifySecurityGroupRules - Add/Modify)
        elif 'addIpPermissions' in request_parameters:
            ip_permissions = request_parameters.get('addIpPermissions', {}).get('items', [])
        elif 'securityGroupRuleSet' in request_parameters:
            # لو جاية من ModifySecurityGroupRules مباشرة
            pass

        # بديل مباشر وآمن للتعامل مع الـ ModifySecurityGroupRules أو جلب القاعدة الحالية وكمان الكود الحالي
        # خلينا نضمن فحص الـ ipPermissions بالطريقة المباشرة المتاحة
        if not ip_permissions and 'ipPermissions' in detail.get('responseElements', {}):
            ip_permissions = detail.get('responseElements', {}).get('ipPermissions', [])

        # فحص وتطبيق الحذف لأي قواعد غير آمنة مفتوحة على 0.0.0.0/0 تشمل بورت 22
        # طريقة بديلة أضمن: لو حصل تعديل على الـ SG ده، نقدر نجيب الحفرة ونقفلها أو نعتمد على الـ permission المستخرجة
        
        # لو الـ ipPermissions فاضية، ممكن نقرأ الـ rules المضافة من الحدث مباشرة لو متوفرة
        # لكن خلينا نظبط الكود بحيث يفحص الـ items المتاحة أياً كانت:
        
        # للتعامل السريع مع ModifySecurityGroupRules اللي فيها ipPermissions مباشرة كـ List:
        raw_permissions = request_parameters.get('ipPermissions')
        if isinstance(raw_permissions, list):
            ip_permissions = raw_permissions
        elif isinstance(raw_permissions, dict):
            ip_permissions = raw_permissions.get('items', [])

        for permission in ip_permissions:
            ip_protocol = permission.get('ipProtocol', '-1')
            from_port = permission.get('fromPort', -1)
            to_port = permission.get('toPort', -1)
            
            # التأكد إن البورت 22 أو كل البورتات مفتوحة لـ 0.0.0.0/0
            is_all_ports = (ip_protocol == '-1')
            is_ssh = (ip_protocol == 'tcp' or ip_protocol == '6') and (from_port <= 22 <= to_port)
            
            if is_all_ports or is_ssh:
                ip_ranges = permission.get('ipRanges', [])
                if isinstance(ip_ranges, dict):
                    ip_ranges = ip_ranges.get('items', [])
                    
                for ip_range in ip_ranges:
                    cidr = ip_range.get('cidrIp') if isinstance(ip_range, dict) else ip_range
                    if cidr == '0.0.0.0/0':
                        logger.warning(f"Unsafe SSH/All port detected on SG: {group_id}. Revoking...")
                        
                        ec2.revoke_security_group_ingress(
                            GroupId=group_id,
                            IpPermissions=[{
                                'IpProtocol': ip_protocol,
                                'FromPort': from_port if from_port != -1 else 22,
                                'ToPort': to_port if to_port != -1 else 22,
                                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                            }]
                        )
                        logger.info(f"Successfully revoked ingress rule for {group_id}")
                        
        return {"status": "Success", "closed_sg": group_id}
        
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        raise e