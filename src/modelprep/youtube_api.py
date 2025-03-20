import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd

class YouTubeAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not found in .env file")
        self.youtube = self._build_api()

    def _build_api(self):
        return build("youtube", "v3", developerKey=self.api_key)

    def get_video_metrics(self, video_id):
        request = self.youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        
        response = request.execute()
        
        if "items" in response and len(response["items"]) > 0:
            video = response["items"][0]
            title = video["snippet"]["title"]
            upload_date = video["snippet"]["publishedAt"]
            views = video["statistics"]["viewCount"]
            
            return [title, upload_date, views]
        else:
            print("Video not found")
