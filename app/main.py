from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils import process_image_or_pdf
import os

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    file_path = f"img/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract the file name without extension
    base_name, _ = os.path.splitext(file.filename)

    # Determine if the file is an image or a PDF
    file_type = file.content_type
    if file_type == "application/pdf":
        file_format = "pdf"
    elif file_type.startswith("image/"):
        file_format = "image"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload an image or a PDF.")

    # Process the file (either image or PDF)
    output_image_path, output_json_path = process_image_or_pdf(file_path, file_format, base_name)

    return {
        "output_image": output_image_path,
        "output_json": output_json_path
    }
