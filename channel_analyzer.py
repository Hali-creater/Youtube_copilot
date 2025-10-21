import streamlit as st
import random
from youtube_api import get_youtube_service, get_channel_stats, get_top_videos
import re

def get_channel_id_from_url(url):
    """
    Extracts the channel ID from various YouTube channel URL formats.
    """
    patterns = [
        r'(?:youtube\.com/channel/)([a-zA-Z0-9_-]+)',
        r'(?:youtube\.com/c/)([a-zA-Z0-9_-]+)',
        r'(?:youtube\.com/user/)([a-zA-Z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def show_channel_analyzer():
    st.header("Channel Analyzer")

    channel_url = st.text_input("Enter a YouTube Channel URL:")
    if st.button("Analyze Channel"):
        if not st.session_state.api_key:
            st.error("Please enter your YouTube API Key in the sidebar.")
        elif not channel_url:
            st.warning("Please enter a channel URL.")
        else:
            channel_id = get_channel_id_from_url(channel_url)
            if channel_id:
                st.session_state.analysis_complete = True
                st.session_state.channel_id = channel_id
            else:
                st.error("Could not extract a valid Channel ID, username, or custom URL from the provided URL.")
                st.session_state.analysis_complete = False

    if 'analysis_complete' in st.session_state and st.session_state.analysis_complete:
        youtube = get_youtube_service(st.session_state.api_key)
        if youtube:
            # Fetch and display channel stats
            stats = get_channel_stats(youtube, st.session_state.channel_id)
            top_videos = get_top_videos(youtube, st.session_state.channel_id)

            if stats and top_videos:
                st.subheader("Channel Statistics")
                st.write(f"**Subscribers:** {int(stats['subscriberCount']):,}")
                st.write(f"**Total Views:** {int(stats['viewCount']):,}")
                st.write(f"**Total Videos:** {int(stats['videoCount']):,}")

                st.subheader("Analysis Dashboard")

                top_topics = [video['title'] for video in top_videos]
                st.markdown("#### Key Insights:")
                st.success(f"Your top performing videos are: **{', '.join(top_topics)}**.")
                st.info("Your audience is mostly: **25-34 year olds interested in technology and programming** (Simulated).")
                st.warning("We've identified a gap in: **Advanced Python topics like asynchronous programming** (Simulated).")

                st.markdown("---")

                st.subheader("Next Video Recommendations")

                rec_1 = "Async Python Tutorial for Beginners"
                rec_2 = "Building a FastAPI Application"
                rec_3 = "Advanced Data Structures in Python"

                recommendations = {
                    rec_1: f"{random.uniform(85, 95):.2f}%",
                    rec_2: f"{random.uniform(75, 85):.2f}%",
                    rec_3: f"{random.uniform(70, 80):.2f}%"
                }

                selected_concept = st.radio("Select a concept to generate content:", list(recommendations.keys()))

                st.write(f"**Confidence Score:** {recommendations[selected_concept]}")

                if st.button("Generate Script & SEO Pack"):
                    st.subheader(f"Content for: {selected_concept}")

                    st.markdown("#### SEO Pack")
                    st.write(f"**Suggested Titles:**")
                    st.write(f"- {selected_concept}")
                    st.write(f"- A Guide to {selected_concept}")
                    st.write(f"- Master {selected_concept} in 10 Minutes")

                    st.write(f"**Keywords:** {selected_concept.lower()}, python, programming, tutorial")

                    st.markdown("#### Script Outline")
                    st.write("- **Hook:** Start with a compelling problem that the video will solve.")
                    st.write("- **Introduction:** Briefly explain what the video will cover.")
                    st.write("- **Main Content:** Break down the topic into 3-4 key points.")
                    st.write("- **Conclusion:** Summarize and provide a call to action.")
