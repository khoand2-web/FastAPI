# app/utils/file_upload.py
from pathlib import Path
from fastapi import UploadFile
from typing import Tuple


def save_upload_file(upload_file: UploadFile, destination: Path) -> Tuple[str, int]:
    """
    Save uploaded file to destination path.

    Args:
        upload_file: UploadFile from FastAPI.
        destination: destination Path.

    Returns:
        Tuple of filename and size in bytes.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as buffer:
        content = upload_file.file.read()
        buffer.write(content)
    return destination.name, destination.stat().st_size
