from PIL import Image, ImageStat
import requests
from io import BytesIO

from modelprep.YoutubeAPI import YouTubeAPI
import pandas as pd

import os.path


class Scraper:
    access_api = YouTubeAPI()
    thumbnail_links = []
    statistics = []
    
    def _upload_thumbnail(self, id, thumbnail_link):
        photo_request = requests.get(thumbnail_link)
        if photo_request.status_code == 200 and os.path.exists('src/data/{id}.jpg') == False:
            with open(f'src/data/{id}.jpg', 'wb') as f:
                f.write(photo_request.content)
        
    def upload_videos(self, id_list):
        for i in id_list:
            title, upload_date, views, thumbnail_url = self.access_api.get_video_metrics(i)
            self.thumbnail_links.append(thumbnail_url)
            self.statistics.append({'ID':i, 'Title':title, 'Date':upload_date, 'Views': views})
            self._upload_thumbnail(i, thumbnail_url)
            print(f"Uploaded {title}")
            
        additional_df = pd.DataFrame(self.statistics)
            
        try:
            existing_df = pd.read_csv('src/data/raw_metrics.csv')
            df = pd.concat([existing_df, additional_df]).drop_duplicates("ID")
            df.to_csv('src/data/raw_metrics.csv', index=False)

            print("Statistics Saved")
        except:
            additional_df.to_csv('src/data/raw_metrics.csv', index=False)
            print("No existing data, new data saved")