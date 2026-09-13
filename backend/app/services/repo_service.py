import os
import shutil
import uuid
from git import Repo

BASE_CLONE_DIR = "app/cloned_repos"

# folders/files to skip entirely
IGNORE_DIRS = {".git", "node_modules", "__pycache__", "venv", ".venv", "dist", "build"}
IGNORE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".exe", ".pyc"}
ALLOWED_EXTENSIONS = {".py"}  # Python-only scope for now


def clone_repository(github_url: str) -> str:
    """Clones a GitHub repo into a unique local folder and returns its path."""
    repo_id = str(uuid.uuid4())[:8]
    target_path = os.path.join(BASE_CLONE_DIR, repo_id)

    os.makedirs(BASE_CLONE_DIR, exist_ok=True)
    Repo.clone_from(github_url, target_path)

    return target_path, repo_id


def get_python_files(repo_path: str) -> list[str]:
    """Walks the cloned repo and returns paths of relevant Python files only."""
    python_files = []

    for root, dirs, files in os.walk(repo_path):
        # modify dirs in-place to skip ignored folders (this makes os.walk skip them)
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in ALLOWED_EXTENSIONS:
                full_path = os.path.join(root, file)
                python_files.append(full_path)

    return python_files


def cleanup_repo(repo_path: str):
    """Deletes a cloned repo folder (call this after processing if you don't want to keep it)."""
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)