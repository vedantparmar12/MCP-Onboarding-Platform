# MCP Onboarding Platform

## Overview

The **MCP Onboarding Platform** is an AI-powered solution designed for automating financial services onboarding. By leveraging advanced tools like document analysis, compliance validation, and risk prediction, the platform enhances the onboarding process efficiently.

## Features

- **Document Analysis**: Analyze onboarding documents using GenAI for compliance and risk assessment.
- **Compliance Validation**: Validate regulatory compliance of onboarding processes.
- **Risk Prediction**: Predict risks associated with onboarding using machine learning.
- **Conversational Interface**: Engage with an AI-powered conversational assistant for interactive onboarding.

## Technologies Used

- **FastAPI**: Asynchronous web framework for building the server.
- **Python 3.11**: Primary programming language.
- **Sentry**: For error monitoring and tracking.
- **Prometheus & Grafana**: Monitoring and visualization.
- **Redis & PostgreSQL**: Caching and database solutions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vedantparmar12/MCP-Onboarding-Platform.git
   cd MCP-Onboarding-Platform
   ```

2. Set up the environment variables. Use the `.env.example` as a template:
   ```bash
   cp .env.example .env
   ```

3. Build and run the services using Docker:
   ```bash
   docker-compose up --build
   ```

## Usage

- Access the API documentation at `http://localhost:8000/docs` for detailed API usage.
- For testing, use FastAPI's interactive API docs or external tools like Postman.

## Configuration

Ensure the following environment variables are configured correctly:

- **API Keys**: Configure ANTHROPIC_API_KEY, OPENAI_API_KEY, and other necessary keys.
- **Database**: Set the DATABASE_URL for PostgreSQL.

## Testing

Run tests using `pytest`:
```bash
pytest tests
```

## Contributing

We welcome contributions! Please fork the repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License.
