import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from youtube_api import get_youtube_service, get_channel_analytics

def show_analytics_decoder():
    st.header("Analytics Decoder")
    st.markdown("""
    *   **Primary Purpose:** To help YouTubers understand their channel analytics, identify growth opportunities, and make data-driven decisions.
    *   **Target User:** YouTubers who want to gain deeper insights from their performance data.
    """)

    if not st.session_state.api_key:
        st.error("Please enter your YouTube API Key in the sidebar to use this feature.")
    else:
        youtube = get_youtube_service(st.session_state.api_key)
        if youtube:
            # For this to work with real data, channel_id would need to be fetched
            # after user authentication (OAuth). We'll use a placeholder.
            channel_id = "UC-lHJZR3Gqxm24_Vd_AJ5Yw" # Google Developers channel for demonstration

            analytics_data = get_channel_analytics(youtube, channel_id)

            if analytics_data and 'rows' in analytics_data:
                df_analytics = pd.DataFrame(analytics_data['rows'], columns=['Date', 'Views', 'Watch Time (hours)', 'Subscribers Gained', 'Estimated Revenue (USD)'])
                df_analytics['Date'] = pd.to_datetime(df_analytics['Date'])

                st.subheader("Your Analytics Data (Simulated)")
                st.dataframe(df_analytics)

                st.subheader("Key Performance Metrics Over Time")
                fig, axes = plt.subplots(2, 2, figsize=(15, 10))

                sns.lineplot(ax=axes[0, 0], data=df_analytics, x='Date', y='Views')
                axes[0, 0].set_title('Daily Views Over Time')
                axes[0, 0].tick_params(axis='x', rotation=45)

                sns.lineplot(ax=axes[0, 1], data=df_analytics, x='Date', y='Watch Time (hours)')
                axes[0, 1].set_title('Daily Watch Time (hours) Over Time')
                axes[0, 1].tick_params(axis='x', rotation=45)

                sns.lineplot(ax=axes[1, 0], data=df_analytics, x='Date', y='Subscribers Gained')
                axes[1, 0].set_title('Daily Subscribers Gained Over Time')
                axes[1, 0].tick_params(axis='x', rotation=45)

                sns.lineplot(ax=axes[1, 1], data=df_analytics, x='Date', y='Estimated Revenue (USD)')
                axes[1, 1].set_title('Daily Estimated Revenue (USD) Over Time')
                axes[1, 1].tick_params(axis='x', rotation=45)

                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("Could not retrieve analytics data.")
