# AI Real Estate Agent

AWS Bedrock agent designed to research and analyze real-estate information using external search and application data sources.

The project uses Amazon Bedrock Agents with Amazon Nova Pro as the foundation model and extends the agent with custom AWS Lambda action groups. Infrastructure, permissions, memory configuration, and deployment are defined as code using the Serverless Framework and AWS CloudFormation resources.

## Architecture

```text
                     ┌─────────────────────┐
                     │ Application / Client│
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Amazon Bedrock Agent│
                     │   Amazon Nova Pro   │
                     └──────────┬──────────┘
                                │
                         Action Groups
                                │
                                ▼
                     ┌─────────────────────┐
                     │     AWS Lambda      │
                     │     Web Search      │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Tavily Search API │
                     └─────────────────────┘
```

The agent combines model reasoning with external tools rather than relying exclusively on information available to the foundation model.

## Agent Capabilities

The agent is configured around several real-estate research tasks, including:

* property and feature analysis
* area research
* comparable-property analysis
* public web research

Agent behavior is divided into dedicated prompt files under `prompts/`, allowing individual capabilities and instructions to evolve independently from the infrastructure definition.

## Tool Integration

### Web Search

The Bedrock Agent exposes a `web_search` action group backed by AWS Lambda.

When the agent determines that external information is required, it can invoke the Lambda function with a search query. The Lambda uses Tavily to retrieve public web results and returns structured results to the Bedrock Agent action-group interface.

```text
Bedrock Agent
     │
     │ web_search(query)
     ▼
AWS Lambda
     │
     ▼
Tavily
     │
     ▼
Structured search results
     │
     └──────────────► Bedrock Agent
```

The Lambda integration is implemented in Python.

## Agent Memory

Bedrock session-summary memory is enabled to preserve useful context across interactions.

The configuration retains recent session summaries and defines a 30-day memory storage period.

## Infrastructure as Code

The project is deployed using Serverless Framework v4 with additional AWS resources defined through CloudFormation.

The stack provisions and configures:

* Amazon Bedrock Agent
* Bedrock Agent Alias
* AWS Lambda action-group integration
* IAM roles and invocation permissions
* SSM Parameter Store entries
* Amazon S3 storage
* agent memory configuration
* cross-account agent invocation support

Agent and alias identifiers are published to AWS Systems Manager Parameter Store so other application components can discover the deployed resources without hard-coded IDs.

## Cross-Account Integration

The stack includes an IAM role for invoking the Bedrock Agent from another AWS account.

This allows the AI service to remain independently deployed while authorized application infrastructure can assume a dedicated role and invoke the agent.

## CI/CD

Deployment is automated through GitHub Actions.

The deployment workflow:

1. configures the Python and Node.js environments
2. loads deployment credentials and external API configuration
3. discovers dependent infrastructure through AWS CloudFormation outputs
4. packages Python Lambda dependencies
5. packages and deploys the Serverless stack
6. retrieves the deployed Bedrock Agent identifiers from SSM
7. updates the agent alias

Sensitive credentials and API keys are provided through GitHub Actions secrets and environment variables.

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── deploy.yaml
├── prompts/
│   ├── instructions.txt
│   ├── description.txt
│   ├── features.txt
│   ├── area.txt
│   └── comparables.txt
├── schemas/
│   └── web_search_payload.yml
├── src/
│   ├── search_lambda/
│   └── package_lambdas.sh
├── serverless.yml
└── README.md
```

## Configuration

Deployment requires environment-specific configuration for AWS and external integrations.

Relevant configuration includes:

```text
STAGE
TAVILY_API_KEY
ALB_DNS
AWS_REGION
```

AWS resource identifiers generated during deployment are stored in SSM Parameter Store rather than embedded directly into dependent application components.

## Technologies

**AI:** Amazon Bedrock Agents, Amazon Nova Pro
**Backend:** Python, AWS Lambda
**Search:** Tavily
**Cloud:** AWS Bedrock, Lambda, IAM, S3, SSM Parameter Store
**Infrastructure:** Serverless Framework, CloudFormation, YAML
**CI/CD:** GitHub Actions

## Project Context

This agent was developed as the AI research component of a larger real-estate application.

The design separates the AI agent from the application's primary backend and data-collection services. External capabilities are exposed to the agent through action groups, allowing additional tools and data sources to be integrated without embedding their implementation directly into the agent.
