import torch
import torchvision.transforms as T
from PIL import Image
import faiss
import numpy as np
import cv2
import matplotlib.pyplot as plt
import json
import sys
import os
import geopandas as gpd

dinov2_vits14 = torch.hub.load("facebookresearch/dinov2", "dinov2_vits14")
device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
dinov2_vits14.to(device)
dinov2_vits14.eval()

transform_image = T.Compose([
    T.Resize(244),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize([0.5], [0.5])
])

def load_image(img_path: str) -> torch.Tensor:
    img = Image.open(img_path).convert('RGB')
    transformed_img = transform_image(img).unsqueeze(0)
    return transformed_img

def search_index(index: faiss.IndexFlatL2, embedding: np.ndarray, k: int = 64) -> list:
    D, I = index.search(embedding.reshape(1, -1), k)
    return I[0][:k]

def extract_uuid_from_filename(file_path: str) -> str:
    filename = os.path.basename(file_path)
    uuid = os.path.splitext(filename)[0]
    return uuid

def main():

    if len(sys.argv) != 2:
        print("Usage: python query_index.py <path_to_query_image>")
        sys.exit(1)

    search_file = sys.argv[1]

    print("*" * 20)

    k = 256

    with torch.no_grad():
        embedding = dinov2_vits14(load_image(search_file).to(device))
        embedding_np = embedding.cpu().numpy()

    data_index = faiss.read_index("/home/hurr_son/repos/geo-object-data-explorer/backends/data/data.bin")

    with open("/home/hurr_son/repos/geo-object-data-explorer/backends/data/all_embeddings.json", "r") as f:
        all_embeddings = json.load(f)
    files = list(all_embeddings.keys())

    indices = search_index(data_index, embedding_np, k=k)

    uuids = []
    print(f"Top {k} similar images:")
    for i in range(k):
        if i < len(indices):
            img_path = files[indices[i]]
            print(f"Rank {i+1}: {img_path}")
            uuid = extract_uuid_from_filename(img_path)
            uuids.append(uuid)
        else:
            print(f"Rank {i+1}: No more results.")

    detections_gdf = gpd.read_file("/home/hurr_son/repos/geo-object-data-explorer/backends/data/detections.geojson")

    if 'detection_id' not in detections_gdf.columns:
        if 'properties' in detections_gdf.columns:
            detections_gdf['detection_id'] = detections_gdf['properties'].apply(lambda x: x['detection_id'])
        else:
            print("Error: 'detection_id' not found in GeoDataFrame.")
            sys.exit(1)

    filtered_gdf = detections_gdf[detections_gdf['detection_id'].isin(uuids)]

    filtered_gdf.to_file("/home/hurr_son/repos/geo-object-data-explorer/backends/data/topk_detections.geojson", driver="GeoJSON")

    print(f"Filtered GeoJSON saved to topk_detections.geojson")

if __name__ == "__main__":
    main()
