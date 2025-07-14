# MCP Onboarding Platform

## Overview

The **MCP Onboarding Platform** is an AI-powered, enterprise-grade solution designed to automate and streamline financial services onboarding. This platform leverages a sophisticated suite of tools for intelligent document analysis, real-time compliance validation, and predictive risk assessment, significantly enhancing operational efficiency and accuracy.

Built with a modern, asynchronous architecture, the platform offers a robust and scalable solution for financial institutions looking to modernize their client onboarding processes. It integrates seamlessly with existing workflows and provides a secure, monitored, and feature-rich environment.

***

## Features

-   **Document Analysis**: Utilizes Generative AI to extract, interpret, and validate information from a wide range of financial documents, including PDFs and images.
-   **Compliance Validation**: Automates regulatory adherence checks against multiple jurisdictions such as **MAS**, **HKMA**, and **SEC**, ensuring that all onboarding activities meet the required legal frameworks.
-   **Risk Prediction**: Employs a machine learning model (**RandomForestClassifier**) and GenAI-driven insights to predict and categorize potential client-associated risks as low, medium, or high.
-   **Conversational Interface**: Offers an AI-powered conversational assistant to guide users through the onboarding process, providing real-time support and information.
-   **Multi-Agent System**: A sophisticated system that coordinates multiple AI agents for comprehensive risk analysis, ensuring a more thorough and accurate assessment.
-   **Feature Flagging**: Enables gradual rollouts and A/B testing of new features like `genai_analysis` and a `multi_agent_system` for controlled deployments and continuous improvement.
-   **Comprehensive Monitoring**: Integrated with **Prometheus** and **Grafana** for real-time metrics on application performance, including document processing rates, API request latency, and active user sessions.

***

## Technologies Used

-   **Backend**: Python 3.11, FastAPI
-   **AI & Machine Learning**: Anthropic, Scikit-learn, PyPDF2
-   **Database & Caching**: PostgreSQL, Redis
-   **Containerization & Orchestration**: Docker, Kubernetes
-   **CI/CD**: GitHub Actions, Docker Hub
-   **Monitoring & Error Tracking**: Prometheus, Grafana, Sentry
-   **Cloud Deployment**: Cloudflare Workers

***

## System Architecture

The MCP Onboarding Platform is built around a central FastAPI server that orchestrates various AI-powered tools and services.

### Core Server (`src/server.py`)

The heart of the application is the `OnboardingMCPServer` class, which initializes and manages all core components:
* **Authentication**: `AuthManager` handles user authentication using JWT.
* **Input Validation**: `InputValidator` ensures that all incoming requests and file uploads meet the required security and format standards.
* **Metrics Collection**: `MetricsCollector` gathers and exposes metrics for Prometheus.
* **Caching**: `CacheManager` provides a caching layer using Redis to improve performance.
* **Database**: `DatabaseManager` manages the connection to the PostgreSQL database.
* **Feature Flags**: `FeatureFlags` allows for dynamic enabling/disabling of features for different users.
* **AI Tools**: The server loads a suite of tools for various onboarding tasks:
    * `DocumentAnalyzerTool`
    * `ComplianceValidatorTool`
    * `RiskPredictorTool`
    * `ConversationalOnboardingTool`

### Cloudflare Worker (`src/worker.js`)

A Cloudflare Worker acts as the entry point for handling requests, providing routing, authentication, and monitoring before they hit the main application. It is configured in `wrangler.toml` with bindings for:
* **KV Namespaces**: For session storage and caching (`SESSIONS`, `CACHE`).
* **D1 Database**: For the primary database (`ONBOARDING_DB`).
* **R2 Storage**: For storing uploaded documents (`DOCUMENTS`).

***

## Getting Started

### Prerequisites

* Docker & Docker Compose
* Git
* Python 3.11

