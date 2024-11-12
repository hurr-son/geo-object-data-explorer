from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from titiler.core.factory import TilerFactory
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from fastapi.responses import JSONResponse
import rasterio
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="My simple app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cog = TilerFactory()
app.include_router(cog.router, tags=["Cloud Optimized GeoTIFF"])

add_exception_handlers(app, DEFAULT_STATUS_CODES)

@app.get("/healthz", description="Health Check", tags=["Health Check"])
def ping():
    """Health check."""
    return {"ping": "pong!"}

geojson_file_path = Path("/home/hurr_son/repos/geo-object-search/backends/data/detections.geojson")

from fastapi.responses import Response

@app.get("/geojson")
async def get_geojson():
    if geojson_file_path.exists():
        with geojson_file_path.open() as f:
            data = f.read()
        return Response(content=data, media_type="application/geo+json")
    else:
        return JSONResponse(content={"error": "GeoJSON file not found"}, status_code=404)
