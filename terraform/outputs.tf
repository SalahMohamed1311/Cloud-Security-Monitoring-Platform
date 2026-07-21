output "instance_public_ip" {
  description = "Public IP of the security monitor node"
  value       = aws_instance.monitor_node.public_ip
}

output "instance_id" {
  description = "ID of the security monitor node"
  value       = aws_instance.monitor_node.id
}