### Installation and Setup

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/vedantparmar12/MCP-Onboarding-Platform.git](https://github.com/vedantparmar12/MCP-Onboarding-Platform.git)
    cd MCP-Onboarding-Platform
    ```

2.  **Set Up Environment Variables**:
    Create a `.env` file by copying the example file. This is crucial for the application to function correctly.
    ```bash
    cp .env.example .env
    ```
    Populate the `.env` file with your credentials and configuration details. See the **Environment Variables** section below for a full list of required variables.

3.  **Build and Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    This command builds the Docker containers and starts all services as defined in `docker-compose.yml`, including the FastAPI application, PostgreSQL database, Redis instance, Prometheus, and Grafana.

4.  **Access the Application**:
    * **API Docs**: `http://localhost:8000/docs`
    * **Grafana Dashboard**: `http://localhost:3000`
    * **Prometheus Metrics**: `http://localhost:9090`

***

## Environment Variables

The following table details the environment variables required to run the platform. These are defined across various configuration files (`docker-compose.yml`, `wrangler.toml`, `k8s/deployment.yml`).

| Variable | Description | Example |
|---|---|---|
| `ANTHROPIC_API_KEY` | API key for the Anthropic (Claude) service. | `your_anthropic_api_key` |
| `SENTRY_DSN` | DSN for Sentry error tracking. | `https://your-dsn@sentry.io/12345` |
| `DATABASE_URL` | Connection string for the PostgreSQL database. | `postgresql://postgres:password@postgres:5432/onboarding_db` |
| `REDIS_HOST` | Hostname for the Redis server. | `redis` |
| `REDIS_PORT` | Port for the Redis server. | `6379` |
| `JWT_SECRET_KEY` | Secret key for generating and validating JWTs. | `your_super_secret_key` |
| `POSTGRES_DB` | Name of the PostgreSQL database. | `onboarding_db` |
| `POSTGRES_USER` | Username for the PostgreSQL database. | `postgres` |
| `POSTGRES_PASSWORD` | Password for the PostgreSQL database. | `password` |
| `CLOUDFLARE_API_TOKEN` | API token for deploying to Cloudflare Workers. | `your_cloudflare_api_token` |
| `DOCKER_USERNAME` | Username for Docker Hub for pushing images. | `your_docker_username` |
| `DOCKER_PASSWORD` | Password for Docker Hub. | `your_docker_password` |
| `KUBECONFIG` | Base64 encoded kubeconfig file for Kubernetes deployment. | `(base64 encoded string)` |
| `SLACK_WEBHOOK` | Webhook URL for Slack notifications. | `https://hooks.slack.com/services/...` |

***

## CI/CD and Automation

The project uses GitHub Actions for continuous integration and deployment. The workflow is defined in `.github/workflows/deploy.yml` and consists of several jobs:

1.  **`test`**:
    * Spins up `redis` and `postgres` service containers for integration testing.
    * Installs Python and system dependencies like `tesseract-ocr`.
    * Runs linting (`flake8`, `black`), type checking (`mypy`), and unit tests (`pytest`).
    * Uploads code coverage reports to Codecov.

2.  **`security`**:
    * Runs a security scan on the codebase using `securecodewarrior/github-action-add-sarif`.

3.  **`build`**:
    * Builds and pushes a Docker image to Docker Hub with tags for `latest` and the specific Git SHA.

4.  **`deploy`**:
    * This job runs only on pushes to the `main` branch.
    * Deploys the application to **Cloudflare Workers** using the `wrangler` CLI.
    * Deploys to a **Kubernetes** cluster by applying the new image tag to the deployment.

5.  **`notify`**:
    * Sends a notification to a Slack channel with the status of the deployment (success or failure).

***

## Monitoring and Error Tracking

### Sentry

Sentry is integrated for real-time error tracking in both the main Python application and the Cloudflare Worker.

* In `src/server.py`, the Sentry SDK is initialized with `FastApiIntegration` and `SqlalchemyIntegration` to automatically capture errors from the web server and database interactions.
* In `src/worker.js`, Sentry is initialized to capture any unhandled exceptions within the Cloudflare Worker.
* The `SENTRY_DSN` environment variable must be set for error reporting to work.

### Prometheus & Grafana

The `docker-compose.yml` file sets up Prometheus and Grafana containers for monitoring.

* **Prometheus** is configured in `config/prometheus.yml` to scrape metrics from the `/metrics` endpoint of the application, as well as from the Redis and Postgres services.
* **Grafana** can be configured with dashboards to visualize the metrics collected by Prometheus. The service is available at `http://localhost:3000`.

***

## Testing

The project includes a comprehensive test suite using `pytest`. To run the tests locally:

```bash
pytest tests/
```

## Contributing

We welcome contributions from the community. Please fork the repository and submit pull requests with improvements or bug fixes.

## License

This project is licensed under the MIT License.
