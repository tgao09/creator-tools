from PIL import Image, ImageStat
import requests
from io import BytesIO

from modelprep.YoutubeAPI import YouTubeAPI
import pandas as pd


class Scraper:
    access_api = YouTubeAPI()
    thumbnail_links = []
    statistics = []
    
    def scrape_videos(self, id_list):
        for i in id_list:
            title, upload_date, views, thumbnail_url = self.access_api.get_video_metrics(i)
            self.thumbnail_links.append(thumbnail_url)
            self.statistics.append({'ID':i, 'Title':title, 'Date':upload_date, 'Views': views})
            print(f"Uploaded {title}")
            
        additional_df = pd.DataFrame(self.statistics)
            
        try:
            existing_df = pd.read_csv('src/data/raw_metrics.csv')
        except:
            additional_df.to_csv('src/data/raw_metrics.csv', index=False)
            print("No existing data, new data saved")
            return
        
        df = pd.concat([existing_df, additional_df]).drop_duplicates()
        df.to_csv('src/data/raw_metrics.csv', index=False)

        print("Statistics Saved")
        return