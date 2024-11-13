# Geo Object Data Explorer

**Note:** This project is a work in progress.

### Features I would like to add

- Query crop from map
- Export labels + image chips for model training
- Visualize inference on raster

## Overview

Geo Object Data Explorer is a web application that allows users to visualize and explore geospatial data, particularly focused on detecting and displaying objects using image embeddings and similarity search. The application combines a Leaflet.js map interface with a backend powered by FastAPI and PyTorch models.

## Features

- **Interactive Map Visualization:** Displays geospatial data on an interactive map using Leaflet.js.
- **Object Detection and Similarity Search:** Utilizes Facebook's DINOv2 model for image embedding and FAISS for efficient similarity search.
- **GeoJSON Data Rendering:** Fetches and displays GeoJSON data for detected objects.
- **Tile Serving:** Serves raster data tiles using Titiler and FastAPI.

## Technologies Used

- **Frontend:**
  - HTML, CSS, JavaScript
  - [Leaflet.js](https://leafletjs.com/) for map rendering
- **Backend:**
  - [FastAPI](https://fastapi.tiangolo.com/) for API endpoints
  - [PyTorch](https://pytorch.org/) and DINOv2 for image embeddings
  - [FAISS](https://github.com/facebookresearch/faiss) for similarity search
  - [Geopandas](https://geopandas.org/) for geospatial data handling
  - [Titiler](https://github.com/developmentseed/titiler) for serving raster tiles

## License

This project is licensed under the MIT License.

## Acknowledgments

- Inspired by [Image Retrieval with DINOv2](https://github.com/roboflow/notebooks/blob/main/notebooks/dinov2-image-retrieval.ipynb) Roboflow Notebook
- [Facebook AI Research](https://ai.facebook.com/) for the DINOv2 model and FAISS.
- [OpenStreetMap Contributors](https://www.openstreetmap.org/copyright) for map tiles.
- [NOAA Office for Coastal Management](https://coast.noaa.gov/) for geospatial data.