from pathlib import Path

# List the files
def list_files(project_path: str)->list[str]:
    path = Path(project_path)

    if not path.exists():
        raise FileNotFoundError(f"Project Not found:{project_path}")

    if not path.is_dir():
        raise ValueError(f"Directory Does not Exists: {project_path}")
    ignored = {".git",".venv","venv","__pycache__","node_modules"}

    files = []
    for file in path.rglob("*"):
        if file.is_file() and not any(part in ignored for part in file.parts):
            files.append(str(file))
    return files

# Read the files
def read_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    return path.read_text(encoding="utf-8")

# Write Files 
def write_file(file_path: str, content: str) -> str:
    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"File written successfully: {file_path}"