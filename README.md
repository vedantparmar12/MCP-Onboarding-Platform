# MCP Onboarding Platform

## Overview

The **MCP Onboarding Platform** is an AI-powered solution designed for automating financial services onboarding. This platform leverages advanced tools for document analysis, compliance validation, and risk prediction to streamline the onboarding process efficiently.

## Features

- **Document Analysis**: Use GenAI to analyze onboarding documents for compliance and risk.
- **Compliance Validation**: Ensure regulatory compliance of onboarding processes.
- **Risk Prediction**: Leverage ML to predict risks in onboarding.
- **Conversational Interface**: Interact with an AI-powered conversational assistant.

## Technologies Used

- **FastAPI**: Asynchronous web framework.
- **Python 3.11**: Core programming language.
- **Sentry**: Error monitoring.
- **Prometheus \u0026 Grafana**: Monitoring and visualization.
- **Redis \u0026 PostgreSQL**: Caching and database solutions.

## Prerequisites

- **Docker \u0026 Docker Compose**: For container management.
- **Git**: Version control system.
- **Python 3.11**: Language runtime.

Ensure these tools are installed and available in your PATH.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/vedantparmar12/MCP-Onboarding-Platform.git
   cd MCP-Onboarding-Platform
   ```

2. **Set Up Environment Variables**
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` to configure the required API keys and database URL:
     ```
     ANTHROPIC_API_KEY=your_anthropic_api_key_here
     OPENAI_API_KEY=your_openai_api_key_here
     DATABASE_URL=postgresql://user:password@localhost:5432/onboarding_db
     REDIS_URL=redis://localhost:6379
     ```

3. **Build and Start the Project Using Docker Compose**
   ```bash
   docker-compose up --build
   ```

   - This command will build the containers and start the services including the application, Redis, PostgreSQL, Prometheus, and Grafana.

4. **Access the Application**
   - Visit `http://localhost:8000/docs` to view the API documentation.
   - Explore the AI tools, and perform document analysis or compliance validation.

## Usage

- Access the API documentation for detailed instructions on each endpoint.
- Use tools like Postman to test API calls.

## Configuration

- **API Keys**: Ensure ANTHROPIC_API_KEY and OPENAI_API_KEY are correctly set in `.env`.
- **Database**: Update DATABASE_URL in `.env` to point to your PostgreSQL instance.

## Testing

- Run the test suite using pytest:
  ```bash
  pytest tests
  ```

## Contributing

We welcome contributions from the community. Please fork the repository and submit pull requests with improvements or bug fixes.

## License

This project is licensed under the MIT License.
