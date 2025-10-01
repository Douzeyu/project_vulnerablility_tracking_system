from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root() -> str:
    return "This a \"Python Project Vulnerability Tracking API System exercise\" for Morgan Stanley Interview."