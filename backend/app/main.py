from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.repo_service import clone_repository, get_python_files, cleanup_repo
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI GitHub Repo Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class AnalyzeRequest(BaseModel):
    github_url: str


@app.post("/analyze")
def analyze_repo(request: AnalyzeRequest):
    try:
        repo_path, repo_id = clone_repository(request.github_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to clone repo: {str(e)}")

    python_files = get_python_files(repo_path)

    if not python_files:
        raise HTTPException(status_code=400, detail="No Python files found in this repository.")

    return {
        "repo_id": repo_id,
        "total_python_files": len(python_files),
        "files": python_files
    }