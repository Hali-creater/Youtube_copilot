import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def show_analytics_decoder():
    st.header("Analytics Decoder")
    st.markdown("""
    *   **Primary Purpose:** To help YouTubers understand their channel analytics, identify growth opportunities, and make data-driven decisions.
    *   **Target User:** YouTubers who want to gain deeper insights from their performance data.
    """)

    st.subheader("Upload Your Analytics Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df_analytics = pd.read_csv(uploaded_file)

        # Check for required columns
        required_columns = ['Date', 'Views', 'Watch Time (hours)', 'Subscribers Gained', 'Estimated Revenue (USD)']
        if all(col in df_analytics.columns for col in required_columns):
            df_analytics['Date'] = pd.to_datetime(df_analytics['Date'])

            st.subheader("Your Analytics Data")
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
            st.error(f"The uploaded CSV file must contain the following columns: {', '.join(required_columns)}")
    else:
        st.info("Upload a CSV file to see your analytics.")
