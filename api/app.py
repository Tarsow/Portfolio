from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="FastAPI Simple Static + API")

# mount static directory at /static
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render a simple template that references a static CSS file.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/download", response_class=FileResponse)
async def download_example():
    """
    Return a file from the static folder for download.
    """
    file_path = BASE_DIR / "static" / "example.txt"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    # FileResponse will stream the file efficiently
    return FileResponse(path=file_path, filename="example.txt", media_type="text/plain")


@app.post("/api/echo")
async def api_echo(payload: dict):
    """
    Simple JSON echo endpoint to test API behavior.
    """
    return JSONResponse({"echo": payload})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Accept an uploaded file and save it under static/uploads/.
    Useful to test multipart/form-data uploads.
    """
    uploads_dir = BASE_DIR / "static" / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)

    dest = uploads_dir / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "saved_to": str(dest.relative_to(BASE_DIR))}
