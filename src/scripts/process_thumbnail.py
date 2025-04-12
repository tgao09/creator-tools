import os
import cv2
import numpy as np
import pandas as pd

def compute_features(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None  # skip unreadable files

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Mean and std of RGB
    mean_rgb = np.mean(img_rgb, axis=(0, 1))
    std_rgb = np.std(img_rgb, axis=(0, 1))

    # Saturation (mean of S channel)
    saturation = np.mean(img_hsv[:, :, 1])

    # Contrast (std of grayscale image)
    contrast = np.std(img_gray)

    # Brightness (mean of grayscale image)
    brightness = np.mean(img_gray)

    # Edge density using Canny
    edges = cv2.Canny(img_gray, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size

    return {
        'ID': os.path.splitext(os.path.basename(image_path))[0],
        'mean_r': mean_rgb[0],
        'mean_g': mean_rgb[1],
        'mean_b': mean_rgb[2],
        'std_r': std_rgb[0],
        'std_g': std_rgb[1],
        'std_b': std_rgb[2],
        'saturation': saturation,
        'contrast': contrast,
        'brightness': brightness,
        'edge_density': edge_density
    }

from sklearn.preprocessing import StandardScaler
import joblib

def process_folder(folder_path, output_csv='src/data/image_features.csv'):
    features = []
    for file in os.listdir(folder_path):
        if file.lower().endswith('.jpg'):
            path = os.path.join(folder_path, file)
            result = compute_features(path)
            if result:
                features.append(result)

    df = pd.DataFrame(features)

    # Preserve ID separately
    IDs = df['ID']
    feature_cols = df.columns.drop('ID')

    # Standardize features
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df[feature_cols]), columns=feature_cols)
    df_scaled.insert(0, 'ID', IDs)

    joblib.dump(scaler, 'src/scaler.pkl')

    df_scaled.to_csv(output_csv, index=False)
    print(f"Saved standardized features for {len(df_scaled)} images to {output_csv}")

image_folder = "src/data/thumbnails"
process_folder(image_folder)
