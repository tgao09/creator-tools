import pandas as pd

raw = pd.read_csv('src/data/raw_metrics.csv')
print(raw.head())
image = pd.read_csv('src/data/image_features.csv')
print(image.head())

processed = pd.merge(raw, image, on='ID', how='inner')
processed = processed.drop_duplicates(subset=['ID'])

processed.to_csv('src/data/processed_metrics.csv', index=False)
print("Joined raw metrics and image features to processed_metrics.csv")