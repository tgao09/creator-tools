from modelprep.youtube_api import YouTubeAPI
import pandas as pd

access_api = YouTubeAPI()

links = ['20vUNgRdB4o', '7dh7R2zfhfI', 'WzN0RNBqdz4']
videos = []

for i in links:
    title, upload_date, views = access_api.get_video_metrics(i)
    videos.append({'Title':title, 'Date':upload_date, 'Views': views})

df = pd.DataFrame(videos)
df.to_csv('src/data/raw_metrics.csv', index=False)