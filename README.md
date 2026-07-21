☁️ Cloud Security Monitoring & Automation Platform

Show Image Show Image Show Image Show Image Show Image

A cloud security project that evolved from a manually monitored secure AWS environment (v1) into a fully automated cloud security platform (v2) — infrastructure as code, event-driven threat response, and CI/CD for infrastructure, all built and documented from scratch.

📌 Project Overview

This project demonstrates hands-on, end-to-end cloud security engineering on AWS: building a hardened environment, monitoring it, simulating real attacks against it, and — in v2 — teaching it to detect and respond to threats on its own, with the entire infrastructure defined and reproducible as code.

	v1	v2
Infrastructure	Built manually via AWS Console	Built with Terraform (Infrastructure as Code)
Threat response	Manual review of GuardDuty/CloudTrail findings	Automated via Lambda, triggered by EventBridge
Validation	Manual checks	GitHub Actions CI validates Terraform on every push
Secrets	N/A	Managed outside the codebase
Teardown	Manual cleanup	One command: terraform destroy
🏗️ Architecture

Core AWS components:

Custom VPC, Public Subnet, Internet Gateway, Route Table
EC2 (Ubuntu Server) behind a restricted Security Group
S3 for centralized log storage
CloudTrail for audit logging
CloudWatch (alarms + dashboards) for monitoring
SNS for real-time email alerts
GuardDuty for threat detection
AWS Config for compliance monitoring

v2 automation layer:

Terraform — the entire environment above is defined as code, modules for network / compute / logging / monitoring
AWS Lambda — automated remediation functions (e.g. closing an unexpectedly open port, creating an incident record, sending notifications)
Amazon EventBridge — routes security findings (GuardDuty, Config, CloudTrail) to the right Lambda function
GitHub Actions — CI pipeline that validates/formats Terraform on every push
Secrets Manager — credentials and sensitive values kept out of the codebase entirely

Full diagrams: see architecture.md and diagram-instructions.md

🔐 Security Features
MFA enforced on the account
Least-privilege IAM policies (no root usage for daily work)
Restricted SSH access
Billing alarms
CloudTrail logging of all account activity
CloudWatch alarms on suspicious activity
GuardDuty findings monitored and routed to automated response
AWS Config continuously checking compliance
Secrets kept out of source control
🎯 Attack Simulations & Incident Response

Real attack scenarios were simulated against the environment to validate detection and (in v2) automated remediation:

SSH brute-force attempts → detected via CloudTrail/GuardDuty
Opening port 22 to 0.0.0.0/0 → detected and remediated
IAM privilege escalation attempt (throwaway test user)
Unusual access key creation → monitored and alerted

Full write-ups: incident-001-ssh-bruteforce.md · incident-002-security-group.md · incident-003-privilege-escalation.md

📁 Repository Structure
Cloud-Security-Monitoring-Platform/
├── .github/workflows/          # GitHub Actions CI (Terraform validation)
├── terraform/                  # Infrastructure as Code
├── lambda/                     # Automated threat-response functions
├── architecture.md             # System architecture
├── project-setup.md            # Setup & prerequisites
├── cloudtrail-logging.md       # Logging configuration
├── cloudwatch-alarms.md        # Alarm configuration
├── cloudwatch-dashboard.md     # Monitoring dashboard
├── sns-alerts.md                # Alerting configuration
├── diagram-instructions.md     # How the architecture diagrams were built
├── incident-001-ssh-bruteforce.md
├── incident-002-security-group.md
├── incident-003-privilege-escalation.md
├── screenshots-checklist.md    # Evidence checklist
├── lessons-learned.md
└── README.md
🧠 Skills Demonstrated

AWS IAM VPC EC2 S3 CloudTrail CloudWatch SNS GuardDuty AWS Config Terraform Infrastructure as Code AWS Lambda Amazon EventBridge GitHub Actions / CI-CD Secrets Management Automated Incident Response Cloud Security Automation DevSecOps Threat Detection Cloud Security Best Practices

🚀 Getting Started
bash
# clone the repo
git clone https://github.com/SalahMohamed1311/Cloud-Security-Monitoring-Platform.git
cd Cloud-Security-Monitoring-Platform/terraform

# configure AWS CLI with a scoped IAM user (never root)
aws configure

# review and provision the infrastructure
terraform init
terraform plan
terraform apply

# tear it all down when you're done
terraform destroy
📦 Releases

Latest: v2.0.0 — Cloud Security Automation Platform — rebuilt infrastructure with Terraform, automated threat response via Lambda, EventBridge integration, GitHub Actions CI, and full documentation.

🗺️ Roadmap (v3)
 AWS Security Hub integration
 WAF (Web Application Firewall)
 Full monitoring dashboard (single-pane-of-glass view)
👤 Author

Salah Mohamed — @SalahMohamed1311 Built as a hands-on path toward cloud security engineering.
