import streamlit as st
from brainstorm_pro import show_brainstorm_pro
from script_genius import show_script_genius
from thumbnail_predictor import show_thumbnail_predictor
from comment_command_center import show_comment_command_center
from analytics_decoder import show_analytics_decoder
from channel_analyzer import show_channel_analyzer

def main():
    st.title("AI Agent for YouTubers")
    st.write("This application provides a suite of tools to help YouTubers create engaging content, analyze performance, and manage their community.")

    st.sidebar.title("Settings")
    st.session_state.api_key = st.sidebar.text_input("Enter your YouTube API Key:", type="password")

    st.sidebar.title("Navigation")
    module = st.sidebar.radio("Go to", [
        "Channel Analyzer",
        "Brainstorm Pro",
        "Script Genius",
        "Thumbnail & Title Predictor",
        "Comment Command Center",
        "Analytics Decoder"
    ])

    if module == "Channel Analyzer":
        show_channel_analyzer()
    elif module == "Brainstorm Pro":
        show_brainstorm_pro()
    elif module == "Script Genius":
        show_script_genius()
    elif module == "Thumbnail & Title Predictor":
        show_thumbnail_predictor()
    elif module == "Comment Command Center":
        show_comment_command_center()
    elif module == "Analytics Decoder":
        show_analytics_decoder()

if __name__ == "__main__":
    main()
