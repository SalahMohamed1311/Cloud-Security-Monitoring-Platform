# Incident 002 - Public SSH Exposure

## Severity

High

## Detection Source

AWS Config

## Description

Port 22 was opened to 0.0.0.0/0 for testing purposes.

## Mitigation

Reverted Security Group to trusted IP only.
