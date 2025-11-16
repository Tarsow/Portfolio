# app.py
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# monta a pasta public/ em /static
app.mount("/static", StaticFiles(directory="public"), name="static")

# configurar templates (pasta templates/)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    # renderiza templates/index.html
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/{api_name}")
def interact_api(api_name, q:str = "nothing"):
    return JSONResponse({"api_name": api_name, "q": q})


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return JSONResponse({"item_id": item_id, "q": q})
