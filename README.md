# Cloud Security Monitoring & Threat Detection Platform

## Project Overview

This project demonstrates the design and implementation of a secure AWS
environment focused on monitoring, threat detection, logging, and
incident response.

## Architecture

-   Custom VPC
-   Public Subnet
-   Internet Gateway
-   EC2 Ubuntu Server
-   S3 for log storage
-   CloudTrail for audit logging
-   CloudWatch for monitoring and dashboards
-   SNS for email alerts
-   GuardDuty for threat detection
-   AWS Config for compliance monitoring

## Security Features

-   MFA enabled
-   Least privilege IAM policies
-   Restricted SSH access
-   Billing alarms
-   CloudTrail logging
-   CloudWatch alarms
-   GuardDuty findings monitoring
-   AWS Config compliance checks

## Attack Simulations

1.  SSH brute-force attempts
2.  Opening port 22 to 0.0.0.0/0 and remediation
3.  Privilege escalation test user
4.  Access key creation and monitoring

## Folder Structure

-   architecture: architecture descriptions
-   diagrams: AWS architecture diagrams
-   screenshots: evidence and screenshots
-   docs: project documentation
-   incident-reports: incident response reports
-   monitoring: metrics and dashboards
-   alerts: SNS and CloudWatch alert documentation

## Skills Demonstrated

-   AWS IAM
-   VPC
-   EC2
-   S3
-   CloudTrail
-   CloudWatch
-   SNS
-   GuardDuty
-   AWS Config
-   Incident Response
-   Threat Detection
-   Cloud Security Best Practices

## Future Improvements

-   Terraform automation
-   EventBridge integration
-   Lambda automation
-   Security Hub integration
-   Web dashboard
