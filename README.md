# PDF Generator Microservice

## Overview

The **PDF Generator Microservice** is a FastAPI-based application that converts HTML content into PDFs asynchronously. It leverages Celery for task management and Redis as a message broker, ensuring efficient and scalable PDF generation.

## Features

- **Asynchronous PDF Generation**: Submit HTML content and retrieve the generated PDF once processing is complete.
- **Task Management**: Monitor the status of PDF generation tasks.
- **Dockerized Deployment**: Easily deployable using Docker and Docker Compose.
- **Continuous Integration**: Integrated with GitHub Actions for automated testing and versioning.

## Architecture

- **FastAPI**: Serves as the web framework for handling HTTP requests.
- **Celery**: Manages asynchronous task queues for PDF generation.
- **Redis**: Acts as the message broker between FastAPI and Celery.
- **WeasyPrint**: Converts HTML content to PDF.
- **PostgreSQL**: (Optional) Database for persisting task data.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/nraynes/pdf-generator.git
   cd pdf-generator
   ```

2. **Set Up Environment Variables**:

   Create a `.env` file in the project root with the following content as necessary for your environment.
   ```bash
   REDIS_URL=redis://redis:6379/0
   DATABASE_URL=postgresql://postgres:password@db:5432/pdfs
   ```

3. **Build and Start the Services**:

   ```bash
   docker-compose up --build
   ```

   This command will build and start the FastAPI application, Redis, and Celery worker.

## Usage

### 1. Generate a PDF

Submit a POST request to `/api/v1/generate` with the HTML content as a file:

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data=@sample.html;type=text/html'
```

**Response**:

```json
{
  "job_id": "your-job-id"
}
```

### 2. Check Task Status

Retrieve the status of a PDF generation task using the `job_id`:

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/status/your-job-id' \
  -H 'accept: application/json'
```

**Response**:

```json
{
  "status": "SUCCESS"
}
```

### 3. Download the Generated PDF

Once the task is complete, download the PDF:

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/download/your-job-id' \
  -H 'accept: application/pdf' \
  -o output.pdf
```

## Configuration

### Environment Variables

- `REDIS_URL`: URL for the Redis server. Default is `redis://redis:6379/0`.

### Docker Compose Services

- **app**: The FastAPI application.
- **redis**: Redis server for message brokering.
- **worker**: Celery worker for processing tasks.

## Development

### Setting Up the Development Environment

1. **Install Dependencies**:

   ```bash
   pip install -r requirements-dev.txt
   ```

   MacOS users (Add this to your .bashprofile or .zprofile for global use, PYTHONPATH is path to project clone):
   ```bash
   brew install cairo pango gdk-pixbuf libffi libxml2 libxslt gobject-introspection
   export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig:$PKG_CONFIG_PATH"
   export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
   export PYTHONPATH=$(pwd)
   ```
   
2. **Run the Application Locally**:

   ```bash
   uvicorn app.main:app --reload
   ```

3. **Start the Celery Worker**:

   ```bash
   celery -A app.workers.tasks worker --loglevel=info
   ```

### Linting and Formatting

- **Linting**: The project uses `flake8` for linting.

  ```bash
  flake8 app
  ```

- **Formatting**: The project uses `black` for code formatting.

  ```bash
  black app
  ```

### Testing

Tests are located in the `tests` directory. Run tests using `pytest`:

```bash
pytest tests
```

### Versioning

The project uses [Commitizen](https://commitizen-tools.github.io/commitizen/) for versioning. To bump the version:

```bash
cz bump --changelog
```

## Continuous Integration

The project integrates with GitHub Actions for:

- **Linting**: Ensures code quality.
- **Testing**: Runs the test suite.
- **Versioning**: Automates version bumps and changelog generation.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'feat: add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.
