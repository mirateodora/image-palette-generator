import cv2
import numpy as np
from sklearn.cluster import KMeans

def extract_colors(img_path, n):
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError("Image not found")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (600, 400))

    pixels = img.reshape(-1, 3)

    kmeans = KMeans(n_clusters=n, random_state=42)
    labels = kmeans.fit_predict(pixels)
    colors = kmeans.cluster_centers_.astype(int)

    counts = np.bincount(labels)
    sorted_idx = np.argsort(-counts)
    sorted_colors = colors[sorted_idx]

    return [tuple(c) for c in sorted_colors]


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)