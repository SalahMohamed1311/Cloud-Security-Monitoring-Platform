# 1. Security Group للتحكم في الدخول والخروج
resource "aws_security_group" "web_sg" {
  name        = "${var.project_name}-sg"
  description = "Allow SSH and HTTP"
  vpc_id      = aws_vpc.main.id

  # السماح بـ SSH (مؤقتاً للتحكم)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

# 2. تعريف الـ Instance (سيرفر المراقبة)
resource "aws_instance" "monitor_node" {
  ami           = "ami-0c101f26f147fa7fd" # Amazon Linux 2023 AMI في us-east-1
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name        = "${var.project_name}-node"
    Environment = var.environment
  }
}