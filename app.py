# app.py
from typing import Union
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import *
from datetime import datetime



app = FastAPI()

# monta a pasta public/ em /static
app.mount("/static", StaticFiles(directory="public"), name="static")

# configurar templates (pasta templates/)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    # renderiza templates/index.html
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/robots.txt", response_class=Response)
def robots():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Sitemap: https://tarsow.dev/sitemap.xml\n"
    )
    return Response(content, media_type="text/plain")

@app.get("/ads.txt", response_class=Response)
def ads():
    content = (
        "google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n"
    )
    return Response(content, media_type="text/plain")

@app.get("/sitemap.xml", response_class=Response)
def sitemap():
    base_url = "https://tarsow.dev"

    urls = [
        "/",
        "progress-knight"
    ]

    xml_items = ""
    now = datetime.utcnow().strftime("%Y-%m-%d")

    for url in urls:
        xml_items += f"""
    <url>
        <loc>{base_url}{url}</loc>
        <lastmod>{now}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>"""

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}
</urlset>
"""

    return Response(content=xml, media_type="application/xml")

@app.get("/progress-monster")
def progress_monster(request: Request):
    return templates.TemplateResponse("progress-monster.html", {"request": request})

@app.get("/api/{api_name}")
def interact_api(api_name, q:str = "nothing"):
    return JSONResponse({"api_name": api_name, "q": q})


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return JSONResponse({"item_id": item_id, "q": q})








#just for testing

# Example in-memory "database" for dynamic pages
CLIENTS = {
    "acme": {"name": "Acme, Ltd", "bio": "Acme does widgets.", "theme_color": "#0b62a4"},
    "globex": {"name": "Globex Corp", "bio": "Globex builds rockets.", "theme_color": "#a42b0b"},
}


@app.get("/client/{client_id}")
async def client_page(request: Request, client_id: str):
    """Render a dynamic client page using a path parameter.

    Demonstrates how to pass per-client data to a Jinja2 template.
    """
    client = CLIENTS.get(client_id)
    if not client:
        # return a simple 404 template response (or raise HTTPException(404))
        return JSONResponse({"error": "client not found"}, status_code=404)

    return templates.TemplateResponse("client.html", {"request": request, "client": client, "client_id": client_id})


@app.post("/inspect")
async def inspect_request(request: Request):
    """Inspect the incoming Request: read IP, headers, cookies and body.

    - Use `request.client` to get the connecting IP (tuple (host, port) or None).
    - Use `request.headers` to access headers (case-insensitive).
    - Use `request.cookies` to access parsed cookies.
    - Use `await request.json()` or `await request.body()` to read the body (async).

    Note: reading the body consumes it; don't read twice unless you buffered it.
    """
    # remote address (host, port) if available
    client_info = None
    if request.client:
        client_info = {"host": request.client.host, "port": request.client.port}

    # headers -> convert to normal dict (strings)
    headers = dict(request.headers)

    # cookies (dict)
    cookies = request.cookies

    # try to parse JSON body; fall back to raw bytes
    body = None
    body_text = None
    try:
        body = await request.json()
    except Exception:
        # not JSON or empty - fallback to raw bytes
        raw = await request.body()
        try:
            body_text = raw.decode("utf-8") if raw else None
        except Exception:
            body_text = str(raw)

    payload = {
        "client": client_info,
        "headers": headers,
        "cookies": cookies,
        "json_body": body,
        "raw_body": body_text,
    }

    return JSONResponse(payload)
