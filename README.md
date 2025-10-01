# project_vulnerability_tracking_system

## Objective:
Develop a Python application using FastAPI that allows users to track vulnerabilities within their Python projects.

## User Story:
As a Python developer, I want to track vulnerabilities in my project's dependencies to ensure its security and reliability.
 
## Functional Requirements:

### 1. Project Endpoints:

- Create project: Allow users to create a Python project by submitting a name, description, and requirements.txt file.
- Get projects: List users’ projects. Identify vulnerable projects.
- Get project dependencies: Retrieve the dependencies for a specified project and identify which of these dependencies are vulnerable.
 
### 2.Dependency Endpoints:

- Get dependencies: List all dependencies tracked across the user’s projects. Identify vulnerable dependencies.
- Get dependency: Provide details about a specific dependency, including usage and associated vulnerabilities.
