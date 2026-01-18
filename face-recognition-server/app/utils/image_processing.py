from fastapi import UploadFile
import os
import uuid
from app.config import settings


async def save_uploaded_image(file: UploadFile) -> str:
    """Save uploaded image to temporary location"""
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    # Save file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return file_path


def cleanup_temp_image(file_path: str):
    """Delete temporary image file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Failed to cleanup temp file {file_path}: {e}")
