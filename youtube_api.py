from googleapiclient.discovery import build
import streamlit as st

@st.cache_data
def get_youtube_service(api_key):
    """Initializes and returns the YouTube API service."""
    try:
        return build('youtube', 'v3', developerKey=api_key)
    except Exception as e:
        st.error(f"Error initializing YouTube API: {e}")
        return None

def get_channel_stats(youtube, channel_id):
    """Fetches channel statistics."""
    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        return response['items'][0]['statistics']
    except Exception as e:
        st.error(f"Error fetching channel stats: {e}")
        return {}

def get_top_videos(youtube, channel_id):
    """Fetches a channel's top videos."""
    try:
        # First, get the uploads playlist ID
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        response = request.execute()
        playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Then, get the videos from the uploads playlist
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=10
        )
        response = request.execute()

        videos = []
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            # Get video stats (like view count)
            video_request = youtube.videos().list(
                part="statistics",
                id=video_id
            )
            video_response = video_request.execute()
            videos.append({
                "title": item['snippet']['title'],
                "views": int(video_response['items'][0]['statistics']['viewCount'])
            })

        # Sort by views and return top 3
        return sorted(videos, key=lambda x: x['views'], reverse=True)[:3]

    except Exception as e:
        st.error(f"Error fetching top videos: {e}")
        return []

def get_trending_videos(youtube):
    """Fetches trending videos on YouTube."""
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode="US",
            maxResults=10
        )
        response = request.execute()
        videos = []
        for item in response['items']:
            videos.append({
                "title": item['snippet']['title'],
                "views": int(item['statistics']['viewCount'])
            })
        return videos
    except Exception as e:
        st.error(f"Error fetching trending videos: {e}")
        return []

def get_channel_analytics(youtube, channel_id):
    """
    Simulates fetching channel analytics data.
    In a real application, this would require OAuth2 and the YouTube Analytics API.
    """
    st.info("Note: The YouTube Analytics API requires OAuth2 authentication for the channel owner. As we only have a developer key, this feature is simulated with sample data.")
    return {
        "rows": [
            ["2023-01-01", 1500, 50, 10, 5.50],
            ["2023-01-02", 1600, 55, 12, 6.00],
            ["2023-01-03", 1700, 60, 15, 6.20],
            ["2023-01-04", 1800, 65, 18, 7.00],
            ["2023-01-05", 1900, 70, 20, 7.50]
        ]
    }

def get_video_comments(youtube, video_id):
    """
    Fetches comments for a video.
    """
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )
        response = request.execute()

        comments = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                "author": comment['authorDisplayName'],
                "text": comment['textDisplay']
            })
        return comments
    except Exception as e:
        st.error(f"Error fetching comments: {e}")
        return []
