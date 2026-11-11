
# AI CI/CD Release Guard

An early-stage DevOps and AI integration project that retrieves GitLab CI/CD pipeline information, evaluates pipeline status, and provides an AI-generated explanation for release decisions.

## Features

- FastAPI backend with health-check endpoint.
- GitLab API integration for project and pipeline information.
- Rule-based release decisions: Allow, Wait, or Block.
- Local Llama 3 integration through Ollama for decision explanations.
- AWS infrastructure provisioning using Terraform.
- Docker-based application packaging.

## Technology Stack

- Python
- FastAPI
- GitLab REST API
- Ollama / Llama 3
- AWS EC2 and VPC
- Terraform
- Docker

## Project Structure

```text
ai-cicd-release-guard/
├── application/
│   ├── mainapp.py
│   └── Dockerfile
├── infra/
│   └── main.tf
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

- Python
- Docker
- Terraform
- AWS CLI configured with appropriate permissions
- GitLab access token
- Ollama with Llama 3 available locally

## Configuration

Configure the following environment variables in a local `.env` file:

- APP_NAME
- ENV
- GITLAB_URL
- GITLAB_TOKEN
- GITLAB_PROJECT_ID

Do not commit `.env` or credentials to Git.

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn application.mainapp:application --reload
```

The API will be available at:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `/health` | Application health check |
| `/gitlab/status` | GitLab connectivity and project count |
| `/gitlab/pipeline/status` | Retrieve pipeline status |
| `/release/decision` | Evaluate release decision and generate AI explanation |

## Infrastructure

Terraform configuration provisions:

- AWS VPC
- Public subnet
- Internet Gateway
- Route table
- Security group
- EC2 instance

Run Terraform commands from the `infra` directory:

```bash
terraform init
terraform plan
terraform apply
```

Review network access rules before provisioning public infrastructure.

## Project Scope

This is an early-stage learning project exploring the integration of CI/CD pipeline information, rule-based release decisions, local LLM explanations, containerization, and AWS infrastructure automation.

It is not intended to be a production-ready release management platform.
