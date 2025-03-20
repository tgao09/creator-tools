import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import csv

class YouTubeAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not found in .env file")
        self.youtube = self._build_api()

    def _build_api(self):
        return build("youtube", "v3", developerKey=self.api_key)

    def get_service(self):
        return self.youtube