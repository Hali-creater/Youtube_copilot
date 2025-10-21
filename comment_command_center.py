import streamlit as st
import pandas as pd
from youtube_api import get_youtube_service, get_video_comments
import re

def get_video_id_from_url(url):
    """
    Extracts the video ID from a YouTube video URL.
    """
    match = re.search(r'(?:v=)([^&]+)', url)
    if match:
        return match.group(1)
    return None

def analyze_sentiment(comment):
    # Basic sentiment analysis based on keywords
    positive_keywords = ["love", "great", "awesome", "excellent", "amazing"]
    negative_keywords = ["hate", "bad", "terrible", "awful", "dislike"]

    comment_lower = comment.lower()

    for word in positive_keywords:
        if word in comment_lower:
            return "Positive"

    for word in negative_keywords:
        if word in comment_lower:
            return "Negative"

    return "Neutral"

def show_comment_command_center():
    st.header("Comment Command Center")
    st.markdown("""
    *   **Primary Purpose:** To assist YouTubers in managing and engaging with their video comments effectively.
    *   **Target User:** YouTubers who want to build a community and efficiently handle comments.
    """)

    st.subheader("Features")

    # Comment Sentiment Analysis
    st.markdown("#### Comment Sentiment Analysis")
    video_url = st.text_input("Enter a YouTube Video URL to analyze comments:")
    if st.button("Analyze Comments"):
        if not st.session_state.api_key:
            st.error("Please enter your YouTube API Key in the sidebar.")
        elif not video_url:
            st.warning("Please enter a video URL.")
        else:
            video_id = get_video_id_from_url(video_url)
            if video_id:
                youtube = get_youtube_service(st.session_state.api_key)
                if youtube:
                    comments = get_video_comments(youtube, video_id)
                    if comments:
                        sentiments = [analyze_sentiment(comment['text']) for comment in comments]

                        comment_data = {
                            "Author": [comment['author'] for comment in comments],
                            "Comment": [comment['text'] for comment in comments],
                            "Sentiment": sentiments
                        }
                        comment_df = pd.DataFrame(comment_data)

                        st.write("### Sentiment Analysis Results")
                        st.dataframe(comment_df)

                        st.write("### Sentiment Distribution")
                        sentiment_counts = comment_df["Sentiment"].value_counts()
                        st.bar_chart(sentiment_counts)
                    else:
                        st.warning("Could not retrieve comments for this video. This could be due to disabled comments or an invalid video ID.")
            else:
                st.error("Invalid YouTube video URL.")
