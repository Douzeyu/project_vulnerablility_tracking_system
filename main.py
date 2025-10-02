import requests

from collections import defaultdict
from fastapi import FastAPI, UploadFile
from typing import Any

from models import Package, Dependency, Project
from settings import settings

app = FastAPI()
project_dict = defaultdict(Project)
dependency_vulnerability = defaultdict(bool)

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
        
        # prepare the curl request to OSV service
        headers = {"Content-Type": "application/json"}
        payload = {"queries": dependency_list}
        response = requests.post(settings.CHECK_MULTIPLE_PACKAGES, json=payload, headers=headers)
        # check the status code
        match response.status_code:
            case 200:
                for vulnerable in response.json()["results"]:
                    if vulnerable:
                        project_vulnerability[name] = True
                        break
            case _:
                # raise runtime error if the status is not 200
                raise RuntimeError(
                    "Error occurred while sending request to OSV service. Status code: " + str(response.json()["code"]) + ". Error message: " + response.json()["message"]
                )
        
    return project_vulnerability

@app.get("/project/{project_name}/")
async def get_project_dependencies(project_name: str) -> dict[str, bool]:
    
    if project_name not in project_dict:
        raise ValueError("Project doesn't exist! Please create the project first in order to execute the vulnerability tracking.")

    dependency_vulnerability = {}
    project = project_dict[project_name]
    dependency_list = [dependency.model_dump() for dependency in project.dependencies.values()]
        
    # prepare the curl request to OSV service
    headers = {"Content-Type": "application/json"}
    payload = {"queries": dependency_list}
    response = requests.post(settings.CHECK_MULTIPLE_PACKAGES, json=payload, headers=headers)
    # check the status code
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
            # raise runtime error if the status is not 200
            raise RuntimeError(
                "Error occurred while sending request to OSV service. Status code: " + str(response.json()["code"]) + ". Error message: " + response.json()["message"]
            )

    return dependency_vulnerability

@app.get("/dependency/")
async def get_dependencies() -> dict[tuple[str, str], bool]:
    dependency_vulnerability = {}
    for project in project_dict.values():

        dependency_list = [ dependency for dependency in project.dependencies.values() if (dependency.package.name, dependency.version) not in dependency_vulnerability]

        # if denpendency list is not empty, send request to OSV service for vulnerability tracking.
        if dependency_list:
            # prepare the curl request to OSV service
            headers = {"Content-Type": "application/json"}
            payload = {"queries": [ dependency.model_dump() for dependency in dependency_list]}
            response = requests.post(settings.CHECK_MULTIPLE_PACKAGES, json=payload, headers=headers)
            # check the status code
            match response.status_code:
                case 200:
                    index = 0
                    for vulnerable in response.json()["results"]:
                        dependency = dependency_list[index]
                        if vulnerable:
                            dependency_vulnerability[(dependency.package.name, dependency.version)] = True
                        else:
                            dependency_vulnerability[(dependency.package.name, dependency.version)] = False
                        index += 1
                case _:
                    # raise runtime error if the status is not 200
                    raise RuntimeError(
                        "Error occurred while sending request to OSV service. Status code: " + str(response.json()["code"]) + ". Error message: " + response.json()["message"]
                    )

    return dependency_vulnerability

@app.get("/dependency/{dependency_name}/{dependency_version}/")
async def get_dependencies(dependency_name: str, dependency_version: str) -> dict[str, Any]:
    dependency = Dependency(package=Package(name=dependency_name), version=dependency_version)
    project_list = []
    for name, project in project_dict.items():
        if (dependency_name in project.dependencies) and (project.dependencies[dependency_name].version == dependency_version):
            project_list.append(name)

    # prepare the curl request to OSV service
    headers = {"Content-Type": "application/json"}
    response = requests.post(settings.CHECK_SINGLE_PACKAGE, json=dependency.model_dump(), headers=headers)
    # check the status code
    match response.status_code:
        case 200:
            if response.json():
                vulnerabilities = response.json()["vulns"]
            else:
                vulnerabilities = "This dependency is not vulnerable."
        case _:
            # raise runtime error if the status is not 200
            raise RuntimeError(
                "Error occurred while sending request to OSV service. Status code: " + str(response.json()["code"]) + ". Error message: " + response.json()["message"]
            )
    
    return {"usage": project_list, "vulnerabilities": vulnerabilities}
