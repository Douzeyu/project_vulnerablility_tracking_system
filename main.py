import requests

from collections import defaultdict
from fastapi import FastAPI, UploadFile
from typing import Union

from models import Package, Dependency, Project

app = FastAPI()
project_dict = defaultdict(Project)

@app.get("/")
def read_root() -> str:
    return "This a \"Python Project Vulnerability Tracking API System exercise\" for Morgan Stanley Interview."

@app.post("/project/")
async def create_projects(name: str, description: str, requirement: UploadFile) -> str:
    content = await requirement.read() # Read the content of the file
    dependencies = {}
    for line in content.decode("utf-8").split("\r\n"): # Split the file content by lines and loop on each line 
        if "==" in line and line[0] != "#": # Filter out the comment line in the file
            dependency = line.split("==")
            package = Package(name=dependency[0])
            dependencies[dependency[0]] = Dependency(package=package, version=dependency[1])
    project_dict[name] = Project(name=name, description=description, dependencies=dependencies)
    return "Project successfully created!"

@app.get("/project/")
async def get_projects() -> dict[str, bool]:
    project_vulnerability = {}
    for name, project in project_dict.items():
        project_vulnerability[name] = False
        dependency_list = [dependency.model_dump() for dependency in project.dependencies.values()]
        
        # prepare the curl request to OSV server
        headers = {"Content-Type": "application/json"}
        payload = {"queries": dependency_list}
        response = requests.post("https://api.osv.dev/v1/querybatch", json=payload, headers=headers)
        match response.status_code:
            case 200:
                for vulnerable in response.json()["results"]:
                    if vulnerable:
                        project_vulnerability[name] = True
                        break
            case _:
                raise RuntimeError(
                    "Error occurred while sending request to OSV server. Status code: " + str(response.json()["code"]) + ". Error message: " + response.json()["message"]
                )
        
    return project_vulnerability

@app.get("/project/{project_name}")
async def get_project_dependencies(project_name: str) -> dict[str, bool]:
    dependency_vulnerability = {}
    project = project_dict[project_name]
    dependency_list = [dependency.model_dump() for dependency in project.dependencies.values()]
        
    # prepare the curl request to OSV server
    headers = {"Content-Type": "application/json"}
    payload = {"queries": dependency_list}
    response = requests.post("https://api.osv.dev/v1/querybatch", json=payload, headers=headers)
    match response.status_code:
        case 200:
            index = 0
            for vulnerable in response.json()["results"]:
                dependency_name = list(project.dependencies.keys())[index]
                if vulnerable:
                    dependency_vulnerability[dependency_name] = True
                else:
                    dependency_vulnerability[dependency_name] = False
                index += 1
        case _:
            raise RuntimeError(
                "Error occurred while sending request to OSV server. Status code: " + str(response.json()["code"]) + ". Error message: " + response.json()["message"]
            )

    return dependency_vulnerability