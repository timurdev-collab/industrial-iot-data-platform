# AWS Cloud and Jira Cloud integration plan

> **Planning documentation only.** This repository does not claim an active AWS deployment, a Jira project, or implemented Jira automation. Earlier local functionality is unchanged.

## Project
Industrial IoT Data Platform

## Proposed AWS architecture
AWS S3 landing zone -> EventBridge schedule -> AWS Lambda ETL -> RDS PostgreSQL/Glue -> CloudWatch

This architecture is a **proposal**, not a deployed service. Some AWS services listed can incur fees. Do not run infrastructure provisioning without an AWS budget, billing alarms, least-privilege credentials and explicit deployment approval. For local development, continue to use the repository's existing documented commands.

## Jira Cloud project management
Use a Jira Cloud Kanban board with issue types Epic, Story, Task and Bug. Suggested workflow: Backlog -> Selected -> In Progress -> Code Review -> Done. Reference the Jira issue key in branch names and pull request titles once Jira is configured. Link commits and PRs through Jira's GitHub integration if authorized.

### Suggested backlog
1. Define data contracts and ingestion schema
2. Implement incremental loads and dead-letter handling
3. Add S3 ingest and least-privilege IAM Terraform
4. Deploy to AWS sandbox after cost approval
5. Benchmark SQL queries and add quality SLAs

## Evidence checklist before mentioning AWS/Jira as hands-on experience
- AWS: deployed resources, infrastructure code, cost guardrails, CloudWatch evidence and reproducible setup instructions.
- Jira: created Jira board/issues, linked repo or PRs, and a demonstrable ticket history.

**Current status:** AWS architecture and Jira workflow are documented; services are **not connected or deployed**.
