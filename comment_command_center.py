import streamlit as st
import pandas as pd

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
    comments_input = st.text_area("Paste a list of comments (one per line):")
    if st.button("Analyze Comments"):
        if comments_input:
            comments = comments_input.splitlines()
            sentiments = [analyze_sentiment(comment) for comment in comments]

            comment_data = {
                "Comment": comments,
                "Sentiment": sentiments
            }
            comment_df = pd.DataFrame(comment_data)

            st.write("### Sentiment Analysis Results")
            st.dataframe(comment_df)

            st.write("### Sentiment Distribution")
            sentiment_counts = comment_df["Sentiment"].value_counts()
            st.bar_chart(sentiment_counts)
        else:
            st.warning("Please paste some comments to analyze.")
