# Project Vulnerability Tracking System

## Objective:
Develop a Python application using FastAPI that allows users to track vulnerabilities within their Python projects.

## Rquirement

This project has the following requirements to be available on your system:

- [uv](https://docs.astral.sh/uv/) for Python project management
- [Docker Desktop](https://docs.docker.com/desktop/) (or Docker Engine on Linux)
- [Git LFS](https://git-lfs.com/)

## Getting Started

This project contains a `Dockerfile` as well as a `docker-compose.yml` to run it as a container.

### Step 1: Create the `.env` file

Copy the `.env.sample` to `.env` and adjust the values as necessary.

```shell
cp .env.sample .env
```

### Step 2: Start the container

You can then bring up the container:

```shell
docker compose up
```

or separately by:

```shell
docker compose up cache
```

then

```shell
docker compose up app
```

Once the image is built and the container running, you can access the project API documentation via `http://localhost:8000/docs` from your browser.

## User Guide:

### 1. Project Endpoints:

- Create project: Allow users to create a Python project by submitting a name, description, and requirements.txt file.

eg:

```shell
curl --location --request POST 'http://localhost:8000/project?project_name=test2&project_description=test' --form 'requirement=@"/F:/requirement2.txt"'
```

- Get projects: List users’ projects. Identify vulnerable projects.

eg:

```shell
curl --location --request GET 'http://localhost:8000/project/'
```

- Get project dependencies: Retrieve the dependencies for a specified project and identify which of these dependencies are vulnerable.

eg:

```shell
curl --location --request GET 'http://localhost:8000/project/{your_project_name}'
```
 
### 2.Dependency Endpoints:

- Get dependencies: List all dependencies tracked across the user’s projects. Identify vulnerable dependencies.

eg:

```shell
curl --location --request GET 'http://localhost:8000/dependency/'
```

- Get dependency: Provide details about a specific dependency, including usage and associated vulnerabilities.

eg:

```shell
curl --location --request GET 'http://localhost:8000/dependency/{dependency_name}/{dependency_version}'
```
