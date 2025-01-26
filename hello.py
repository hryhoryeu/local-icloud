from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
from pathlib import Path
from typing import List

app = FastAPI()

# Paths for storing images
UPLOAD_DIR = Path("uploads")
ORIGINAL_DIR = UPLOAD_DIR / "original"
PREVIEW_DIR = UPLOAD_DIR / "previews"
THUMBNAIL_DIR = UPLOAD_DIR / "thumbnails"

ORIGINAL_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
PREVIEW_DIR.mkdir(exist_ok=True)
THUMBNAIL_DIR.mkdir(exist_ok=True)


def resize_image(image_path: str, output_path: str, size: tuple):
    """Resize the image and save it to the output path."""
    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(output_path)


@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload multiple images and create resized versions."""
    results = []
    for file in files:
        # Save original file
        original_path = ORIGINAL_DIR / file.filename
        with open(original_path, "wb") as buffer:
            buffer.write(await file.read())

        # Create preview (800x800 max) and thumbnail (150x150 max)
        preview_path = PREVIEW_DIR / file.filename
        thumbnail_path = THUMBNAIL_DIR / file.filename

        resize_image(original_path, preview_path, (600, 600))
        resize_image(original_path, thumbnail_path, (200, 200))

        # Add file paths to results
        results.append(
            {
                "original": f"/images/original/{file.filename}",
                "preview": f"/images/previews/{file.filename}",
                "thumbnail": f"/images/thumbnails/{file.filename}",
            }
        )

    return {"message": "Files uploaded and processed successfully!", "files": results}


@app.get("/images/{image_type}/{filename}")
async def get_image(image_type: str, filename: str):
    """Serve an image (original, preview, or thumbnail)."""
    if image_type not in ["original", "previews", "thumbnails"]:
        return {
            "error": "Invalid image type. Must be one of 'original', 'previews', or 'thumbnails'."
        }

    file_path = UPLOAD_DIR / image_type / filename

    if not file_path.exists():
        return {"error": "File not found."}

    return FileResponse(file_path)


@app.get("/")
async def read_root():
    """Landing page."""
    return {"message": "Welcome to the Image Upload API"}
