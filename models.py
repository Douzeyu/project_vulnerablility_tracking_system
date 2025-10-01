from pydantic import BaseModel

class Package(BaseModel):
    name: str
    ecosystem: str = "PyPI"

class Dependency(BaseModel):
    package: Package
    version: str

class Project(BaseModel):
    name: str
    description: str
    dependencies: dict[str, Dependency]