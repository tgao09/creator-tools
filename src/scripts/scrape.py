import sys
import os

from modelprep.youtube_api import YouTubeAPI

yt_api = YouTubeAPI()  # Create an API instance
youtube = yt_api.get_service()  # Get the YouTube API service

if(youtube):
    print("YouTube API service created successfully")