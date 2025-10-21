import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
from youtube_api import get_youtube_service, get_trending_videos

def show_brainstorm_pro():
    st.header("Brainstorm Pro")
    st.markdown("""
    *   **Primary Purpose:** To assist YouTubers in generating new video ideas, identifying trending topics, and understanding audience interests to create engaging content.
    *   **Target User:** YouTubers looking for inspiration and data-driven insights for content creation.
    """)

    st.subheader("Features")

    # Trend Analysis
    st.markdown("#### Google Trends Analysis")
    topic = st.text_input("Enter a topic or keyword to analyze trends:")
    if st.button("Analyze Trends"):
        if topic:
            try:
                pytrends = TrendReq(hl='en-US', tz=360)
                pytrends.build_payload([topic], cat=0, timeframe='today 5-y', geo='', gprop='')
                interest_over_time_df = pytrends.interest_over_time()

                if not interest_over_time_df.empty:
                    st.write(f"Showing Google Trends interest for: **{topic}**")
                    st.line_chart(interest_over_time_df[topic])
                else:
                    st.warning("Could not retrieve trend data for this topic. Please try another.")
            except Exception as e:
                st.error(f"An error occurred while fetching trend data: {e}")
        else:
            st.warning("Please enter a topic.")

    st.markdown("---")

    st.markdown("#### Trending on YouTube")
    if st.button("Get YouTube Trends"):
        if not st.session_state.api_key:
            st.error("Please enter your YouTube API Key in the sidebar.")
        else:
            youtube = get_youtube_service(st.session_state.api_key)
            if youtube:
                trending_videos = get_trending_videos(youtube)
                if trending_videos:
                    st.write("### Currently Trending Videos on YouTube")
                    for video in trending_videos:
                        st.write(f"- **{video['title']}** ({video['views']:,} views)")

    st.markdown("---")

    # Keyword Suggestion
    st.markdown("#### Keyword Suggestion")
    video_topic_keyword = st.text_input("Enter a broad video topic for keyword suggestions:")
    if st.button("Suggest Keywords"):
        if video_topic_keyword:
            st.write(f"Keyword suggestions for: **{video_topic_keyword}**")
            # Simulated keyword data
            keyword_data = {
                "Keyword": [f"{video_topic_keyword} tutorial", f"best {video_topic_keyword} 2023", f"{video_topic_keyword} for beginners", f"DIY {video_topic_keyword}"],
                "Search Volume": ["High", "Medium", "High", "Low"],
                "Competition": ["High", "Medium", "Low", "Medium"]
            }
            keyword_df = pd.DataFrame(keyword_data)
            st.table(keyword_df)
        else:
            st.warning("Please enter a video topic.")
